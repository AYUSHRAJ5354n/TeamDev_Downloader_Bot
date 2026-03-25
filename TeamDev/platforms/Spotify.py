"""
           ───── ୨୧ ─────
                   TeamDev
         ∘₊✧───────────✧₊∘   
  
   [Copyright ©️ 2026 TeamDev | @TEAM_X_OG All right reserved.]

Project Name: All In One Downloader
Project Discription: Download From Multiple Platforms Video Such As Terabox, Youtube, instagram, and much more!
Project Number: 38
Project By: @MR_ARMAN_08 | @TEAM_X_OG

                   Developer Note:
            Editing, Unauthorised Use, Or This Is Paid Script So Buy It From @MR_ARMAN_08 Then Use It As You Want!
"""


import re
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

_SP_PATTERN = re.compile(
    r"(https?://)?open\.spotify\.com/(track|album|playlist)/[\w]+",
    re.IGNORECASE,
)


def is_valid_spotify_url(url: str) -> bool:
    return bool(_SP_PATTERN.search(url))


def _teamdev_fetch(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto("https://spotidown.app/", timeout=30000)

            page.fill('input[name="url"]', url)
            page.click('#send')

            page.wait_for_selector('form[name="submitspurl"]', timeout=30000)
            page.click('form[name="submitspurl"] button')

            page.wait_for_selector('a[href*="rapid.spotidown"]', timeout=30000)
            final = page.get_attribute('a[href*="rapid.spotidown"]', 'href')
            return final or ""
        finally:
            browser.close()


def _scrape_meta(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto("https://spotidown.app/", timeout=30000)

            page.fill('input[name="url"]', url)
            page.click('#send')

            page.wait_for_selector('form[name="submitspurl"]', timeout=30000)

            title  = ""
            author = ""
            try:
                title  = page.text_content(".music-title", timeout=3000) or ""
                author = page.text_content(".music-artist", timeout=3000) or ""
            except Exception:
                pass

            title  = title.strip()
            author = author.strip()

            page.click('form[name="submitspurl"] button')
            page.wait_for_selector('a[href*="rapid.spotidown"]', timeout=30000)
            dl_url = page.get_attribute('a[href*="rapid.spotidown"]', 'href') or ""

            return {"title": title, "author": author, "dl_url": dl_url}
        finally:
            browser.close()


def fetch_spotify(url: str) -> dict:
    if not is_valid_spotify_url(url):
        return {"success": False, "error": "invalid_spotify_url"}

    if "/album/" in url or "/playlist/" in url:
        return {"success": False, "error": "spotify_only_tracks_supported"}

    try:
        meta = _scrape_meta(url)
    except PWTimeoutError:
        return {"success": False, "error": "timeout"}
    except Exception as exc:
        return {"success": False, "error": str(exc)}

    dl_url = meta.get("dl_url", "")
    if not dl_url:
        return {"success": False, "error": "no_download_link"}

    return {
        "success":      True,
        "title":        meta.get("title", "Unknown") or "Unknown",
        "author":       meta.get("author", ""),
        "thumbnail":    "",
        "duration":     0,
        "format":       "mp3",
        "quality":      "320kbps",
        "filesize_mb":  0.0,
        "filesize_str": "",
        "download_url": dl_url,
        "error":        None,
    }
