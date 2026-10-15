# Entities Service

A FastAPI-based service for managing entities with MongoDB integration.

## Prerequisites

- Python 3.8 or higher
- MongoDB instance (local or cloud)
- pip (Python package manager)
- virtualenv (recommended)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd entities
```

2. Create and activate a virtual environment:
```bash
python -m venv projenv
source projenv/bin/activate  # On Unix/macOS
# OR
.\projenv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
MONGO_URI="your_mongodb_connection_string"
API_KEY="your_api_key"
RANDOM="path_to_project_root"
FILE_SVC_URI="http://localhost:8001"
FILE_SVC_APIKEY="your_file_service_api_key"
```

### Environment Variables Explained

- `MONGO_URI`: MongoDB connection string (required)
- `API_KEY`: API key for service authentication
- `RANDOM`: Project root directory path
- `FILE_SVC_URI`: File service endpoint URL
- `FILE_SVC_APIKEY`: API key for file service authentication

## Testing

Before running the service, it's recommended to run the test suite to ensure everything is working correctly:

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
# From the project root directory
python -m pytest
```

3. Run specific unit tests:
```bash
# From the project root directory
python -m pytest tests/unit_tests.py -v
```

### Test Run Screenshot 
<img src = "https://github.com/Chat-craft/.github/blob/main/entities-tests.png" />

### Troubleshooting Test Issues

If you encounter errors while running tests:

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Check if the virtual environment is activated:
```bash
# On Unix/macOS
source projenv/bin/activate
# On Windows
.\projenv\Scripts\activate
```

3. Verify the project structure:
```
entities/
├── src/
│   └── app/
│       ├── core/
│       ├── models/
│       ├── schemas/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── unit_tests.py
├── pyproject.toml
└── requirements.txt
```

4. If you get import errors:
   - Make sure you're running the tests from the project root directory
   - Use `python -m pytest` instead of just `pytest`
   - Check that all `__init__.py` files are present in the necessary directories

5. For MongoDB-related test failures, ensure your MongoDB instance is running and the connection string in `.env` is correct.

## Running the Service

1. Start the service:
```bash
uvicorn main:app --reload
```

The service will be available at `http://localhost:8000`

## Development

- The project uses `ruff` for linting
- Tests can be run using `pytest`
- API documentation is available at `/docs` when the service is running

## Project Structure

```
entities/
├── src/            # Source code
├── tests/          # Test files
├── requirements.txt # Project dependencies
├── main.py         # Application entry point
└── .env           # Environment configuration
```

## License

See the [LICENSE](LICENSE) file for details.
