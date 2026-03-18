# automation/download_pdf.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def download_pdf(driver, tender_id, timeout=60):
    wait = WebDriverWait(driver, timeout)

  
    driver.switch_to.window(driver.window_handles[-1])

    # 1️⃣ Find Print button
    try:
        print_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick,'window.print')]")
            )
        )

    except TimeoutException:
        print("⚠ Print button not found, checking iframes...")
        found = False

        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)

                print_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@onclick,'window.print')]")
                    )
                )
                print("🖨 Print button found inside iframe")
                found = True
                break

            except TimeoutException:
                continue

        if not found:
            raise TimeoutException("❌ Print button not found anywhere")

    # 2️⃣ CLICK PRINT (NON-BLOCKING)
    print(f"⬇ Printing tender: {tender_id}")
    print_btn.click()   # 🔑 THIS FIXES SCRIPT TIMEOUT

    # 3️⃣ Give Chrome time to start printing
    time.sleep(1)
