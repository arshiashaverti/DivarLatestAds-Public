import asyncio
import logging
import os
import shutil
from pathlib import Path

from playwright.async_api import async_playwright

from .config import load_settings
from .scraper import scrape_ads
from .storage import find_new_ads, load_ids, save_ids

LOGGER = logging.getLogger("divar_monitor.local")


def notify_windows(title: str, message: str, link: str) -> None:
    if os.name != "nt":
        LOGGER.warning("Windows notifications are only available on Windows.")
        return

    try:
        from winotify import Notification, audio

        toast = Notification(
            app_id="Divar New Ads Monitor",
            title=title[:200],
            msg=message[:400],
            duration="long",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.add_actions(label="View listing", launch=link)
        toast.show()
    except Exception:
        LOGGER.exception("Could not display Windows notification.")


def find_browser() -> str | None:
    candidates = [
        shutil.which("chrome"),
        shutil.which("msedge"),
        os.path.expandvars(
            r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate

    return None


async def run() -> None:
    settings = load_settings()
    state_path = Path(settings.state_file)
    known_ids = load_ids(state_path)

    browser_path = find_browser()

    async with async_playwright() as playwright:
        launch_options = {"headless": True}
        if browser_path:
            launch_options["executable_path"] = browser_path

        browser = await playwright.chromium.launch(**launch_options)

        try:
            page = await browser.new_page(locale="fa-IR")
            while True:
                try:
                    ads = await scrape_ads(
                        page,
                        settings.url,
                        settings.max_ads,
                        settings.wait_ms,
                    )

                    if not known_ids:
                        known_ids.update(ad["id"] for ad in ads)
                        save_ids(state_path, known_ids)
                        LOGGER.info(
                            "Initial baseline saved: %d listings.",
                            len(ads),
                        )
                    else:
                        new_ads = find_new_ads(ads, known_ids)

                        for ad in reversed(new_ads):
                            notify_windows(
                                "New Divar listing",
                                ad["title"],
                                ad["url"],
                            )
                            known_ids.add(ad["id"])
                            save_ids(state_path, known_ids)

                        LOGGER.info(
                            "Checked %d listings; %d new.",
                            len(ads),
                            len(new_ads),
                        )

                except Exception:
                    LOGGER.exception("Monitoring cycle failed.")

                await asyncio.sleep(300)
        finally:
            await browser.close()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        LOGGER.info("Monitoring stopped by user.")


if __name__ == "__main__":
    main()