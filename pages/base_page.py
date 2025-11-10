"""
Base Page class with common methods for all pages
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from locators import TestData


class BasePage:
    """Base class to initialize the base page that will be inherited by all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestData.TIMEOUT_MEDIUM)
        self.wait_short = WebDriverWait(driver, TestData.TIMEOUT_SHORT)
        self.wait_long = WebDriverWait(driver, TestData.TIMEOUT_LONG)
        
    def get_element(self, locator, timeout=None):
        """Wait for element to be present in DOM and return it
        I use this method everywhere to avoid hardcoded waits"""
        wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_MEDIUM)
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"Element not found with locator: {locator}")
            return None
    
    def get_visible_element(self, locator, timeout=None):
        """Get element only when its visible on page
        Sometimes element exists in DOM but not visible yet"""
        wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_MEDIUM)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Element not visible: {locator}")
            return None
    
    def get_clickable_element(self, locator, timeout=None):
        """Wait until element is ready to be clicked
        Important for buttons that might be disabled initially"""
        wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_MEDIUM)
        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print(f"Element not clickable: {locator}")
            return None
    
    def click(self, locator, timeout=None):
        """Click element with retry logic
        Sometimes regular click doesnt work so I added JavaScript click as backup"""
        element = self.get_clickable_element(locator, timeout)
        if element:
            try:
                element.click()
                return True
            except ElementNotInteractableException:
                # If normal click fails, try with JavaScript
                self.driver.execute_script("arguments[0].click();", element)
                return True
        return False
    
    def type_text(self, locator, text, clear_first=True, timeout=None):
        """Type text into input field
        Usually we want to clear field first to avoid mixing old and new text"""
        element = self.get_visible_element(locator, timeout)
        if element:
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        return False
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by typing the text
        I found that typing works better than using Select class sometimes"""
        element = self.get_element(locator, timeout)
        if element:
            try:
                select = Select(element)
                select.select_by_visible_text(text)
                return True
            except:
                # Fallback to typing if Select doesnt work
                element.send_keys(text)
                return True
        return False
    
    def get_text(self, locator, timeout=None):
        """Get text content from element"""
        element = self.get_visible_element(locator, timeout)
        return element.text if element else ""
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get any attribute value from element like value, class, id etc"""
        element = self.get_element(locator, timeout)
        return element.get_attribute(attribute) if element else None
    
    def is_element_present(self, locator, timeout=None):
        """Check if element exists in DOM (doesnt have to be visible)"""
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_SHORT)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is actually visible on screen"""
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_SHORT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for loading spinners or popups to disappear"""
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_MEDIUM)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, text, timeout=None):
        """Wait for URL to contain specific text - useful for navigation checks"""
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.TIMEOUT_MEDIUM)
            wait.until(EC.url_contains(text))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element - sometimes elements are not in viewport"""
        element = self.get_element(locator, timeout)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.wait_short.until(lambda driver: True)  # Small wait for scroll
            return True
        return False
    
    def press_key(self, locator, key, timeout=None):
        """Press specific key on element"""
        element = self.get_element(locator, timeout)
        if element:
            element.send_keys(key)
            return True
        return False
    
    def press_enter(self, locator, timeout=None):
        """Press Enter key - useful for form submissions"""
        return self.press_key(locator, Keys.ENTER, timeout)
    
    def take_screenshot(self, filename):
        """Take screenshot for test evidence"""
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved as: {filename}")
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def wait_for_page_load(self):
        """Wait for page to load completely by checking document state"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def close_update_popup(self):
        """Close VarSome update popup that sometimes appears in iframe
        This popup can block our test so we need to handle it"""
        from locators import Locators
        
        time.sleep(2)  # Give popup time to appear
        
        try:
            # Look for iframes since popup might be inside one
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    # Try to find and click close button
                    element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable(Locators.VERSION_POPUP_CLOSE)
                    )
                    
                    if element:
                        element.click()
                        print("Update popup closed successfully")
                        self.driver.switch_to.default_content()
                        time.sleep(1)
                        return True
                except:
                    self.driver.switch_to.default_content()
                    continue
                    
        except:
            self.driver.switch_to.default_content()
        
        return False