"""
Simple run script for VarSome Test Automation
Makes it easy to run the test - just execute: python run_test.py
"""

import subprocess
import sys
import os


def check_requirements():
    """Check if required packages are installed
    If not, install them automatically"""
    try:
        import selenium
        import webdriver_manager
        print("Required packages found")
        return True
    except ImportError:
        print("Missing required packages")
        print("\nInstalling packages now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])
        print("Packages installed successfully")
        return True


def run_test():
    """Run the main test file"""
    print("\n" + "="*70)
    print(" VarSome Test Automation - Starting Test Run")
    print("="*70)
    print("\nChecking requirements first...")
    
    if not check_requirements():
        return
    
    print("\nStarting test execution...")
    print("-"*70)
    
    # Run the actual test
    result = subprocess.run([sys.executable, "test_germline_variant.py"])
    
    if result.returncode == 0:
        print("\nTest execution completed successfully!")
    else:
        print("\nTest execution failed - check output above for details")
    
    print("="*70)


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nError occured: {e}")
        print("Make sure all files are in correct location")
    
    input("\nPress Enter to exit...")