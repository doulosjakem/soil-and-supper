#!/usr/bin/env python3
"""
Shared utilities for dataset download adapters.
"""

import hashlib
import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

import requests
import zipfile
import tarfile

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
SUPPORTED_ARCHIVE_EXTENSIONS = {".zip", ".tar.gz", ".tgz", ".tar", ".gz"}
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def compute_sha256(path: Path, chunk_size: int = 8192) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def is_html_or_error(path: Path) -> tuple[bool, Optional[str]]:
    """Check if a file is actually an HTML page or error document instead of an archive/image dataset."""
    if not path.exists() or not path.is_file():
        return False, "File does not exist"

    try:
        with open(path, "rb") as f:
            header = f.read(4096)

        header_lower = header.lower()

        if b"<!doctype html>" in header_lower or b"<html" in header_lower:
            return True, "File is HTML"

        if header[:2] == b"PK":
            return False, None

        if header[:2] == b"\x1f\x8b":
            return False, None

        if header[:4] == b"\x50\x4b\x03\x04":
            return False, None

        if header[:5] == b"%PDF-":
            return False, None

        if path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
            try:
                with open(path, "rb") as f2:
                    prefix = f2.read(16)
                if prefix[:2] in (b"\xff\xd8", b"\x89P"):
                    return False, None
                return True, "File extension suggests image but magic bytes do not match"
            except Exception:
                return True, "Cannot read file"

        if path.suffix.lower() in SUPPORTED_ARCHIVE_EXTENSIONS:
            if header[:2] != b"PK" and header[:2] != b"\x1f\x8b":
                return True, f"Extension suggests archive but magic bytes are {header[:4]!r}"

        return False, None
    except Exception as e:
        return True, f"Error reading file: {e}"


def verify_archive(path: Path) -> Dict[str, Any]:
    """Verify that a path is a valid archive and report its contents."""
    result = {
        "valid": False,
        "file_count": 0,
        "image_count": 0,
        "sample_files": [],
        "error": None,
    }

    if not path.exists():
        result["error"] = "File does not exist"
        return result

    html, reason = is_html_or_error(path)
    if html:
        result["error"] = reason
        return result

    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path, "r") as z:
                names = z.namelist()
                result["valid"] = True
                result["file_count"] = len(names)
                for name in names[:20]:
                    result["sample_files"].append(name)
                    if any(name.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
                        result["image_count"] += 1
                return result
        elif tarfile.is_tarfile(path):
            with tarfile.open(path, "r:*") as t:
                members = t.getmembers()
                result["valid"] = True
                result["file_count"] = len(members)
                for member in members[:20]:
                    result["sample_files"].append(member.name)
                    if any(member.name.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
                        result["image_count"] += 1
                return result
        elif path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
            result["valid"] = True
            result["file_count"] = 1
            result["image_count"] = 1
            return result
        else:
            result["error"] = "Unknown file format"
            return result
    except zipfile.BadZipFile:
        result["error"] = "Bad ZIP file"
        return result
    except tarfile.ReadError:
        result["error"] = "Bad tar file"
        return result
    except Exception as e:
        result["error"] = str(e)
        return result


def download_with_resume(
    url: str,
    dest_path: Path,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 120,
    chunk_size: int = 8192,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Download a file with resume support and detailed metadata."""
    merged_headers = {**DEFAULT_HEADERS}
    if headers:
        merged_headers.update(headers)

    result = {
        "success": False,
        "http_status": None,
        "final_url": None,
        "content_type": None,
        "content_length": 0,
        "actual_size": 0,
        "checksum": None,
        "resumed": False,
        "error": None,
    }

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = dest_path.with_suffix(dest_path.suffix + ".part")

    existing_size = 0
    if temp_path.exists():
        existing_size = temp_path.stat().st_size

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            request_headers = dict(merged_headers)
            if existing_size > 0:
                request_headers["Range"] = f"bytes={existing_size}-"

            session = requests.Session()
            response = session.get(
                url,
                headers=request_headers,
                timeout=timeout,
                stream=True,
                allow_redirects=True,
            )

            result["http_status"] = response.status_code
            result["final_url"] = response.url
            result["content_type"] = response.headers.get("Content-Type", "")
            result["content_length"] = int(response.headers.get("Content-Length", 0))

            if response.status_code in (200, 206):
                mode = "ab" if response.status_code == 206 and existing_size > 0 else "wb"
                result["resumed"] = mode == "ab"

                with open(temp_path, mode) as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            result["actual_size"] += len(chunk)

                if result["actual_size"] > 0:
                    result["success"] = True
                    result["checksum"] = compute_sha256(temp_path)
                    break
            else:
                result["error"] = f"HTTP {response.status_code}"
                if response.status_code in (403, 429, 503):
                    time.sleep(min(2 ** attempt, 30))
                    continue
                break

        except requests.exceptions.RequestException as e:
            result["error"] = f"Request failed: {e}"
            time.sleep(min(2 ** attempt, 30))
        except Exception as e:
            result["error"] = str(e)
            break

    if not result["success"]:
        if temp_path.exists():
            failed_path = temp_path.with_suffix(temp_path.suffix + ".failed")
            temp_path.rename(failed_path)
            result["failed_path"] = str(failed_path)
        return result

    try:
        temp_path.replace(dest_path)
    except OSError:
        if temp_path.exists():
            failed_path = temp_path.with_suffix(temp_path.suffix + ".failed")
            temp_path.rename(failed_path)
            result["failed_path"] = str(failed_path)
        result["success"] = False
        result["error"] = "Failed to move temp file to destination"

    return result


def detect_known_error_page(path: Path) -> Optional[str]:
    """Detect known error page types from file content."""
    if not path.exists():
        return None
    try:
        with open(path, "rb") as f:
            header = f.read(2048)
        header_str = header.decode("utf-8", errors="ignore").lower()
        if "google drive - virus scan warning" in header_str:
            return "Google Drive virus scan warning"
        if "recaptcha" in header_str and "challengepage" in header_str:
            return "Google reCAPTCHA challenge"
        if "404" in header_str and ("not found" in header_str or "page not found" in header_str):
            return "HTTP 404 Not Found"
        if "access denied" in header_str or "forbidden" in header_str:
            return "Access denied / Forbidden"
        if "cloudflare" in header_str and "checking your browser" in header_str:
            return "Cloudflare challenge"
        if "login" in header_str and "sign in" in header_str:
            return "Login / Sign-in page"
        return None
    except Exception:
        return None
