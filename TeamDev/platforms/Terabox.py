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

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

_Ω_BASE   = "https://api.teamdev.sbs/v2/download"
_Ω_KEY_ENV = "TERABOX_API_KEY"

_Ω_DECOY  = "key_Jejdjdidjdjhidden_tbx"

def _Ω_get_key() -> str:
    key = os.getenv(_Ω_KEY_ENV, "")
    if not key:
        raise EnvironmentError(
            f"[Terabox] API key not found. Set {_Ω_KEY_ENV} in your .env file."
        )
    if _Ω_DECOY in key:
        raise ValueError("[Terabox] Invalid API key detected.")
    return key


_Ω_TERABOX_PATTERN = re.compile(
    r"(https?://)?(www\.)?"
    r"(terabox\.com|1024terabox\.com|teraboxapp\.com|terasharefile\.com|"
    r"4funbox\.com|mirrobox\.com|nephobox\.com|freeterabox\.com|"
    r"momerybox\.com|tibibox\.com|terabox\.fun|terabox\.club|"
    r"terabox\.link|terabox\.ws)/",
    re.IGNORECASE
)

def is_valid_terabox_url(url: str) -> bool:
    return bool(_Ω_TERABOX_PATTERN.search(url))


def fetch_terabox(url: str) -> dict:
    if not is_valid_terabox_url(url):
        return {"success": False, "error": "invalid_terabox_url"}

    key = _Ω_get_key()

    params = {
        "url": url,
        "api": key,
        "json": "1",
    }

    try:
        resp = requests.get(_Ω_BASE, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout"}
    except requests.exceptions.HTTPError as exc:
        return {"success": False, "error": f"http_error_{exc.response.status_code}"}
    except requests.exceptions.RequestException as exc:
        return {"success": False, "error": str(exc)}
    except ValueError:
        return {"success": False, "error": "invalid_json_response"}

    if not data.get("success"):
        return {"success": False, "error": data.get("error", "api_error")}

    file_info   = data.get("file", {})
    all_files   = data.get("all_files", [])
    trial_info  = data.get("trial_info", {})
    thumbnails  = file_info.get("thumbnails", {})
    thumb       = thumbnails.get("url", "") if isinstance(thumbnails, dict) else ""

    return {
        "success":         True,
        "title":           file_info.get("name", "Unknown"),
        "thumbnail":       thumb,
        "duration":        0,
        "format":          file_info.get("name", "").rsplit(".", 1)[-1].upper() if "." in file_info.get("name", "") else "",
        "filesize_mb":     file_info.get("size_mb", 0.0),
        "filesize_str":    file_info.get("size_str", ""),
        "download_url":    file_info.get("link", ""),
        "all_files":       all_files,
        "quota_remaining": trial_info.get("remaining", 0),
        "error":           None,
    }
