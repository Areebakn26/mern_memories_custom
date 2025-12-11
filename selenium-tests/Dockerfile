FROM python:3.9-slim

# ============ SYSTEM DEPENDENCIES ============
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libgbm1 \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# ============ INSTALL CHROME ============
RUN mkdir -p /etc/apt/keyrings && \
    wget -q -O /etc/apt/keyrings/chrome.asc https://dl-ssl.google.com/linux/linux_signing_key.pub && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/chrome.asc] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# ============ INSTALL CHROMEDRIVER (FIXED) ============
# Using webdriver-manager which automatically handles version matching
RUN pip install --no-cache-dir webdriver-manager

# ============ SETUP PYTHON ENVIRONMENT ============
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============ COPY TEST FILES ============
# Copy all test files
COPY . .

# ============ CREATE DIRECTORIES ============
# Create directories for test results and screenshots
RUN mkdir -p /app/test-results && \
    mkdir -p /app/ss && \
    mkdir -p /app/tests

# ============ VERIFICATION ============
# Verify installation
RUN echo "=== Verification ===" && \
    python --version && \
    pip list | grep -E "selenium|pytest|webdriver" && \
    google-chrome --version

# ============ ENVIRONMENT VARIABLES ============
# Set environment variables for headless Chrome
ENV HEADLESS=true
ENV DISPLAY=:99
ENV PYTHONPATH=/app
ENV SCREENSHOT_DIR=/app/ss

# ============ DEFAULT COMMAND ============
# Default command to run tests (can be overridden by Jenkins)
CMD ["python", "-m", "pytest", "tests/", "-v", \
     "--html=/app/test-results/report.html", \
     "--self-contained-html", \
     "--junitxml=/app/test-results/junit-results.xml", \
     "--tb=short"]