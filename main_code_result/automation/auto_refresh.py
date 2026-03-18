from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def refresh_page(driver, timeout=10, retries=3):
    for attempt in range(1, retries + 1):
        try:
            print(f"🔄 Attempt {attempt}: Checking page...")

            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tr[contains(@class,'list_header')]")
                )
            )

            print("✅ Page already loaded")
            return True

        except:
            print("⚠ Page not loaded. Refreshing...")

            try:
                driver.refresh()
            except Exception as e:
                print("❌ Refresh command failed:", e)

            time.sleep(2)

    print("❌ Page failed to load after retries")
    return False