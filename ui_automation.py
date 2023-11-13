import os
import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver():
    chromedriver_dir = '/Downloads/'
    if os.name == 'posix':  # Unix-based OS (Linux, macOS)
        chromedriver_path = os.path.join(chromedriver_dir, 'chromedriver_mac_arm64/chromedriver')
    elif os.name == 'nt':  # Windows OS
        chromedriver_path = os.path.join(chromedriver_dir, 'chromedriver_win32/chromedriver')
    else:
        raise Exception("Unsupported operating system")

    webdriver.chrome.driver = chromedriver_path
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def login_url():
    return 'https://www.saucedemo.com/'

def test_invalid_username(driver, login_url):
    driver.get(login_url)

    try:
        driver.find_element(By.ID, 'user-name').send_keys('invalid_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        actual_error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        expected_error_message = "Epic sadface: Username and password do not match any user in this service"
        assert actual_error_message == expected_error_message, f"Expected error message: '{expected_error_message}', but got: '{actual_error_message}'"
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

def test_valid_login(driver, login_url):
    driver.get(login_url)

    try:
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        assert "inventory.html" in driver.current_url, f"Expected URL to contain 'inventory.html' but got '{driver.current_url}' instead."
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

def test_empty_shopping_cart(driver, login_url):
    driver.get(login_url)

    try:
        # login
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        # go to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        assert "cart.html" in driver.current_url

        # checkout
        driver.find_element(By.ID, 'checkout').click()
        assert "checkout-step-one.html" in driver.current_url

        # enter checkout info
        driver.find_element(By.ID, 'first-name').send_keys('Harry')
        driver.find_element(By.ID, 'last-name').send_keys('Potter')
        driver.find_element(By.ID, 'postal-code').send_keys('123456')
        driver.find_element(By.ID, 'continue').click()
        assert "checkout-step-two.html" in driver.current_url

        # complete checkout
        driver.find_element(By.ID, 'finish').click()

        actual_error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        expected_error_message = "Error: The cart cannot be empty"
        assert actual_error_message == expected_error_message, f"Expected error message: '{expected_error_message}', but got: '{actual_error_message}'"
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

def test_checkout(driver, login_url):
    driver.get(login_url)

    try:
        # login
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        # add item to cart
        driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack').click()
        assert driver.find_element(By.ID, 'remove-sauce-labs-backpack').is_displayed()

        # go to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        assert "cart.html" in driver.current_url

        # checkout
        driver.find_element(By.ID, 'checkout').click()
        assert "checkout-step-one.html" in driver.current_url

        # enter checkout info
        driver.find_element(By.ID, 'first-name').send_keys('Harry')
        driver.find_element(By.ID, 'last-name').send_keys('Potter')
        driver.find_element(By.ID, 'postal-code').send_keys('123456')
        driver.find_element(By.ID, 'continue').click()
        assert "checkout-step-two.html" in driver.current_url

        # complete checkout
        driver.find_element(By.ID, 'finish').click()
        assert "checkout-complete.html" in driver.current_url, f"Expected URL to contain 'checkout-complete.html' but got '{driver.current_url}' instead."
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

def test_empty_postal_code(driver, login_url):
    driver.get(login_url)

    try:
        # login
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        # add item to cart
        driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack').click()
        assert driver.find_element(By.ID, 'remove-sauce-labs-backpack').is_displayed()

        # go to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        assert "cart.html" in driver.current_url

        # checkout
        driver.find_element(By.ID, 'checkout').click()
        assert "checkout-step-one.html" in driver.current_url

        # enter checkout info
        driver.find_element(By.ID, 'first-name').send_keys('Harry')
        driver.find_element(By.ID, 'last-name').send_keys('Potter')
        driver.find_element(By.ID, 'continue').click()

        actual_error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        expected_error_message = "Error: Postal Code is required"
        assert actual_error_message == expected_error_message, f"Expected error message: '{expected_error_message}', but got: '{actual_error_message}'"
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

def test_logout(driver, login_url):
    driver.get(login_url)

    try:
        # login
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce', Keys.RETURN)

        # logout
        driver.find_element(By.ID, 'react-burger-menu-btn').click()
        time.sleep(2)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        assert driver.current_url == login_url, f"Expected '{login_url}' but got '{driver.current_url}' instead."
    except NoSuchElementException as e:
        pytest.fail(f"No such element: {e}")

if __name__ == "__main__":
    pytest.main()
