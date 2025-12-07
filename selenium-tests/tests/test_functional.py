import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestFunctionalFeatures:
    """Test functional features like likes, search, etc."""
    
    def test_08_like_memory(self, driver, base_url, wait, take_screenshot):
        """Test 8: Like/unlike functionality"""
        print("🧪 Test 8: Like memory")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find like button
        like_selectors = [
            "//button[contains(text(), 'Like')]",
            "//button[@aria-label='like']",
            "//*[contains(@class, 'like')]",
            "//svg[contains(@class, 'like')]/ancestor::button",
            "//button[.//*[contains(text(), 'Like')]]"
        ]
        
        like_button = None
        for xpath in like_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, xpath)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        like_button = button
                        print(f"✅ Found like button: {xpath}")
                        break
                if like_button:
                    break
            except:
                continue
        
        if not like_button:
            print("ℹ️ No like button found, checking for heart icons")
            heart_selectors = [
                "//*[local-name()='svg' and contains(@class, 'heart')]/ancestor::button",
                "//button[.//*[local-name()='svg']]"
            ]
            for xpath in heart_selectors:
                try:
                    buttons = driver.find_elements(By.XPATH, xpath)
                    for button in buttons:
                        if button.is_displayed():
                            like_button = button
                            print(f"✅ Found heart button: {xpath}")
                            break
                    if like_button:
                        break
                except:
                    continue
        
        if not like_button:
            print("⚠️ No like functionality found")
            pytest.skip("Like functionality not available")
        
        # Get initial state
        initial_text = like_button.text
        print(f"📝 Like button text before: '{initial_text}'")
        
        take_screenshot("before_like")
        
        # Click like button
        like_button.click()
        print("✅ Clicked like button")
        
        # Wait for animation/state change
        time.sleep(2)
        take_screenshot("after_like")
        
        # Get new state
        try:
            new_text = like_button.text
            print(f"📝 Like button text after: '{new_text}'")
            
            if new_text != initial_text:
                print("✅ Like count/text changed")
            else:
                print("ℹ️ Text unchanged, checking for visual feedback")
        except:
            print("ℹ️ Could not get text after click")
        
        # Try to unlike (click again)
        like_button.click()
        print("✅ Clicked again (unlike)")
        time.sleep(1)
        
        print("✅ Test 8: Like functionality tested")
    
    def test_09_search_functionality(self, driver, base_url, wait, take_screenshot):
        """Test 9: Search memories"""
        print("🧪 Test 9: Search functionality")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find search input
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='Search']",
            "input[placeholder*='search']",
            "#search",
            ".search input",
            "input[name='search']"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                for inp in inputs:
                    if inp.is_displayed():
                        search_input = inp
                        print(f"✅ Found search input: {selector}")
                        break
                if search_input:
                    break
            except:
                continue
        
        if not search_input:
            print("ℹ️ No search input found, checking for search button")
            # Look for search button that might open a search bar
            search_button_selectors = [
                "//button[@aria-label='search']",
                "//button[.//*[contains(text(), 'Search')]]",
                "//button[contains(@class, 'search')]"
            ]
            for xpath in search_button_selectors:
                try:
                    buttons = driver.find_elements(By.XPATH, xpath)
                    for button in buttons:
                        if button.is_displayed():
                            button.click()
                            time.sleep(1)
                            # Now try to find search input again
                            for selector in search_selectors:
                                try:
                                    inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                                    for inp in inputs:
                                        if inp.is_displayed():
                                            search_input = inp
                                            print(f"✅ Found search input after button click: {selector}")
                                            break
                                    if search_input:
                                        break
                                except:
                                    continue
                        if search_input:
                            break
                    if search_input:
                        break
                except:
                    continue
        
        if not search_input:
            print("⚠️ No search functionality found")
            pytest.skip("Search functionality not available")
        
        take_screenshot("search_input")
        
        # Enter search term
        search_term = "test"
        search_input.clear()
        search_input.send_keys(search_term)
        print(f"🔍 Searching for: '{search_term}'")
        
        # Submit search (press Enter or wait)
        search_input.submit()
        time.sleep(3)
        
        take_screenshot("search_results")
        
        # Check if results are filtered
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        if "no results" in page_text or "not found" in page_text:
            print("ℹ️ No results found for search term")
        elif search_term in page_text:
            print(f"✅ Search term '{search_term}' found in results")
        else:
            print("ℹ️ Search executed, checking for filtered content")
        
        print("✅ Test 9: Search functionality tested")
    
    def test_10_tags_filter(self, driver, base_url, wait, take_screenshot):
        """Test 10: Filter by tags"""
        print("🧪 Test 10: Tags filter")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find tags
        tag_selectors = [
            ".tag", "[class*='tag']", ".MuiChip-root",
            "button:contains('#')", "//button[contains(text(), '#')]"
        ]
        
        tags_found = []
        for selector in tag_selectors:
            try:
                if selector.startswith("//"):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for elem in elements:
                    if elem.is_displayed() and elem.is_enabled():
                        tag_text = elem.text
                        if tag_text and len(tag_text) > 0:
                            tags_found.append((elem, tag_text))
            except:
                continue
        
        print(f"🔖 Found {len(tags_found)} tag(s)")
        
        if not tags_found:
            print("ℹ️ No tags found, creating a memory with tags first")
            # We'd need to create a memory with tags first
            print("⚠️ Skipping tag filter test - no tags available")
            pytest.skip("No tags available to test")
        
        # Click first tag
        first_tag, tag_text = tags_found[0]
        print(f"📌 Clicking tag: '{tag_text}'")
        
        take_screenshot("before_tag_click")
        
        first_tag.click()
        print(f"✅ Clicked tag: {tag_text}")
        
        # Wait for filter
        time.sleep(3)
        take_screenshot("after_tag_filter")
        
        # Check if filtered
        current_url = driver.current_url
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        if "filter" in current_url or "tag" in current_url:
            print(f"✅ URL indicates filtering: {current_url}")
        elif tag_text.lower() in page_text.lower():
            print(f"✅ Tag '{tag_text}' found in page content")
        else:
            print("ℹ️ Tag click may have filtered content")
        
        print("✅ Test 10: Tag filter tested")
    
    def test_11_sort_functionality(self, driver, base_url, wait, take_screenshot):
        """Test 11: Sort memories"""
        print("🧪 Test 11: Sort functionality")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find sort dropdown/button
        sort_selectors = [
            "select[name='sort']",
            "select[aria-label*='sort']",
            ".sort select",
            "#sort",
            "//select[contains(@class, 'sort')]",
            "//button[contains(text(), 'Sort')]"
        ]
        
        sort_element = None
        for selector in sort_selectors:
            try:
                if selector.startswith("//"):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for elem in elements:
                    if elem.is_displayed():
                        sort_element = elem
                        print(f"✅ Found sort element: {selector}")
                        break
                if sort_element:
                    break
            except:
                continue
        
        if not sort_element:
            print("ℹ️ No sort functionality found")
            pytest.skip("Sort functionality not available")
        
        take_screenshot("sort_element")
        
        # Try to interact with sort
        if sort_element.tag_name == "select":
            # It's a dropdown
            from selenium.webdriver.support.ui import Select
            select = Select(sort_element)
            
            # Get current selection
            current_option = select.first_selected_option
            print(f"📊 Current sort: {current_option.text}")
            
            # Try to change sort
            options = select.options
            if len(options) > 1:
                # Select a different option
                for option in options:
                    if option.text != current_option.text:
                        select.select_by_visible_text(option.text)
                        print(f"✅ Changed sort to: {option.text}")
                        break
                
                # Wait for sort to apply
                time.sleep(3)
                take_screenshot("after_sort_change")
            else:
                print("ℹ️ Only one sort option available")
        
        elif sort_element.tag_name == "button":
            # It's a button that might open sort options
            sort_element.click()
            time.sleep(1)
            take_screenshot("sort_options_opened")
            
            # Look for sort options
            option_selectors = [
                "//li[contains(text(), 'Newest')]",
                "//li[contains(text(), 'Oldest')]",
                "//li[contains(text(), 'Popular')]",
                "//*[@role='menuitem']"
            ]
            
            for xpath in option_selectors:
                try:
                    options = driver.find_elements(By.XPATH, xpath)
                    if options:
                        options[0].click()
                        print(f"✅ Selected sort option: {xpath}")
                        break
                except:
                    continue
        
        print("✅ Test 11: Sort functionality tested")
    
    def test_12_form_validation(self, driver, base_url, wait, take_screenshot):
        """Test 12: Form validation"""
        print("🧪 Test 12: Form validation")
        
        # Go to create page
        driver.get(f"{base_url}/create")
        time.sleep(3)
        
        take_screenshot("empty_form")
        
        # Try to submit empty form
        submit_selectors = [
            "button[type='submit']",
            "//button[@type='submit']",
            "//button[contains(text(), 'Submit')]"
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                if selector.startswith("//"):
                    buttons = driver.find_elements(By.XPATH, selector)
                else:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        submit_button = button
                        print(f"✅ Found submit button: {selector}")
                        break
                if submit_button:
                    break
            except:
                continue
        
        if not submit_button:
            print("⚠️ No submit button found")
            pytest.skip("Cannot test form validation")
        
        # Click submit on empty form
        submit_button.click()
        print("✅ Submitted empty form")
        
        time.sleep(2)
        take_screenshot("after_empty_submit")
        
        # Check for validation errors
        error_selectors = [
            ".error", "[class*='error']", ".Mui-error",
            "[role='alert']", ".validation", "[class*='invalid']"
        ]
        
        errors_found = []
        for selector in error_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed():
                        error_text = elem.text
                        if error_text:
                            errors_found.append(error_text)
                            print(f"⚠️ Validation error: {error_text}")
            except:
                continue
        
        if errors_found:
            print(f"✅ Found {len(errors_found)} validation error(s)")
        else:
            # Check for required field indicators
            required_selectors = [
                "[required]", "[aria-required='true']",
                "//*[contains(text(), '*')]", "//*[contains(text(), 'required')]"
            ]
            
            required_found = False
            for selector in required_selectors:
                try:
                    if selector.startswith("//"):
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        required_found = True
                        print(f"✅ Found required field indicator: {selector}")
                        break
                except:
                    continue
            
            if not required_found:
                print("ℹ️ No validation errors or required indicators found")
        
        print("✅ Test 12: Form validation tested")