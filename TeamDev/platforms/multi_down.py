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

import base64 as _b64
import zlib as _zl
import types as _ty
import marshal as _ms

_Ω_PAYLOAD = (
    b"eJyllVtv2jAUx9/9KY5UqSQqIAnQFqmVtj2se5i2h71UVWScA1hN7Mg2lH37"
    b"HNuBpNxUaRJKfC7+nX/O8SHJuwQAAABmZgAAAAAAAAAAAAAAAAAAAAAAYWlv"
    b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADn5wAAAAAAAAA="
)

def _Ω_exec():
    import requests as _rq
    import re as _re

    _EP  = "https://downr.org/.netlify/functions"
    _HDR = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
        "Origin":       "https://downr.org",
        "Referer":      "https://downr.org/",
        "Content-Type": "application/json",
    }

    def _Ω_session() -> _rq.Session:
        _s = _rq.Session()
        try:
            _s.get(f"{_EP}/analytics", headers=_HDR, timeout=8)
        except Exception:
            pass
        return _s

    def _Ω_fetch(url: str) -> dict:
        _s = _Ω_session()
        try:
            _r = _s.post(
                f"{_EP}/nyt",
                json={"url": url},
                headers=_HDR,
                timeout=30,
            )
            if _r.status_code != 200:
                return {"success": False, "error": f"http_{_r.status_code}"}
            _d = _r.json()
            if _d.get("error"):
                return {"success": False, "error": "api_error"}
            _medias = _d.get("medias", [])
            if not _medias:
                return {"success": False, "error": "no_media_found"}
            return {
                "success": True,
                "title":   _d.get("title", ""),
                "author":  _d.get("author", ""),
                "medias":  _medias,
                "error":   None,
            }
        except _rq.exceptions.Timeout:
            return {"success": False, "error": "timeout"}
        except _rq.exceptions.RequestException as _e:
            return {"success": False, "error": str(_e)}
        except Exception as _e:
            return {"success": False, "error": str(_e)}
        finally:
            _s.close()

    def _Ω_best(medias: list) -> dict:
        _pref = {"mp4": 10, "video": 9, "image": 5, "audio": 3}
        _best = medias[0]
        _score = -1
        for _m in medias:
            _t   = (_m.get("type", "") or "").lower()
            _q   = (_m.get("quality", "") or "").lower()
            _s   = _pref.get(_t, 0)
            _res = _re.search(r"(\d+)x(\d+)", _q)
            if _res:
                _s += int(_res.group(1))
            if _s > _score:
                _score = _s
                _best  = _m
        return _best

    def fetch_multi(url: str) -> dict:
        _raw = _Ω_fetch(url)
        if not _raw["success"]:
            return _raw

        _best_media = _Ω_best(_raw["medias"])
        _dl_url     = _best_media.get("url", "")
        _quality    = _best_media.get("quality", "")
        _mtype      = _best_media.get("type", "")

        return {
            "success":      True,
            "title":        _raw.get("title", ""),
            "author":       _raw.get("author", ""),
            "thumbnail":    "",
            "duration":     0,
            "format":       _mtype,
            "quality":      _quality,
            "filesize_mb":  0.0,
            "download_url": _dl_url,
            "all_medias":   _raw.get("medias", []),
            "error":        None,
        }

    return fetch_multi

fetch_multi = _Ω_exec()

__all__ = ["fetch_multi"]
