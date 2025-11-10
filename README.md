# VarSome Test Automation

Selenium-based test automation for verifying BRAF:V600E variant classification on VarSome.

## Test Objective

Verify that BRAF:V600E (hg38) is correctly classified as "Pathogenic" with red color indicator.

## Project Structure

```
varsome-test-automation/
├── test_germline_variant.py    # Main test case
├── base_page.py                # Base page with common methods
├── home_page.py                # Homepage interactions
├── results_page.py             # Results page verification
├── sample_info_modal.py        # Modal form handling
├── locators.py                 # Element locators & test data
├── requirements.txt            # Dependencies
└── run_test.py                 # Test runner
```

## Setup

### Prerequisites
- Python 3.7 or higher
- Google Chrome browser (latest version)
- Git

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/florin0001/varsome-test-automation.git
cd varsome-test-automation
```

2. **Create virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python --version
pip list
```
ChromeDriver will be automatically downloaded and managed by Selenium.
## Run Test

```bash
python test_germline_variant.py
```

or

```bash
python run_test.py
```

## Requirements

- Python 3.7+
- Chrome browser
- Internet connection

## Test Data

- Variant: BRAF:V600E
- Genome: hg38
- Phenotype: Cancer
- Sex: Female
- Age: 60
- Ethnicity: East Asian

## Implementation Notes

- Page Object Model design pattern
- Explicit waits
- Centralized locators
- Handles cookie popups, iframes, and dynamic content
- Screenshots on test completion

## Known Issues

- VarSome free tier: 1 request per day limit
- Some sections require premium access

## Troubleshooting

**Module not found error:**
```bash
pip install -r requirements.txt
```

**ChromeDriver issues:**
- Ensure Chrome browser is installed and updated
- Selenium 4+ automatically manages ChromeDriver

**Test fails at cookie popup:**
- Clear browser cache and cookies
- Restart the test

**Rate limit error:**
- Wait 24 hours between test runs on free tier
- Or create a VarSome account for more requests

## Status

✓ Test passing - successfully verifies Pathogenic classification
