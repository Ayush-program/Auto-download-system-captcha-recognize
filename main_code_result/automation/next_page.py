from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def click_next_page(driver, timeout=20):
    try:
        next_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "loadNext"))
        )

        driver.execute_script("arguments[0].click();", next_btn)
        print("➡ Clicked NEXT page")

        # wait until page reloads (table refresh)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//tr[contains(@class,'list_header')]")
            )
        )
        return True

    except TimeoutException:
        print("⛔ No NEXT page found")
        return False
