import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestHomepage:
    """Test homepage functionality"""
    
    def test_01_homepage_loads(self, driver, base_url, wait, take_screenshot):
        """Test 1: Homepage loads successfully"""
        print("🧪 Test 1: Homepage loads")
        
        driver.get(base_url)
        
        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)  # Extra time for React
        
        # Take screenshot
        take_screenshot("homepage_loaded")
        
        # Check page content
        page_source = driver.page_source.lower()
        assert "memories" in page_source or "memory" in page_source, \
            f"Page should contain 'memories'. Content: {page_source[:500]}"
        
        print("✅ Test 1: Homepage loaded successfully")
    
    def test_02_navigation_bar_exists(self, driver, base_url, wait, take_screenshot):
        """Test 2: Navigation bar is present"""
        print("🧪 Test 2: Navigation bar check")
        
        driver.get(base_url)
        time.sleep(2)
        
        # Look for navigation elements
        nav_selectors = [
            "nav", "header", ".navbar", ".appbar", 
            "[role='navigation']", ".MuiAppBar-root"
        ]
        
        nav_found = False
        for selector in nav_selectors:
            try:
                if selector.startswith(".") or selector.startswith("["):
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                else:
                    elements = driver.find_elements(By.TAG_NAME, selector)
                
                if elements:
                    nav_found = True
                    print(f"✅ Found navigation with selector: {selector}")
                    break
            except:
                continue
        
        take_screenshot("navigation_bar")
        
        # Check for logo/title
        logo_selectors = [
            "h1", "h2", ".logo", ".title", ".MuiTypography-h4",
            "[class*='logo']", "[class*='title']"
        ]
        
        logo_found = False
        for selector in logo_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.text:
                        logo_found = True
                        print(f"✅ Found logo/title: {element.text[:50]}")
                        break
            except:
                continue
        
        assert nav_found or logo_found, "No navigation or title found"
        print("✅ Test 2: Navigation/Title present")
    
    def test_03_memories_displayed(self, driver, base_url, wait, take_screenshot):
        """Test 3: Memories are displayed on homepage"""
        print("🧪 Test 3: Memories displayed")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Look for memory cards/posts
        memory_selectors = [
            ".memory", ".post", ".card", ".MuiCard-root",
            "[class*='memory']", "[class*='post']", "[class*='card']",
            "article", "section"
        ]
        
        memories_found = []
        for selector in memory_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for elem in elements:
                        if elem.is_displayed() and elem.size['width'] > 0:
                            memories_found.append(elem)
            except:
                continue
        
        take_screenshot("memories_displayed")
        
        if memories_found:
            print(f"✅ Found {len(memories_found)} memory card(s)")
            assert True
        else:
            # Check if there's a "No memories" message
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            if "no memories" in page_text or "create your first" in page_text:
                print("ℹ️ No memories found (fresh app)")
                assert True
            else:
                print("⚠️ No memories found and no 'no memories' message")
                assert False, "Should display memories or 'no memories' message"
        
        print("✅ Test 3: Memories display check passed")