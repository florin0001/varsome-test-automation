"""
ResultsPage Page Object for VarSome variant results page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators import Locators, TestData
import re

class ResultsPage(BasePage):
    """Page Object for Variant Results Page
    This is where we verify the classification results"""
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def wait_for_results_page(self):
        """Wait for results page to load after search
        The page takes some time to load all the data"""
        print("Waiting for results page to load...")
        
        # Check if URL changed to include variant
        url_changed = self.wait_for_url_contains("variant", timeout=TestData.TIMEOUT_LONG)
        # Also check if results container is visible
        page_loaded = self.is_element_visible(Locators.RESULTS_CONTAINER, timeout=TestData.TIMEOUT_LONG)
        
        # Wait for any loading spinners to go away
        self.wait_for_element_to_disappear(Locators.LOADING_SPINNER, timeout=TestData.TIMEOUT_SHORT)
        self.wait_for_element_to_disappear(Locators.LOADING_OVERLAY, timeout=TestData.TIMEOUT_SHORT)
        
        return url_changed or page_loaded
    
    def is_on_results_page(self):
        """Verify we landed on the right page"""
        url = self.get_current_url()
        # Check URL contains variant info
        if "variant" in url.lower() or "braf" in url.lower():
            return True
            
        # Also check for results container element
        return self.is_element_visible(Locators.RESULTS_CONTAINER, timeout=TestData.TIMEOUT_SHORT)
    
    def verify_page_sections(self, print_results=True):
        """Check if all expected sections are present on the page
        Not all sections always load, especially LOVD needs premium access"""
        sections_status = {
            "General Information": self.is_element_visible(Locators.GENERAL_INFO_CARD, timeout=10),
            "Germline Classification": self.is_element_visible(Locators.GERMLINE_CLASSIFICATION_CARD, timeout=10),
            "PharmGKB": self.is_element_visible(Locators.PHARMGKB_CARD, timeout=10),
            "ClinVar": self.is_element_visible(Locators.CLINVAR_CARD, timeout=10),
            "LOVD": self.is_element_visible(Locators.LOVD_CARD, timeout=10),
            "Publications": self.is_element_visible(Locators.PUBLICATIONS_CARD, timeout=10)
        }
        
        if print_results:
            print("Checking page sections:")
            for section, present in sections_status.items():
                status = "[OK]" if present else "[Missing]"
                print(f"  {status} {section}")
            
        return sections_status
    
    def verify_required_sections(self):
        """Check only the critical sections for our test
        Mainly we need Germline Classification section"""
        sections = self.verify_page_sections(print_results=True)
        
        germline_present = sections.get("Germline Classification", False)
        
        if not germline_present:
            print("WARNING: Germline Classification section not found!")
            
        # Note which sections are missing but dont fail test for them
        missing_sections = [name for name, present in sections.items() if not present]
        if missing_sections:
            print(f"Note: Some sections missing: {', '.join(missing_sections)}")
            print("This is normal if you dont have premium access")
            
        return germline_present
    
    def is_germline_classification_visible(self):
        """Quick check if Germline Classification card is visible"""
        return self.is_element_visible(Locators.GERMLINE_CLASSIFICATION_CARD)
    
    def handle_warning_popup(self):
        """Handle 'I understand' warning popup that sometimes appears
        VarSome shows this for clinical interpretation disclaimer"""
        from locators import Locators
        
        if self.is_element_present(Locators.WARNING_UNDERSTAND_BUTTON, timeout=3):
            if self.click(Locators.WARNING_UNDERSTAND_BUTTON):
                print("Handled 'I understand' warning popup")
                self.wait_short.until(lambda driver: True)
                return True
        return False
    
    def expand_germline_classification(self):
        """Click to expand the Germline Classification section
        The section starts collapsed so we need to expand it"""
        print("Expanding Germline Classification section...")
        
        # First scroll to the element
        self.scroll_to_element(Locators.GERMLINE_CLASSIFICATION_CARD)
        import time
        time.sleep(2)  # Wait for scroll animation
        
        # Click using JavaScript to avoid interception issues
        element = self.get_element(Locators.GERMLINE_CLASSIFICATION_CARD)
        if element:
            self.driver.execute_script("arguments[0].click();", element)
            
            # Check if warning popup appears after expanding
            self.handle_warning_popup()
            return True
        
        return False
    
    def get_verdict_text(self):
        """Get the classification verdict text (should be 'Pathogenic')"""
        # Try primary locator first
        verdict_text = self.get_text(Locators.PATHOGENIC_VERDICT)
        if verdict_text:
            return verdict_text
            
        # Try alternative locator if first doesnt work
        verdict_text = self.get_text(Locators.PATHOGENIC_VERDICT_ALT)
        if verdict_text:
            return verdict_text
            
        return None
    
    def get_verdict_color(self):
        """Get the background color of verdict element
        We need to verify its red for Pathogenic classification"""
        element = None
        
        # Find the verdict element
        if self.is_element_present(Locators.PATHOGENIC_VERDICT, timeout=2):
            element = self.get_element(Locators.PATHOGENIC_VERDICT)
        elif self.is_element_present(Locators.PATHOGENIC_VERDICT_ALT, timeout=2):
            element = self.get_element(Locators.PATHOGENIC_VERDICT_ALT)
            
        if element:
            # Get parent element which has the background color
            parent = element.find_element(By.XPATH, "..")
            bg_color = parent.value_of_css_property("background-color")
            
            # Parse RGB values to check if its red
            if bg_color and ("rgb" in bg_color or "rgba" in bg_color):
                # Extract RGB values using regex
                rgb_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', bg_color)
                if rgb_match:
                    r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
                    # Check if color is red (high R, low G and B)
                    if r > 150 and g < 50 and b < 50:
                        return "red"
                return bg_color
        
        return None
    
    def verify_pathogenic_classification(self):
        """Main verification method - check both text and color
        This is the key verification for our test case"""
        print("Verifying classification details...")
        
        # First expand the section
        self.expand_germline_classification()
        self.wait_short.until(lambda driver: True)
        
        # Get and check verdict text
        verdict = self.get_verdict_text()
        is_pathogenic = "pathogenic" in verdict.lower() if verdict else False
        
        # Get and check color
        color = self.get_verdict_color()
        is_red = color == "red" if color else False
        
        # Return all the results
        return {
            "verdict_text": verdict,
            "is_pathogenic": is_pathogenic,
            "color": color,
            "is_red": is_red,
            "success": is_pathogenic and is_red  # Both must be true
        }
    
    def take_verdict_screenshot(self, filename="verdict_screenshot.png"):
        """Take screenshot of verdict section for evidence
        Always good to have proof that test passed"""
        # Scroll to verdict section first
        self.scroll_to_element(Locators.GERMLINE_CLASSIFICATION_CARD)
        self.wait_short.until(lambda driver: True)
        
        # Take the screenshot
        self.take_screenshot(filename)
        return filename