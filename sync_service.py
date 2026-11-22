import json
import os
import threading
import time
import urllib.request
from datetime import datetime, timezone


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_PATH = os.path.join(BASE_DIR, "sync_sources.json")
METADATA_PATH = os.path.join(DATA_DIR, "sync_metadata.json")

SYNC_LOCK = threading.Lock()


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {"sources": [], "interval_hours": 6}
    with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def atomic_json_write(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def fetch_source(source):
    url = source["url"]
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Bharat-Mitra/1.0 Official-Data-Sync", "Accept": "application/json,text/html,*/*"},
    )
    with urllib.request.urlopen(request, timeout=int(source.get("timeout_seconds", 10))) as response:
        payload = response.read(3 * 1024 * 1024)
        content_type = response.headers.get("Content-Type", "")
        return response.status, content_type, payload


def json_payload(payload):
    try:
        return json.loads(payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def merge_supported_json(source, data):
    target = source.get("target")
    if not target:
        return False

    target_path = os.path.join(DATA_DIR, target)
    incoming = data
    if isinstance(data, dict):
        incoming = data.get(source.get("records_key"))
    if not isinstance(incoming, list) or not incoming:
        return False

    if target == "schemes.json":
        required = {"id", "name", "description"}
        if not all(required.issubset(item.keys()) for item in incoming if isinstance(item, dict)):
            return False

    atomic_json_write(target_path, incoming)
    return True


def sync_now(reason="manual"):
    if not SYNC_LOCK.acquire(blocking=False):
        return {"success": False, "status": "already-running", "message": "A data sync is already in progress."}

    started = utc_now()
    results = []
    updated_targets = set()
    try:
        config = load_config()
        for source in config.get("sources", []):
            result = {
                "name": source["name"],
                "url": source["url"],
                "reachable": False,
                "updated": False,
            }
            try:
                status, content_type, payload = fetch_source(source)
                result["reachable"] = 200 <= status < 400
                if result["reachable"] and "json" in content_type.lower():
                    data = json_payload(payload)
                    if data is not None and merge_supported_json(source, data):
                        target = source["target"]
                        updated_targets.add(target)
                        result["updated"] = True
            except Exception as exc:
                result["error"] = str(exc)
            results.append(result)

        if os.path.exists(os.path.join(DATA_DIR, "schemes.json")):
            with open(os.path.join(DATA_DIR, "schemes.json"), "r", encoding="utf-8") as handle:
                schemes = json.load(handle)
            changed = False
            checked_urls = {r["url"].rstrip("/") for r in results if r["reachable"]}
            today = datetime.now(timezone.utc).strftime("%d %b %Y")
            for scheme in schemes:
                portal = str(scheme.get("portal_url", "")).rstrip("/")
                if portal and portal in checked_urls:
                    scheme["verified_date"] = today
                    scheme["freshness_badge"] = "Live Official Portal Checked"
                    changed = True
            if changed:
                atomic_json_write(os.path.join(DATA_DIR, "schemes.json"), schemes)
                updated_targets.add("schemes.json")

        reachable = sum(1 for result in results if result["reachable"])
        metadata = {
            "last_sync": utc_now(),
            "sync_started": started,
            "reason": reason,
            "success": reachable > 0,
            "sources_checked": len(results),
            "sources_reachable": reachable,
            "updated_targets": sorted(updated_targets),
            "results": results,
        }
        atomic_json_write(METADATA_PATH, metadata)
        return metadata
    finally:
        SYNC_LOCK.release()


def get_sync_status():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return {
        "last_sync": None,
        "success": False,
        "sources_checked": 0,
        "sources_reachable": 0,
        "updated_targets": [],
        "results": [],
    }
