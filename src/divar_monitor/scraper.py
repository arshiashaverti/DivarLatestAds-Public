from urllib.parse import urljoin, urlparse

from playwright.async_api import Page


async def scrape_ads(
    page: Page,
    url: str,
    limit: int = 10,
    wait_ms: int = 4000,
) -> list[dict[str, str]]:
    response = await page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000,
    )

    if response is None:
        raise RuntimeError("The target page did not return a response.")

    if response.status >= 400:
        raise RuntimeError(f"Target website returned HTTP {response.status}.")

    if wait_ms:
        await page.wait_for_timeout(wait_ms)

    cards = page.locator('a[href*="/v/"]')
    results: list[dict[str, str]] = []
    seen: set[str] = set()

    for index in range(await cards.count()):
        card = cards.nth(index)
        href = await card.get_attribute("href")

        if not href:
            continue

        link = urljoin("https://divar.ir", href)
        parsed = urlparse(link)

        if parsed.netloc not in {"divar.ir", "www.divar.ir"}:
            continue

        if "/v/" not in parsed.path or link in seen:
            continue

        title = " ".join((await card.inner_text()).split())
        if not title:
            continue

        ad_id = parsed.path.rstrip("/").split("/")[-1]
        if not ad_id:
            continue

        seen.add(link)
        results.append({
            "id": ad_id,
            "title": title,
            "url": link,
        })

        if len(results) >= limit:
            break

    if not results:
        raise RuntimeError(
            "No listings were extracted. The page structure may have changed "
            "or the website may have blocked the request."
        )

    return results