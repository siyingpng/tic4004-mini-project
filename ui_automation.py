import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def setup():
    chromedriver_dir = '/Downloads/'
    if os.name == 'posix':  # Unix-based OS (Linux, macOS)
        chromedriver_path = os.path.join(chromedriver_dir, 'chromedriver_mac_arm64/chromedriver')
    elif os.name == 'nt':  # Windows OS
        chromedriver_path = os.path.join(chromedriver_dir, 'chromedriver_win32/chromedriver')
    else:
        raise Exception("Unsupported operating system")

    webdriver.chrome.driver = chromedriver_path
    driver = webdriver.Chrome()
    return driver

def teardown(driver):
    driver.quit()

def test_standard_user_login():
    driver = setup()
    login_url = 'https://www.saucedemo.com'
    driver.get(login_url)

    username_field = driver.find_element(By.ID, 'user-name')
    password_field = driver.find_element(By.ID, 'password')

    username_field.send_keys('standard_user')
    password_field.send_keys('secret_sauce')

    password_field.send_keys(Keys.RETURN)

    assert "inventory.html" in driver.current_url
    print("Test for standard user login succeeded.")

    teardown(driver)

if __name__ == "__main__":
    test_standard_user_login()
