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

_Ω_BASE  = "https://downr.org/.netlify/functions"
_Ω_HDR   = {
    "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36",
    "Origin":       "https://downr.org",
    "Referer":      "https://downr.org/",
    "Content-Type": "application/json",
}

_Ω_VIMEO_PATTERN = re.compile(
    r"(https?://)?(www\.)?(vimeo\.com|player\.vimeo\.com)/",
    re.IGNORECASE,
)

def is_valid_vimeo_url(url: str) -> bool:
    return bool(_Ω_VIMEO_PATTERN.search(url))


def _Ω_session() -> requests.Session:
    s = requests.Session()
    try:
        s.get(f"{_Ω_BASE}/analytics", headers=_Ω_HDR, timeout=8)
    except Exception:
        pass
    return s


def _Ω_pick_best(medias: list) -> dict:
    _res_order = ["1080", "720", "480", "360", "240"]
    for target in _res_order:
        for m in medias:
            q = (m.get("quality") or "").lower()
            if target in q:
                return m
    return medias[0] if medias else {}


def fetch_vimeo(url: str) -> dict:
    if not is_valid_vimeo_url(url):
        return {"success": False, "error": "invalid_vimeo_url"}

    s = _Ω_session()
    try:
        r = s.post(
            f"{_Ω_BASE}/nyt",
            json={"url": url},
            headers=_Ω_HDR,
            timeout=30,
        )
        if r.status_code != 200:
            return {"success": False, "error": f"http_{r.status_code}"}
        data = r.json()
        if data.get("error"):
            return {"success": False, "error": "api_error"}

        medias = data.get("medias", [])
        if not medias:
            return {"success": False, "error": "no_media_found"}

        best    = _Ω_pick_best(medias)
        dl_url  = best.get("url", "")
        quality = best.get("quality", "")

        return {
            "success":      True,
            "title":        data.get("title", ""),
            "author":       data.get("author", ""),
            "thumbnail":    "",
            "duration":     0,
            "format":       "mp4",
            "quality":      quality,
            "filesize_mb":  0.0,
            "download_url": dl_url,
            "all_medias":   medias,
            "error":        None,
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        s.close()
