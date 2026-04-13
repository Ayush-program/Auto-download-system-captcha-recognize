import os

def get_latest_pdf(download_dir):
    files = [
        os.path.join(download_dir, f)
        for f in os.listdir(download_dir)
        if f.lower().endswith(".pdf")
    ]

    if not files:
        return None, None

    latest_pdf = max(files, key=os.path.getmtime)

    return latest_pdf, os.path.basename(latest_pdf)
