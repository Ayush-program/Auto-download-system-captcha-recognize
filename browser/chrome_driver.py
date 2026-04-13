from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(download_dir):
    options = Options()

    prefs = {
        # ⬇ Normal downloads
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1,

        # 🖨 Print → Save as PDF automatically
        "printing.print_preview_sticky_settings.appState": """
        {
            "recentDestinations":[{"id":"Save as PDF","origin":"local"}],
            "selectedDestinationId":"Save as PDF",
            "version":2
        }
        """,
        "savefile.default_directory": download_dir
    }

    options.add_experimental_option("prefs", prefs)

    # 🔑 THIS LINE AUTO-CLICKS SAVE (CRITICAL)
    options.add_argument("--kiosk-printing")

    # Stability flags (keep yours)
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.maximize_window()
    return driver
