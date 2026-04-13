from config import STATE_TENDER_PORTALS

def restart_browser(driver, DOWNLOAD_DIR, state):
    print("🔄 Restarting browser...")

    # close old browser safely
    try:
        driver.quit()
    except:
        pass

    # import here to avoid circular imports
    from browser.chrome_driver import get_chrome_driver
    from automation.open_site import open_tender_site

    # create new browser
    driver = get_chrome_driver(DOWNLOAD_DIR)

    # open website
    open_tender_site(driver, STATE_TENDER_PORTALS[state]["url"])

    # manual captcha
    input("👉 Solve CAPTCHA and press ENTER to continue...")

    print("✔ Browser restarted successfully")

    return driver
