import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def open_tender_site(driver, url, ocr):

    driver.get(url)
    print("✔ Website opened")

    time.sleep(2)

    # Select AOC option from dropdown
    try:
        dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
        dropdown.select_by_value("6")  # AOC
        print("✔ AOC option selected")
    except Exception as e:
        print("Dropdown selection error:", e)

    while True:
        try:
            # find captcha image
            captcha = driver.find_element(By.ID, "captchaImage")

            # save captcha screenshot
            captcha_path = "temp_captcha.png"
            captcha.screenshot(captcha_path)

            # predict captcha
            captcha_text = ocr.predict(captcha_path)

            print("Predicted captcha:", captcha_text)

            # fill captcha textbox
            captcha_box = driver.find_element(By.ID, "captchaText")
            captcha_box.clear()
            captcha_box.send_keys(captcha_text)
            
            # click search
            driver.find_element(By.ID, "Search").click()

            # wait for result table with id "tabList"
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "tabList"))
                )
                print("✔ Result table loaded")
                break
            except TimeoutException:
                print("❌ CAPTCHA incorrect → retry")

        except Exception as e:
            print("Error:", e)
            time.sleep(2)