# Selenium Tests for MERN Memories

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start MongoDB: `mongod` or `docker run -d -p 27017:27017 mongo`
3. Start backend: `cd backend && npm start`
4. Start frontend: `cd frontend && npm start`
5. Run tests: `python run_tests.py`

## Test Structure
- `tests/conftest.py`: Configuration and fixtures
- `tests/test_*.py`: Test suites