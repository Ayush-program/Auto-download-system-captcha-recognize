import os
import time


def rename_pdf(download_dir, original_name, tender_id):
    old_path = os.path.join(download_dir, original_name)
    new_name = f"{tender_id}.pdf"
    new_path = os.path.join(download_dir, new_name)

    # Wait until file is fully downloaded and unlocked
    while True:
        if os.path.exists(old_path) and not old_path.endswith(".crdownload"):
            try:
                with open(old_path, 'rb'):
                    break  # file is ready
            except PermissionError:
                pass
        time.sleep(0.5)

    os.rename(old_path, new_path)
    return new_path
