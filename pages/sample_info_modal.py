"""
SampleInfoModal Page Object for Optional Sample Information modal
"""

from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators import Locators, TestData


class SampleInfoModal(BasePage):
    """Page Object for the Optional Sample Information Modal
    This modal appears after search and asks for additional patient info"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def check_if_modal_appears(self):
        """Check if the optional modal shows up
        Sometimes it appears, sometimes it doesnt - depends on previous searches"""
        return self.is_element_visible(Locators.MODAL_CONTAINER, timeout=TestData.TIMEOUT_SHORT)
    
    def select_germline_tab(self):
        """Select Germline tab in the modal
        We need germline for our test case, not somatic"""
        # Check if already on Germline tab
        if self.is_element_visible(Locators.GERMLINE_TAB_ACTIVE, timeout=2):
            print("Germline tab is already selected")
            return True
            
        # Click to select Germline tab
        return self.click(Locators.GERMLINE_TAB)
    
    def fill_phenotype(self, phenotype_text):
        """Fill phenotype field - it has autocomplete functionality
        Need to type and then select from dropdown"""
        if not self.type_text(Locators.PHENOTYPE_INPUT, phenotype_text):
            print("Could not type in phenotype field")
            return False
            
        # Handle autocomplete dropdown
        element = self.get_element(Locators.PHENOTYPE_INPUT)
        if element:
            self.wait_short.until(lambda driver: True)  # Wait for dropdown
            element.send_keys(Keys.ARROW_DOWN)  # Select first option
            self.wait_short.until(lambda driver: True)
            element.send_keys(Keys.ENTER)
            return True
        return False
    
    def select_sex(self, sex_value):
        """Select sex from dropdown using keyboard navigation
        I found keyboard navigation more reliable than Select class here"""
        if not self.click(Locators.SEX_DROPDOWN):
            print(f"Could not open sex dropdown")
            return False
        
        element = self.get_element(Locators.SEX_DROPDOWN)
        if element:
            element.send_keys(sex_value)  # Type the value
            self.wait_short.until(lambda driver: True)
            element.send_keys(Keys.ENTER)  # Select it
            return True
            
        return False
    
    def enter_age(self, age_value):
        """Enter age at onset - simple text field"""
        if not self.type_text(Locators.AGE_INPUT, str(age_value)):
            # Try alternative locator if first one fails
            return self.type_text(Locators.AGE_INPUT_ALT, str(age_value))
        return True
    
    def select_ethnicity(self, ethnicity_value):
        """Select ethnicity from dropdown
        Similar approach as sex dropdown"""
        if not self.click(Locators.ETHNICITY_DROPDOWN):
            print(f"Could not open ethnicity dropdown")
            return False
        
        element = self.get_element(Locators.ETHNICITY_DROPDOWN)
        if element:
            element.send_keys(ethnicity_value)
            self.wait_short.until(lambda driver: True)
            element.send_keys(Keys.ENTER)
            return True
            
        return False
    
    def click_search_in_modal(self):
        """Click Search button inside the modal to submit the form"""
        if not self.click(Locators.MODAL_SEARCH_BUTTON):
            # Try alternative button if first one doesnt work
            return self.click(Locators.MODAL_SEARCH_BUTTON_ALT)
        return True
    
    def wait_for_modal_to_close(self):
        """Wait for modal to disappear after submitting"""
        return self.wait_for_element_to_disappear(Locators.MODAL_CONTAINER, 
                                                  timeout=TestData.TIMEOUT_MEDIUM)
    
    def handle_security_validation(self):
        """Handle security validation page if it appears
        Sometimes VarSome shows a security check"""
        import time
        from locators import Locators
        
        if self.is_element_present(Locators.SECURITY_PROCEED_BUTTON, timeout=5):
            if self.click(Locators.SECURITY_PROCEED_BUTTON):
                print("Security validation handled - proceeding")
                time.sleep(5)  # Wait for page to load after security check
                return True
        
        return False
    
    def fill_sample_information(self, phenotype, sex, age, ethnicity):
        """Fill all the sample information fields at once
        This is a helper method to fill everything in one go"""
        success = True
        
        print("Filling sample information form...")
        
        if not self.select_germline_tab():
            print("Warning: Could not select Germline tab")
            success = False
        
        if not self.fill_phenotype(phenotype):
            print(f"Warning: Issue with phenotype field: {phenotype}")
            success = False
        else:
            print(f"  Phenotype: {phenotype}")
        
        if not self.select_sex(sex):
            print(f"Warning: Issue with sex field: {sex}")
            success = False
        else:
            print(f"  Sex: {sex}")
        
        if not self.enter_age(age):
            print(f"Warning: Issue with age field: {age}")
            success = False
        else:
            print(f"  Age at onset: {age}")
        
        if not self.select_ethnicity(ethnicity):
            print(f"Warning: Issue with ethnicity field: {ethnicity}")
            success = False
        else:
            print(f"  Ethnicity: {ethnicity}")
        
        return success