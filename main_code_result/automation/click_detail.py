from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def click_detail(driver, timeout=20):
    """
    Finds and clicks the 'View the all stage summary Details' link,
    switches to the popup window,
    and skips if session expired page appears.
    """

    wait = WebDriverWait(driver, timeout)

    main_window = driver.current_window_handle

    # 1️⃣ Find the stage summary link
    stage_link = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//a[starts-with(@id,'DirectLink_') and contains(@title,'stage summary')]"
            )
        )
    )

    # 2️⃣ Click using JavaScript
    driver.execute_script("arguments[0].click();", stage_link)

    # 3️⃣ Wait for popup
    wait.until(lambda d: len(d.window_handles) > 1)

    # 4️⃣ Switch to popup
    driver.switch_to.window(driver.window_handles[-1])

    # ✅ 5️⃣ Check if session expired page loaded
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'session in the client area has expired')]")
            )
        )

        print("⚠ Session expired detected. Skipping this row...")

        # Close popup
        driver.close()

        # Switch back to main window
        driver.switch_to.window(main_window)

        return False   # 🔴 Tell calling function to skip

    except TimeoutException:
        # ✅ No session error — continue normally
       
        return True
