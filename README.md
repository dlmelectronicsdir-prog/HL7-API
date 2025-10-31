# HL7-API

FastAPI Middleware for Laboratory Analyzer (F2400) integration with PURELAB LIS.

## Overview

This API serves as a middleware layer between the F2400 laboratory analyzer and the PURELAB Laboratory Information System (LIS). It provides four main endpoints for authentication, retrieving pending tests, uploading test results, and listing available tests.

## Features

- **JWT-based Authentication**: Secure token-based authentication for all protected endpoints
- **Mock Data**: Pre-configured sample and test data for development and testing
- **Simple Integration**: RESTful API with straightforward request/response formats
- **FastAPI Framework**: Modern, fast, and well-documented Python web framework

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dlmelectronicsdir-prog/HL7-API.git
cd HL7-API
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the API server using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

For production deployment, remove the `--reload` flag:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### 1. Authentication

**Endpoint**: `GET /lis_apis/applogin`

**Query Parameters**:
- `userName`: User login name
- `password`: User password

**Default Credentials** (for development only):
- Username: `wsadmin`
- Password: `password`

**⚠️ Security Note**: These credentials are hardcoded for development and testing purposes only. In production, credentials should be stored in environment variables or a secure configuration system.

**Response**:
- Success: `OK_LOGIN|{jwt_token}`
- Failure: `INVALID_LOGIN`

**Example**:
```bash
curl "http://localhost:8000/lis_apis/applogin?userName=wsadmin&password=password"
```

**Response**:
```
OK_LOGIN|eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Get Pending Tests

**Endpoint**: `GET /lis_apis/tests_lis_download/{sample_id}`

**Path Parameters**:
- `sample_id`: Sample identifier (e.g., S001, S002)

**Headers**:
- `token`: JWT token from login

**Response**:
- Success: `QUERY_OK|Test_Count|Patient_id|Patient_Name|Patient_Gender|Patient_DOB|Test_code_1|Test_code_2|...`
- Sample Not Found: `NOT_FOUND`
- Invalid Token: `INVALID_LOGIN`
- Expired Token: `EXPIRED_TOKEN`

**Example**:
```bash
curl -H "token: YOUR_JWT_TOKEN" "http://localhost:8000/lis_apis/tests_lis_download/S001"
```

**Response**:
```
QUERY_OK|3|P12345|John Doe|M|1980-01-15|CBC|GLU|CRE
```

### 3. Upload Results

**Endpoint**: `POST /lis_apis/results_lis_upload/{path_data}`

**Path Parameters**:
- `path_data`: Data in format `SampleId|TestCode1=Result1|TestCode2=Result2|...`

**Headers**:
- `token`: JWT token from login

**Response**:
- Pipe-separated status flags for each test:
  - `UPLOADED`: Test result successfully uploaded
  - `NOT_FOUND`: Test or sample not found
- `INVALID_LOGIN`: Invalid token
- `EXPIRED_TOKEN`: Expired token

**Example**:
```bash
curl -X POST -H "token: YOUR_JWT_TOKEN" \
  "http://localhost:8000/lis_apis/results_lis_upload/S001%7CCBC=14.5%7CGLU=95"
```

**Response**:
```
UPLOADED|UPLOADED
```

### 4. Get All Tests

**Endpoint**: `GET /lis_apis/get_tests_list`

**Headers**:
- `token`: JWT token from login

**Response**:
- Success: `QUERY_OK|Test_Count|Test_code_1<TAB>Test_Name_1|Test_code_2<TAB>Test_Name_2|...`
- No Tests: `NOT_FOUND`
- Invalid Token: `INVALID_LOGIN`
- Expired Token: `EXPIRED_TOKEN`

**Example**:
```bash
curl -H "token: YOUR_JWT_TOKEN" "http://localhost:8000/lis_apis/get_tests_list"
```

**Response**:
```
QUERY_OK|7|CBC	Complete Blood Count|GLU	Glucose|CRE	Creatinine|...
```

## Mock Data

The API comes with pre-configured mock data for testing:

### Sample Data:
- **S001**: John Doe (M, DOB: 1980-01-15) - Tests: CBC, GLU, CRE
- **S002**: Jane Smith (F, DOB: 1990-05-20) - Tests: HBA1C, TSH

### Test Catalog:
- CBC - Complete Blood Count
- GLU - Glucose
- CRE - Creatinine
- HBA1C - Hemoglobin A1C
- TSH - Thyroid Stimulating Hormone
- ALT - Alanine Aminotransferase
- AST - Aspartate Aminotransferase

## Security

- JWT tokens expire after 60 minutes
- The secret key is randomly generated at server startup
- For production use, consider:
  - Storing credentials in environment variables
  - Using a persistent secret key
  - Implementing a proper database backend
  - Adding rate limiting
  - Enabling HTTPS/TLS

## Development

### Project Structure
```
HL7-API/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .github/            # GitHub workflows
```

### Adding More Tests or Samples

Edit the `MOCK_SAMPLES` and `MOCK_TESTS` dictionaries in `main.py` to add more test data.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port number with `--port 8001`
2. **Module not found**: Ensure you've activated the virtual environment and installed dependencies
3. **Token expired**: Re-authenticate to get a new token

## License

This project is provided as-is for integration purposes.

## Support

For issues or questions, please open an issue on the GitHub repository.
