"""
Locators for VarSome Website - All locators in one place for easy maintenance
I keep all locators here so if website changes, I only need to update one file
"""

from selenium.webdriver.common.by import By


class Locators:
    """Central repository for all element locators
    Organized by page section for easy finding"""
    
    # Homepage search elements
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Enter gene') or contains(@placeholder, 'variant')]")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, "input[type='text']:not([type='hidden'])")  # Backup selector
    GENOME_DROPDOWN = (By.XPATH, "//select[@name='genome' or @id='genome']")
    GENOME_DROPDOWN_ALT = (By.CSS_SELECTOR, "select.genome-select, select[data-testid='genome']")
    GENOME_HG38_OPTION = (By.XPATH, "//option[@value='hg38' or contains(text(), 'hg38')]")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), 'Search') or contains(@aria-label, 'Search')]")
    SEARCH_BUTTON_ALT = (By.CSS_SELECTOR, "button[type='submit'], button.search-btn")
    
    # Modal elements
    MODAL_CONTAINER = (By.XPATH, "//form[@tabindex='-1']")  # The modal form
    GERMLINE_TAB = (By.XPATH, "//div[@data-testid='twoStateToggle-left' and contains(text(), 'Germline')]")
    GERMLINE_TAB_ACTIVE = (By.XPATH, "//div[@data-testid='twoStateToggle-left' and contains(@class, 'tw-bg-primary')]")
    
    # Modal form fields - these IDs change sometimes but pattern is consistent
    PHENOTYPE_INPUT = (By.ID, "react-select-2-input")
    SEX_DROPDOWN = (By.ID, "react-select-6-input")
    AGE_INPUT = (By.XPATH, "//div[@id='germline-modal-onset-age']//input[@placeholder]")
    AGE_INPUT_ALT = (By.CSS_SELECTOR, "input[name*='age'], input[placeholder*='age']")
    ETHNICITY_DROPDOWN = (By.ID, "react-select-7-input")
    ETHNICITY_DROPDOWN_ALT = (By.CSS_SELECTOR, "select[name='ethnicity'], select[data-field='ethnicity']")
    
    # Modal buttons
    MODAL_SEARCH_BUTTON = (By.XPATH, "//form//button[2]")  # Second button is search
    MODAL_SEARCH_BUTTON_ALT = (By.CSS_SELECTOR, ".modal-footer button.btn-primary, .modal button[type='submit']")
    
    # Security validation page (sometimes appears)
    SECURITY_PROCEED_BUTTON = (By.ID, "proceedBtn")
    
    # Results page containers
    RESULTS_CONTAINER = (By.CSS_SELECTOR, ".results-container, .variant-page, main")
    
    # Information cards on results page
    GENERAL_INFO_CARD = (By.ID, "variantDetails")
    GERMLINE_CLASSIFICATION_CARD = (By.ID, "acmg")  # Main one we need
    PHARMGKB_CARD = (By.ID, "pharmGKB")
    CLINVAR_CARD = (By.ID, "clinVar")
    LOVD_CARD = (By.ID, "lovd")
    PUBLICATIONS_CARD = (By.ID, "publications")
    
    # Warning popup that sometimes appears
    WARNING_UNDERSTAND_BUTTON = (By.XPATH, "//button[contains(text(), 'I understand')]")
    
    # Classification verdict elements - the key elements we're testing
    PATHOGENIC_VERDICT = (By.XPATH, "//div[contains(@class, 'ColoredPill')]//span[text()='Pathogenic']")
    PATHOGENIC_VERDICT_ALT = (By.XPATH, "//span[text()='Pathogenic']")  # Simpler backup
    
    # Loading indicators to wait for
    LOADING_SPINNER = (By.CSS_SELECTOR, ".spinner, .loading, .loader, [class*='load']")
    LOADING_OVERLAY = (By.CSS_SELECTOR, ".loading-overlay, .busy-indicator")
    
    # Cookie consent popup
    COOKIE_ACCEPT_BUTTON = (By.ID, "onetrust-accept-btn-handler")  # OneTrust cookie banner accept button
    
    # Update popup that sometimes shows
    VERSION_POPUP_CLOSE = (By.ID, "interactive-close-button")


class TestData:
    """Test data values - keeping them separate from code"""
    
    # Website URL
    BASE_URL = "https://varsome.com"
    
    # Variant to test
    VARIANT = "BRAF:V600E"
    GENOME = "hg38"
    
    # Sample information for modal
    PHENOTYPE = "Cancer"
    PHENOTYPE_CODE = "MONDO:0004992"  # This gets selected automatically
    SEX = "Female"
    AGE = "60"
    ETHNICITY = "East Asian"
    
    # Expected results
    EXPECTED_VERDICT = "Pathogenic"
    EXPECTED_COLOR = "red"
    
    # Timeout values in seconds
    TIMEOUT_SHORT = 5
    TIMEOUT_MEDIUM = 10
    TIMEOUT_LONG = 20
    TIMEOUT_EXTRA_LONG = 30