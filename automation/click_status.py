from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.click_detail import click_detail
from automation.wait_for_dow import wait_for_download
from automation.get_file import get_latest_pdf
from automation.download_pdf import download_pdf
from automation.next_page import click_next_page
from automation.rename_pdf import rename_pdf
from automation.restart_browser import restart_browser
from automation.auto_refresh import refresh_page

from database.check_exists import tender_exists
from database.save_to_db import save_pdf_data


import os
import traceback
import re



def get_total_records(driver, timeout=20):
    text = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//b[contains(text(),'Total records')]")
        )
    ).text

    # Extract number (168)
    total = int(re.search(r"\d+", text).group())
    return total


def click_status(driver,DOWNLOAD_DIR,state,max_download,table_name):

    wait = WebDriverWait(driver, 40)

    index = 0
    page_no = 1
    download_count = 0
    skip_count = 0
    reload_page = False
    session_expired_count = 0



    total_records = get_total_records(driver)
    print(f"📊 TOTAL TENDERS AVAILABLE: {total_records}")

    while True:
        try:

            if reload_page:
                wait = WebDriverWait(driver, 40)
                reload_page = False
                continue

            # ✅ WAIT FOR LIST PAGE SIGNAL (HEADER ROW)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tr[contains(@class,'list_header')]")
                )
            )

            rows = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//tbody/tr[@class='even' or @class='odd']")
                )
            )

            

            print(f"\n📄 PAGE NO: {page_no}")
            print(f"🔎 Tender on this page: {len(rows)}")

            if index >= len(rows):
                print("📄 Page completed, checking for NEXT...")

                has_next = click_next_page(driver)

                if not has_next:
                    print("✅ No more pages. All tenders processed.")
                    break
                # new page loaded
                page_no += 1
                index = 0
                continue

            row = rows[index]
            tds = row.find_elements(By.TAG_NAME, "td")

            if len(tds) < 2:
                print(f"⚠️ Row {index} malformed, skipping")
                index += 1
                continue

            tender_id = tds[1].text.strip()
            print(f"⬇⬇⬇ Processing row {index+1} ⬇⬇⬇| {tender_id}")

            if tender_exists(tender_id,table_name):
                print(f"⏭ Skipping already-downloaded tender | {tender_id}")
                skip_count += 1
                index += 1
                continue

            view_link = row.find_element(
                By.XPATH, ".//a[contains(@title,'View Tender Status')]"
            )

            driver.execute_script("arguments[0].click();", view_link)

            opened = click_detail(driver)

            if not opened:
                session_expired_count +=1

                index += 1

                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@title='Back']"))
                    ).click()
                continue   # Skip this row safely

            download_pdf(driver, tender_id)
            
            wait_for_download(DOWNLOAD_DIR)

            pdf_path, pdf_name = get_latest_pdf(DOWNLOAD_DIR)

            if not pdf_path or not pdf_name:
                print(f"❌ PDF not found for {tender_id}, skipping save")
                index += 1
                continue

            final_path = rename_pdf(DOWNLOAD_DIR, pdf_name, tender_id)

            if not final_path or not os.path.exists(final_path):
                print(f"❌ Rename failed for {tender_id}")
                index += 1
                continue

            save_pdf_data(
                tender_id=tender_id,
                pdf_path=final_path,
                state=state,
                table_name=table_name
            )

            download_count += 1

            # 🔑 CLOSE POPUP & GO BACK
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # ✅ HARD NAVIGATION BACK (NO CLICK)
            WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Back']"))
            ).click()

            # ✅ WAIT UNTIL LIST PAGE IS REALLY BACK
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//tr[contains(@class,'list_header')]/td[2]"),
                    "Tender ID"
                )
            ) 

            index += 1
            print("\n" + "=" * 60)

            if download_count == max_download :
                print(f"Dowload and save your {download_count} pdfs.")
                break

        except Exception as e:
            print("\n❌ ERROR OCCURRED")
            print(e)
            traceback.print_exc()
            print("⚡ Attempting automatic recovery...")

            # 1️⃣ auto refresh attempt
            if refresh_page(driver):
                print("♻ Auto recovery successful. Continuing...\n")
                continue

            # 2️⃣ manual refresh
            print("❌ Auto recovery failed.")
            input("Please refresh manually and press Enter :")

            # 3️⃣ check again after manual refresh
            if refresh_page(driver):
                print("♻ Manual recovery successful. Continuing...\n")
                continue
            else :       
                # 4️⃣ BOTH FAILED → show menu
                print("\n❌ Recovery failed.")
                print("What do you want to do?")
                print("1️⃣ New Start")
                print("2️⃣ Continue")
                print("3️⃣ End")

                choice = input("Choose (1/2/3): ").strip()

                if choice == "1":
                    print("🔄 New start selected")
                    driver = restart_browser(driver, DOWNLOAD_DIR, state)
                    wait = WebDriverWait(driver, 40)

                    index = 0
                    page_no = 1
                    skip_count = 0
                    download_count = 0
                    force_new_start = True
                    continue

                elif choice == "2":
                    print("▶ Continue selected")
                    driver = restart_browser(driver, DOWNLOAD_DIR, state)
                    wait = WebDriverWait(driver, 40)

                    index = 0
                    page_no = 1
                    reload_page = True
                    continue

                else:
                    print("👋 Program ended safely")
                    break
                
    print("\n" + "=" * 50)
    print("📊 FINAL SUMMARY")
    print(f"📥 PDFs downloaded: {download_count}")
    print(f"⏭ PDFs skipped (already exist): {skip_count}")
    print(f"🔄 Session expired detected: {session_expired_count}")
    print(f"📊 Total processed: {download_count + skip_count}")
    print("=" * 50)


