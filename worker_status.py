# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests

BUILDBOT_API = "https://buildbot.python.org/all/api/v2"
WORKER_ID = 120

def get_worker_status():
    try:
        url = f"{BUILDBOT_API}/workers/{WORKER_ID}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        workers = data.get("workers", [])
        
        if not workers:
            return {"status": "not_found", "connected": False}
        
        worker = workers[0]
        connected_to = worker.get("connected_to", [])
        
        return {
            "status": "connected" if connected_to else "disconnected",
            "connected": bool(connected_to),
            "name": worker.get("name", "Unknown")
        }
    except Exception as e:
        return {"status": "error", "connected": False}

def main():
    status_info = get_worker_status()
    
    # Menu bar display
    if status_info["status"] == "connected":
        print("🟢 Buildbot")  # Green circle in menu bar
    elif status_info["status"] == "disconnected":
        print("🔴 Buildbot")  # Red circle in menu bar
    else:
        print("⚠️ Buildbot")  # Warning for error
    
    # Dropdown menu
    print("---")
    print(f"Worker: {status_info.get('name', 'savannah-raspbian')}")
    print(f"Status: {status_info['status']}")
    print("---")
    print(f"View on Web | href=https://buildbot.python.org/all/#/workers/{WORKER_ID}")
    print("Refresh | refresh=true")

if __name__ == "__main__":
    main()