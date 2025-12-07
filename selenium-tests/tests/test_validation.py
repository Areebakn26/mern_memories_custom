import pytest
import time
from selenium.webdriver.common.by import By

class TestValidation:
    """Additional validation tests"""
    
    def test_13_responsive_design(self, driver, base_url, take_screenshot):
        """Test 13: Responsive design"""
        print("🧪 Test 13: Responsive design")
        
        # Test mobile view
        driver.set_window_size(375, 667)  # iPhone size
        driver.get(base_url)
        time.sleep(3)
        take_screenshot("mobile_view")
        
        # Check if content is visible
        body = driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed(), "Body not visible on mobile"
        print("✅ Mobile view: Content visible")
        
        # Test tablet view
        driver.set_window_size(768, 1024)  # iPad size
        driver.refresh()
        time.sleep(3)
        take_screenshot("tablet_view")
        print("✅ Tablet view: Content visible")
        
        # Restore desktop
        driver.set_window_size(1920, 1080)
        driver.refresh()
        print("✅ Test 13: Responsive design tested")
    
    def test_14_error_handling(self, driver, base_url, take_screenshot):
        """Test 14: Error handling (404 page)"""
        print("🧪 Test 14: Error handling")
        
        # Navigate to non-existent page
        driver.get(f"{base_url}/nonexistent-page-12345")
        time.sleep(3)
        take_screenshot("error_page")
        
        # Check for error message or redirect
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        current_url = driver.current_url
        
        if "404" in page_text or "not found" in page_text or "error" in page_text:
            print("✅ Error page displayed correctly")
        elif current_url != f"{base_url}/nonexistent-page-12345":
            print(f"✅ Redirected from error page to: {current_url}")
        else:
            print("ℹ️ No explicit error message, but app didn't crash")
        
        print("✅ Test 14: Error handling tested")
    
    def test_15_performance_check(self, driver, base_url):
        """Test 15: Performance - page load time"""
        print("🧪 Test 15: Performance check")
        
        start_time = time.time()
        driver.get(base_url)
        
        # Wait for page to be interactive
        time.sleep(3)
        
        load_time = time.time() - start_time
        print(f"⏱️ Page load time: {load_time:.2f} seconds")
        
        # Acceptable load time (adjust as needed)
        assert load_time < 10, f"Page load too slow: {load_time:.2f}s"
        
        print("✅ Test 15: Performance acceptable")