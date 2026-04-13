import os
from config import STATE_TENDER_PORTALS
from browser.chrome_driver import get_chrome_driver
from automation.open_site import open_tender_site
from automation.click_status import click_status
from database.table_manager import ensure_state_table
from Captcha_solver.captcha_predict import CaptchaOCR
import re


BASE_DOWNLOAD_DIR = r"C:\Users\DELL\Desktop\Download_PDF"

def run():
    while True:
        state = input("Enter State Name: ").strip().lower()
        state = re.sub(r"\s+", "_", state)
        state = re.sub(r"[^a-z_]", "", state)

        if state in STATE_TENDER_PORTALS:
            break
        else:
            print("❌ Invalid state.")
            print("Supported states:", ", ".join(STATE_TENDER_PORTALS.keys()), "\n")

    max_download =int(input("How many tender pdfs do you download :"))

    state_table = ensure_state_table(state)

    # 🔑 Create state-specific download folder
    DOWNLOAD_DIR = os.path.join(BASE_DOWNLOAD_DIR, state)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    print(f"📁 Download folder: {DOWNLOAD_DIR}")

    driver = get_chrome_driver(DOWNLOAD_DIR)
    
    ocr = CaptchaOCR(r"C:\Users\DELL\Downloads\main_code\main_code_result\Captcha_solver\captcha_ocr_final.zip")
    open_tender_site(driver, STATE_TENDER_PORTALS[state]["url"],ocr)

    input("➡ After CAPTCHA & Search, press ENTER...")

    click_status(driver, DOWNLOAD_DIR,state,max_download,state_table)

    driver.quit()
    print("✅ Process completed")


if __name__ == "__main__":
    run()
