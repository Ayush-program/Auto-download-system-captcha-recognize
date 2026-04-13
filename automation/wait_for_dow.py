# automation/wait_for_dow.py
import os
import time

def wait_for_download(download_dir, timeout=60):
    end = time.time() + timeout

    while time.time() < end:
        files = os.listdir(download_dir)

        downloading = any(f.endswith(".crdownload") for f in files)
        pdfs = [f for f in files if f.endswith(".pdf")]

        if pdfs and not downloading:
            return True

        time.sleep(0.5)

    raise TimeoutError("❌ PDF download did not complete")
