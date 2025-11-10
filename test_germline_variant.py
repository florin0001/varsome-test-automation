"""
Test Case: Verification of Germline Variant Classification for BRAF:V600E
Using Page Object Model Pattern

This is the main test file that runs the actual test scenario
"""

import unittest
from datetime import datetime
from selenium import webdriver
import time
# Import our page objects
from pages.home_page import HomePage
from pages.sample_info_modal import SampleInfoModal
from pages.results_page import ResultsPage

# Import test data
from locators import TestData


class TestGermlineVariantClassification(unittest.TestCase):
    """Test case for verifying BRAF:V600E variant classification
    The requirement is to verify it shows as Pathogenic in red color"""
    
    @classmethod
    def setUpClass(cls):
        """Setup runs once before all tests
        I initialize the driver and page objects here"""
        print("\n" + "="*70)
        print("TEST SUITE: VarSome Germline Variant Classification")
        print("="*70)
        print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*70)
        
        # Setup Chrome with options to avoid detection and popups
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide that its automated
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--log-level=3")  # Reduce console noise
        
        # Initialize Chrome driver - it will auto download chromedriver if needed
        cls.driver = webdriver.Chrome(options=chrome_options)
        
        # Create page objects for each page we'll interact with
        cls.home_page = HomePage(cls.driver)
        cls.modal = SampleInfoModal(cls.driver)
        cls.results_page = ResultsPage(cls.driver)
        
    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests are done"""
        print("\n" + "-"*70)
        input("Press Enter to close browser...")  # Let me see results before closing
        cls.driver.quit()
        print(f"Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def setUp(self):
        """Setup before each test method"""
        self.test_passed = True
        
    def tearDown(self):
        """Cleanup after each test method
        Take screenshot if test fails for debugging"""
        if not self.test_passed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.driver.save_screenshot(f"failure_{timestamp}.png")
            print(f"Failure screenshot saved")
            
    def test_verify_braf_v600e_pathogenic_classification(self):
        """
        Main test case - follows the steps from requirement document:
        1. Launch VarSome Website
        2. Search for BRAF:V600E variant
        3. Fill Optional Sample Information
        4. Verify Results Page loads properly
        5. Expand Germline Classification section
        6. Verify it shows Pathogenic in red color
        """
        
        print("\nTEST: Verification of BRAF:V600E Pathogenic Classification")
        print("-"*70)
        
        try:
            # STEP 1: Launch VarSome Website
            print("\n[STEP 1] Launching VarSome Website")
            success = self.home_page.navigate_to_homepage()
            self.assertTrue(success, "Failed to load VarSome homepage")
            print("Homepage loaded successfully")
            
            # STEP 2: Search for the variant
            print("\n[STEP 2] Starting Variant Search")
            
            # Enter BRAF:V600E in search box
            self.assertTrue(
                self.home_page.enter_variant(TestData.VARIANT),
                "Failed to enter variant in search box"
            )
            print(f"Entered variant: {TestData.VARIANT}")
            
            # Make sure hg38 genome is selected
            self.assertTrue(
                self.home_page.verify_genome_is_hg38(),
                "Could not verify hg38 genome"
            )
            print(f"Genome verified as: {TestData.GENOME}")
            
            # Click search to start
            self.assertTrue(
                self.home_page.click_search(),
                "Failed to click search button"
            )
            print("Search initiated successfully")
            
            # STEP 3: Handle Optional Sample Information Modal
            print("\n[STEP 3] Checking for Optional Sample Information Modal")
            
            # The modal doesnt always appear
            modal_appeared = self.modal.check_if_modal_appears()
            
            if modal_appeared:
                print("Modal appeared - filling sample information")
                
                # Select Germline tab first
                self.assertTrue(
                    self.modal.select_germline_tab(),
                    "Failed to select Germline tab"
                )
                print("Germline tab selected")
                
                # Fill all the fields
                print("Filling patient information:")
                self.modal.fill_phenotype(TestData.PHENOTYPE)
                print(f"  Phenotype: {TestData.PHENOTYPE}")
                
                self.modal.select_sex(TestData.SEX)
                print(f"  Sex: {TestData.SEX}")
                
                self.modal.enter_age(TestData.AGE)
                print(f"  Age: {TestData.AGE}")
                
                self.modal.select_ethnicity(TestData.ETHNICITY)
                print(f"  Ethnicity: {TestData.ETHNICITY}")
                
                print("  Other fields left blank (not required)")
                
                # Submit the modal
                self.assertTrue(
                    self.modal.click_search_in_modal(),
                    "Failed to submit modal"
                )
                print("Modal submitted")
                
                # Wait for it to close
                self.assertTrue(
                    self.modal.wait_for_modal_to_close(),
                    "Modal did not close properly"
                )
                print("Modal closed - proceeding to results")
            else:
                print("No modal appeared - going directly to results")
            
            # Handle security check if it appears
            self.modal.handle_security_validation()
            
            # STEP 4: Verify Results Page
            print("\n[STEP 4] Verifying Results Page")
            
            time.sleep(5)  # Give page time to load all data
            
            # Wait for results to load
            self.assertTrue(
                self.results_page.wait_for_results_page(),
                "Results page did not load"
            )
            print("Results page loaded")
            
            # Verify we're on the right page
            self.assertTrue(
                self.results_page.is_on_results_page(),
                "Not on results page - something went wrong"
            )
            print(f"On results page for: {TestData.VARIANT}")
            
            # Check what sections loaded
            print("\nChecking page sections:")
            sections = self.results_page.verify_page_sections(print_results=True)
            time.sleep(5)  # Let all sections load
            
            # We need at least Germline Classification section
            required_sections = {
                "General Information": sections.get("General Information", False),
                "Germline Classification": sections.get("Germline Classification", False),
                "PharmGKB": sections.get("PharmGKB", False),
                "ClinVar": sections.get("ClinVar", False),
                "LOVD": sections.get("LOVD", False),
                "Publications": sections.get("Publications", False)
            }
            
            # Germline Classification is critical for our test
            self.assertTrue(
                required_sections["Germline Classification"],
                "Germline Classification section missing - cant continue test"
            )
            
            # Note any missing sections but dont fail
            missing_sections = [name for name, present in required_sections.items() if not present]
            if missing_sections:
                print(f"\nNote: Some sections didnt load: {', '.join(missing_sections)}")
                print("Continuing with test anyway...")
            
            # STEP 5: Expand Germline Classification
            print("\n[STEP 5] Expanding Germline Classification Section")
            
            # Verify section is there
            self.assertTrue(
                self.results_page.is_germline_classification_visible(),
                "Germline Classification section not visible"
            )
            print("Found Germline Classification section")
            
            # Click to expand it
            self.assertTrue(
                self.results_page.expand_germline_classification(),
                "Could not expand Germline Classification"
            )
            print("Section expanded successfully")
            
            # STEP 6: Verify Classification Results
            print("\n[STEP 6] Verifying Classification Verdict")
            
            # Get the classification details
            classification = self.results_page.verify_pathogenic_classification()
            
            # Check we got verdict text
            self.assertIsNotNone(
                classification["verdict_text"],
                "Could not find verdict text"
            )
            print(f"Verdict found: {classification['verdict_text']}")
            
            # Verify its Pathogenic
            self.assertTrue(
                classification["is_pathogenic"],
                f"Expected 'Pathogenic' but got '{classification['verdict_text']}'"
            )
            print(f"Verdict correct: {TestData.EXPECTED_VERDICT}")
            
            # Check we can get the color
            self.assertIsNotNone(
                classification["color"],
                "Could not determine verdict color"
            )
            print(f"Color detected: {classification['color']}")
            
            # Verify color is red
            self.assertTrue(
                classification["is_red"],
                f"Expected red color but got '{classification['color']}'"
            )
            print(f"Color correct: {TestData.EXPECTED_COLOR}")
            
            # Take screenshot for proof
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = f"success_pathogenic_{timestamp}.png"
            self.results_page.take_verdict_screenshot(screenshot_file)
            print(f"\nScreenshot saved: {screenshot_file}")
            
            # Final check - both text and color must be right
            self.assertTrue(
                classification["success"],
                "Classification verification failed"
            )
            
            print("\n" + "="*70)
            print("TEST PASSED: BRAF:V600E correctly shows as Pathogenic in red")
            print("="*70)
            
        except AssertionError as e:
            self.test_passed = False
            print(f"\nTEST FAILED: {str(e)}")
            raise
        except Exception as e:
            self.test_passed = False
            print(f"\nUNEXPECTED ERROR: {str(e)}")
            raise


if __name__ == "__main__":
    # Run the test with detailed output
    unittest.main(verbosity=2)