import asyncio
import logging
from pathlib import Path

from playwright.async_api import async_playwright

from .config import get_telegram_credentials, load_settings
from .scraper import scrape_ads
from .storage import find_new_ads, load_ids, save_ids
from .telegram import send_telegram_message

LOGGER = logging.getLogger("divar_monitor.cloud")


async def run() -> None:
    get_telegram_credentials()
    settings = load_settings()
    state_path = Path(settings.state_file)
    known_ids = load_ids(state_path)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        try:
            page = await browser.new_page(locale="fa-IR")
            ads = await scrape_ads(
                page,
                settings.url,
                settings.max_ads,
                settings.wait_ms,
            )

            if not known_ids:
                save_ids(state_path, {ad["id"] for ad in ads})
                LOGGER.info(
                    "Initial baseline saved. No notifications sent."
                )
                return

            new_ads = find_new_ads(ads, known_ids)
            LOGGER.info("Found %d new listings.", len(new_ads))

            for ad in reversed(new_ads):
                message = (
                    "🆕 New Divar listing\n\n"
                    f"{ad['title']}\n\n{ad['url']}"
                )

                # Save each ID only after Telegram confirms delivery.
                send_telegram_message(message)
                known_ids.add(ad["id"])
                save_ids(state_path, known_ids)
                LOGGER.info("Notification sent for listing %s.", ad["id"])

            known_ids.update(ad["id"] for ad in ads)
            save_ids(state_path, known_ids)

        finally:
            await browser.close()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    asyncio.run(run())


if __name__ == "__main__":
    main()