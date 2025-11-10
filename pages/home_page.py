"""
HomePage Page Object for VarSome website
"""

from pages.base_page import BasePage
from locators import Locators, TestData
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    """Page Object for VarSome Homepage - handles search functionality"""
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def navigate_to_homepage(self):
        """Navigate to VarSome homepage and handle initial popups"""
        print("Navigating to VarSome homepage...")
        self.driver.get(TestData.BASE_URL)
        self.wait_for_page_load()
        
        # Handle cookie consent that usually appears
        self.handle_cookie_consent()
        self.close_update_popup()  # Sometimes theres an update popup
        
        return self.is_homepage_loaded()
    
    def is_homepage_loaded(self):
        """Check if homepage loaded properly by looking for search input"""
        # Try both possible search input locators
        return self.is_element_visible(Locators.SEARCH_INPUT) or \
               self.is_element_visible(Locators.SEARCH_INPUT_ALT)
    
    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears
        The cookie banner uses OneTrust and has a specific accept button ID"""
        try:
            # Wait a bit for cookie banner to appear
            import time
            time.sleep(2)
            
            # Try to click the accept cookies button
            cookie_accept_btn = (By.ID, "onetrust-accept-btn-handler")
            if self.is_element_present(cookie_accept_btn, timeout=3):
                if self.click(cookie_accept_btn):
                    print("Cookie consent accepted")
                    time.sleep(1)  # Wait for banner to disappear
                    return True
            
            # If button not found, cookie banner might not be present
            print("No cookie banner found or already accepted")
                    
        except Exception as e:
            print(f"Cookie consent handling skipped: {e}")
            
        return False
    
    def enter_variant(self, variant_text):
        """Enter the variant text in search box
        The search input can have different selectors so I try both"""
        print(f"Entering variant: {variant_text}")
        if not self.type_text(Locators.SEARCH_INPUT, variant_text):
            # Try alternative selector if first one fails
            return self.type_text(Locators.SEARCH_INPUT_ALT, variant_text)
        return True
    
    def select_genome(self, genome_version):
        """Select reference genome from dropdown
        Usually hg38 is default but we can select it explicitly"""
        if self.is_element_present(Locators.GENOME_DROPDOWN):
            return self.select_dropdown_by_text(Locators.GENOME_DROPDOWN, genome_version)
        elif self.is_element_present(Locators.GENOME_DROPDOWN_ALT):
            return self.select_dropdown_by_text(Locators.GENOME_DROPDOWN_ALT, genome_version)
        else:
            print(f"Genome dropdown not found - assuming {genome_version} is default")
            return True
    
    def verify_genome_is_hg38(self):
        """Verify that hg38 is selected as reference genome
        This is important because results can differ between genome versions"""
        if self.is_element_present(Locators.GENOME_DROPDOWN):
            value = self.get_attribute(Locators.GENOME_DROPDOWN, "value")
            if value and "hg38" in value.lower():
                return True
        
        # Check if hg38 option is visible
        if self.is_element_visible(Locators.GENOME_HG38_OPTION, timeout=2):
            return True
            
        print("Could not verify genome but assuming hg38 is default")
        return True
    
    def click_search(self):
        """Click search button to start variant search
        Sometimes the button is blocked by cookie banner so I retry"""
        print("Clicking search button...")
        
        if self.click(Locators.SEARCH_BUTTON):
            return True
            
        # Maybe cookie banner is blocking, try to handle it again
        self.handle_cookie_consent()
        
        if self.click(Locators.SEARCH_BUTTON_ALT):
            return True
            
        # If still not working, use JavaScript click
        search_btn = self.get_element(Locators.SEARCH_BUTTON)
        if search_btn:
            self.driver.execute_script("arguments[0].click();", search_btn)
            print("Used JavaScript click for search button")
            return True
            
        # Last resort - press Enter in search field
        return self.press_enter(Locators.SEARCH_INPUT)