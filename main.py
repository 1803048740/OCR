import subprocess
import sys
import webbrowser
import threading
import time
import uvicorn

PORT = 8000


def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    t = threading.Thread(target=open_browser, daemon=True)
    t.start()
    uvicorn.run("backend.app:app", host="0.0.0.0", port=PORT, reload=False)
