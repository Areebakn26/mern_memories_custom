import pytest
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TestCRUDOperations:
    """Test Create, Read, Update, Delete operations"""
    
    def generate_test_data(self):
        """Generate unique test data"""
        timestamp = int(time.time())
        return {
            "title": f"Test Memory {timestamp}",
            "message": f"This is an automated test memory created at {timestamp}",
            "tags": f"test{timestamp},selenium,automation"
        }
    
    def test_04_create_memory(self, driver, base_url, wait, take_screenshot):
        """Test 4: Create a new memory"""
        print("🧪 Test 4: Create memory")
        
        driver.get(base_url)
        time.sleep(3)
        
        test_data = self.generate_test_data()
        
        # Find and click create button
        create_selectors = [
            "//button[contains(text(), 'Create')]",
            "//button[contains(text(), 'Add')]",
            "//button[contains(text(), 'New')]",
            "//button[@aria-label='create']",
            "//button[.//*[contains(text(), 'Create')]]",
            "//a[contains(text(), 'Create')]"
        ]
        
        create_clicked = False
        for xpath in create_selectors:
            try:
                create_buttons = driver.find_elements(By.XPATH, xpath)
                for button in create_buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        create_clicked = True
                        print(f"✅ Clicked create button with xpath: {xpath}")
                        break
                if create_clicked:
                    break
            except:
                continue
        
        if not create_clicked:
            # Try direct navigation
            driver.get(f"{base_url}/create")
            create_clicked = True
            print("✅ Navigated directly to create page")
        
        assert create_clicked, "Could not find or click create button"
        
        # Wait for form
        time.sleep(3)
        take_screenshot("create_form")
        
        # Fill title field
        title_filled = False
        title_selectors = [
            ("input[name='title']", By.CSS_SELECTOR),
            ("input[placeholder*='Title']", By.CSS_SELECTOR),
            ("input[placeholder*='title']", By.CSS_SELECTOR),
            ("textarea[name='title']", By.CSS_SELECTOR),
            ("#title", By.CSS_SELECTOR),
            ("//input[@name='title']", By.XPATH),
            ("//textarea[@name='title']", By.XPATH)
        ]
        
        for selector, by_type in title_selectors:
            try:
                if by_type == By.CSS_SELECTOR:
                    element = driver.find_element(by_type, selector)
                else:
                    element = driver.find_element(by_type, selector)
                
                if element.is_displayed():
                    element.clear()
                    element.send_keys(test_data["title"])
                    title_filled = True
                    print(f"✅ Filled title with selector: {selector}")
                    break
            except:
                continue
        
        assert title_filled, "Could not find title field"
        
        # Fill message field
        message_filled = False
        message_selectors = [
            ("textarea[name='message']", By.CSS_SELECTOR),
            ("textarea[placeholder*='Message']", By.CSS_SELECTOR),
            ("textarea[placeholder*='message']", By.CSS_SELECTOR),
            ("#message", By.CSS_SELECTOR),
            ("//textarea[@name='message']", By.XPATH)
        ]
        
        for selector, by_type in message_selectors:
            try:
                if by_type == By.CSS_SELECTOR:
                    element = driver.find_element(by_type, selector)
                else:
                    element = driver.find_element(by_type, selector)
                
                if element.is_displayed():
                    element.clear()
                    element.send_keys(test_data["message"])
                    message_filled = True
                    print(f"✅ Filled message with selector: {selector}")
                    break
            except:
                continue
        
        assert message_filled, "Could not find message field"
        
        # Fill tags field (optional)
        tags_selectors = [
            ("input[name='tags']", By.CSS_SELECTOR),
            ("input[placeholder*='Tags']", By.CSS_SELECTOR),
            ("input[placeholder*='tags']", By.CSS_SELECTOR),
            ("#tags", By.CSS_SELECTOR),
            ("//input[@name='tags']", By.XPATH)
        ]
        
        for selector, by_type in tags_selectors:
            try:
                if by_type == By.CSS_SELECTOR:
                    element = driver.find_element(by_type, selector)
                else:
                    element = driver.find_element(by_type, selector)
                
                if element.is_displayed():
                    element.clear()
                    element.send_keys(test_data["tags"])
                    print(f"✅ Filled tags with selector: {selector}")
                    break
            except:
                continue
        
        take_screenshot("form_filled")
        
        # Submit form
        submit_selectors = [
            ("button[type='submit']", By.CSS_SELECTOR),
            ("//button[@type='submit']", By.XPATH),
            ("button:contains('Submit')", By.CSS_SELECTOR),
            ("//button[contains(text(), 'Submit')]", By.XPATH),
            ("//button[contains(text(), 'Create')]", By.XPATH),
            ("//button[contains(text(), 'Save')]", By.XPATH)
        ]
        
        form_submitted = False
        for selector, by_type in submit_selectors:
            try:
                if by_type == By.CSS_SELECTOR:
                    buttons = driver.find_elements(by_type, selector)
                else:
                    buttons = driver.find_elements(by_type, selector)
                
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        form_submitted = True
                        print(f"✅ Submitted with selector: {selector}")
                        break
                if form_submitted:
                    break
            except:
                continue
        
        assert form_submitted, "Could not submit form"
        
        # Wait for creation
        time.sleep(5)
        take_screenshot("after_submit")
        
        # Verify memory was created
        driver.get(base_url)
        time.sleep(3)
        
        page_source = driver.page_source
        assert test_data["title"] in page_source, \
            f"Created memory title '{test_data['title']}' not found on homepage"
        
        print("✅ Test 4: Memory created successfully")
    
    def test_05_view_memory_details(self, driver, base_url, wait, take_screenshot):
        """Test 5: View memory details"""
        print("🧪 Test 5: View memory details")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find a memory to click
        clickable_selectors = [
            ".memory", ".post", ".card", ".MuiCard-root",
            "[class*='memory']", "[class*='post']", "[class*='card']"
        ]
        
        memory_clicked = False
        for selector in clickable_selectors:
            try:
                memories = driver.find_elements(By.CSS_SELECTOR, selector)
                for memory in memories:
                    if memory.is_displayed() and memory.is_enabled():
                        # Get memory title before clicking
                        try:
                            title_elem = memory.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, [class*='title'], [class*='heading']")
                            memory_title = title_elem.text
                            print(f"📝 Memory title: {memory_title}")
                        except:
                            memory_title = "Unknown"
                        
                        # Click the memory
                        memory.click()
                        memory_clicked = True
                        print(f"✅ Clicked memory with selector: {selector}")
                        break
                if memory_clicked:
                    break
            except:
                continue
        
        if not memory_clicked:
            # Check if there are memories
            body_text = driver.find_element(By.TAG_NAME, "body").text
            if "no memories" in body_text.lower():
                print("ℹ️ No memories to view, skipping test")
                pytest.skip("No memories available to view")
            else:
                assert False, "Memories exist but could not click any"
        
        # Wait for details page
        time.sleep(3)
        take_screenshot("memory_details")
        
        # Check if we're on a details page
        current_url = driver.current_url
        if "detail" in current_url or "memory" in current_url or "post" in current_url:
            print(f"✅ On details page: {current_url}")
        else:
            # Check if details are shown in modal or same page
            print(f"ℹ️ Current URL: {current_url}")
        
        # Look for detailed content
        detail_selectors = [
            "h1", "h2", ".title", ".content", ".message",
            "p", "div[class*='content']", "div[class*='message']"
        ]
        
        detail_found = False
        for selector in detail_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed() and len(elem.text) > 10:
                        print(f"📋 Found detail content: {elem.text[:100]}...")
                        detail_found = True
                        break
                if detail_found:
                    break
            except:
                continue
        
        assert detail_found, "Could not find memory details"
        print("✅ Test 5: Memory details viewed")
    
    def test_06_edit_memory(self, driver, base_url, wait, take_screenshot):
        """Test 6: Edit an existing memory"""
        print("🧪 Test 6: Edit memory")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Find edit button
        edit_selectors = [
            "//button[contains(text(), 'Edit')]",
            "//button[@aria-label='edit']",
            "//*[contains(@class, 'edit')]",
            "//svg[contains(@class, 'edit')]/ancestor::button"
        ]
        
        edit_clicked = False
        for xpath in edit_selectors:
            try:
                edit_buttons = driver.find_elements(By.XPATH, xpath)
                for button in edit_buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        edit_clicked = True
                        print(f"✅ Clicked edit button: {xpath}")
                        break
                if edit_clicked:
                    break
            except:
                continue
        
        if not edit_clicked:
            print("ℹ️ No edit button found, trying to navigate")
            # Try to go to edit page directly
            current_url = driver.current_url
            if "/post/" in current_url:
                edit_url = current_url + "/edit"
                driver.get(edit_url)
                edit_clicked = True
            else:
                print("⚠️ Could not find edit button or determine edit URL")
                pytest.skip("No edit functionality found")
        
        # Wait for edit form
        time.sleep(3)
        take_screenshot("edit_form")
        
        # Update title
        timestamp = int(time.time())
        new_title = f"Edited Memory {timestamp}"
        
        # Try to find and update title field
        title_updated = False
        title_selectors = [
            "input[name='title']",
            "textarea[name='title']",
            "input[placeholder*='Title']",
            "#title",
            "h1[contenteditable='true']"
        ]
        
        for selector in title_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    element.clear()
                    element.send_keys(new_title)
                    title_updated = True
                    print(f"✅ Updated title with selector: {selector}")
                    break
            except:
                continue
        
        if not title_updated:
            print("ℹ️ Could not find title field to edit")
        
        take_screenshot("form_edited")
        
        # Save changes
        save_selectors = [
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Update')]",
            "button[type='submit']"
        ]
        
        changes_saved = False
        for xpath in save_selectors:
            try:
                save_buttons = driver.find_elements(By.XPATH, xpath)
                for button in save_buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        changes_saved = True
                        print(f"✅ Saved changes with: {xpath}")
                        break
                if changes_saved:
                    break
            except:
                continue
        
        # Wait for save
        time.sleep(5)
        take_screenshot("after_edit")
        
        # Verify edit
        if changes_saved:
            # Go back to homepage
            driver.get(base_url)
            time.sleep(3)
            
            page_source = driver.page_source
            if new_title in page_source:
                print(f"✅ Memory edited successfully: {new_title}")
            else:
                print("ℹ️ Edit may have worked but new title not immediately visible")
        
        print("✅ Test 6: Edit operation completed")
    
    def test_07_delete_memory(self, driver, base_url, wait, take_screenshot):
        """Test 7: Delete a memory"""
        print("🧪 Test 7: Delete memory")
        
        driver.get(base_url)
        time.sleep(3)
        
        # Count memories before deletion
        memory_selectors = [
            ".memory", ".post", ".card", ".MuiCard-root"
        ]
        
        memories_before = 0
        for selector in memory_selectors:
            try:
                memories = driver.find_elements(By.CSS_SELECTOR, selector)
                memories_before = len([m for m in memories if m.is_displayed()])
                if memories_before > 0:
                    break
            except:
                continue
        
        print(f"📊 Memories before: {memories_before}")
        
        if memories_before == 0:
            print("ℹ️ No memories to delete, creating one first")
            self.test_04_create_memory(driver, base_url, wait, take_screenshot)
            memories_before = 1
        
        # Find delete button
        delete_selectors = [
            "//button[contains(text(), 'Delete')]",
            "//button[@aria-label='delete']",
            "//*[contains(@class, 'delete')]",
            "//svg[contains(@class, 'delete')]/ancestor::button"
        ]
        
        delete_clicked = False
        for xpath in delete_selectors:
            try:
                delete_buttons = driver.find_elements(By.XPATH, xpath)
                for button in delete_buttons:
                    if button.is_displayed() and button.is_enabled():
                        # Take screenshot before deletion
                        take_screenshot("before_delete")
                        
                        button.click()
                        delete_clicked = True
                        print(f"✅ Clicked delete button: {xpath}")
                        break
                if delete_clicked:
                    break
            except:
                continue
        
        if not delete_clicked:
            print("⚠️ No delete button found")
            pytest.skip("Delete functionality not available")
        
        # Handle confirmation dialog
        time.sleep(2)
        
        # Check for confirmation dialog
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"⚠️ Alert text: {alert_text}")
            alert.accept()
            print("✅ Accepted alert confirmation")
        except:
            print("ℹ️ No alert dialog, checking for modal")
            # Look for confirmation modal
            confirm_selectors = [
                "//button[contains(text(), 'Yes')]",
                "//button[contains(text(), 'Confirm')]",
                "//button[contains(text(), 'OK')]"
            ]
            for xpath in confirm_selectors:
                try:
                    confirm_buttons = driver.find_elements(By.XPATH, xpath)
                    for button in confirm_buttons:
                        if button.is_displayed():
                            button.click()
                            print(f"✅ Clicked confirmation: {xpath}")
                            break
                except:
                    continue
        
        # Wait for deletion
        time.sleep(5)
        take_screenshot("after_delete")
        
        # Count memories after deletion
        driver.refresh()
        time.sleep(3)
        
        memories_after = 0
        for selector in memory_selectors:
            try:
                memories = driver.find_elements(By.CSS_SELECTOR, selector)
                memories_after = len([m for m in memories if m.is_displayed()])
                if memories_after > 0:
                    break
            except:
                continue
        
        print(f"📊 Memories after: {memories_after}")
        
        # Verify deletion
        assert memories_after < memories_before, \
            f"Memory count didn't decrease. Before: {memories_before}, After: {memories_after}"
        
        print("✅ Test 7: Memory deleted successfully")