import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright

from .config import load_settings
from .scraper import scrape_ads


async def export_ads(output: Path) -> None:
    settings = load_settings()

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
        finally:
            await browser.close()

    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": settings.url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(ads),
        "ads": ads,
    }
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {len(ads)} listings to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect listings from a configured Divar search page."
    )
    parser.add_argument(
        "--output",
        default="data/ads.json",
        help="Output JSON file (default: data/ads.json)",
    )
    args = parser.parse_args()
    asyncio.run(export_ads(Path(args.output)))


if __name__ == "__main__":
    main()