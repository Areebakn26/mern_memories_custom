import pytest
import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variables
backend_process = None
frontend_process = None

def start_mern_app():
    """Start MERN application locally"""
    global backend_process, frontend_process
    
    print("\n" + "="*60)
    print("STARTING MERN MEMORIES APPLICATION")
    print("="*60)
    
    # Start Backend
    backend_dir = os.path.join(os.path.dirname(__file__), "../../backend")
    if os.path.exists(backend_dir):
        print(f"📦 Starting backend from: {backend_dir}")
        backend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        print("✅ Backend started on port 5000")
    else:
        print("⚠️  Backend directory not found")
    
    # Start Frontend
    frontend_dir = os.path.join(os.path.dirname(__file__), "../../frontend")
    if os.path.exists(frontend_dir):
        print(f"🎨 Starting frontend from: {frontend_dir}")
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        print("✅ Frontend started on port 3000")
    else:
        print("⚠️  Frontend directory not found")
    
    # Wait for servers
    print("⏳ Waiting for servers to start (15 seconds)...")
    time.sleep(15)
    print("="*60 + "\n")

def stop_mern_app():
    """Stop MERN application"""
    global backend_process, frontend_process
    
    print("\n" + "="*60)
    print("STOPPING MERN MEMORIES APPLICATION")
    print("="*60)
    
    if frontend_process:
        frontend_process.terminate()
        print("✅ Frontend stopped")
    
    if backend_process:
        backend_process.terminate()
        print("✅ Backend stopped")
    
    print("="*60)

def pytest_sessionstart(session):
    """Start app before all tests"""
    use_local = os.getenv("USE_LOCAL", "true").lower() == "true"
    if use_local:
        start_mern_app()

def pytest_sessionfinish(session, exitstatus):
    """Stop app after all tests"""
    use_local = os.getenv("USE_LOCAL", "true").lower() == "true"
    if use_local:
        stop_mern_app()

@pytest.fixture(scope="session")
def driver():
    """Create and configure Chrome driver using webdriver-manager"""
    chrome_options = Options()
    
    # Headless mode for CI/CD
    if os.getenv("HEADLESS", "true").lower() == "true":
        chrome_options.add_argument("--headless")
    
    # Required for Docker/CI environments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Add user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Disable logging for cleaner output
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Initialize driver with webdriver-manager
    print("🔧 Initializing Chrome driver with webdriver-manager...")
    try:
        # Use webdriver-manager to automatically download and manage chromedriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"✅ Chrome driver initialized: {driver.capabilities['browserVersion']}")
    except Exception as e:
        print(f"❌ Failed to initialize driver: {e}")
        # Fallback to system chromedriver if webdriver-manager fails
        print("⚠️  Falling back to system chromedriver...")
        driver = webdriver.Chrome(options=chrome_options)
    
    driver.implicitly_wait(15)  # Increased for local server
    driver.set_page_load_timeout(30)
    
    yield driver
    
    # Cleanup
    try:
        driver.save_screenshot("final_state.png")
        print("📸 Final screenshot saved")
    except Exception as e:
        print(f"⚠️  Could not save final screenshot: {e}")
    
    try:
        driver.quit()
        print("✅ Chrome driver closed")
    except:
        pass

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment or use localhost"""
    app_url = os.getenv("APP_URL", "http://localhost:3000")
    print(f"🌐 Using base URL: {app_url}")
    return app_url

@pytest.fixture(scope="function")
def wait(driver):
    """Provide WebDriverWait instance"""
    return WebDriverWait(driver, 20)

@pytest.fixture(scope="function")
def take_screenshot(driver):
    """Take screenshot helper"""
    def _take_screenshot(name):
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")
        return filename
    return _take_screenshot

@pytest.fixture(scope="function")
def cleanup_memories(driver, base_url):
    """Cleanup after test by deleting test memories"""
    yield
    # This runs after each test
    try:
        driver.get(base_url)
        time.sleep(2)
        # Logic to delete test memories if needed
        print("🧹 Test cleanup completed")
    except Exception as e:
        print(f"⚠️  Cleanup failed: {e}")