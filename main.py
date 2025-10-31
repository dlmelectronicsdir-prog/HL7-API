"""
FastAPI Middleware for Laboratory Analyzer (F2400) integration with PURELAB LIS.
"""

from fastapi import FastAPI, Header, HTTPException
from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
import secrets

app = FastAPI(
    title="Laboratory Analyzer LIS API",
    description="Middleware API for F2400 Laboratory Analyzer integration with PURELAB LIS",
    version="1.0.0"
)

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60

# Hardcoded credentials
VALID_USERNAME = "wsadmin"
VALID_PASSWORD = "password"

# Mock data
MOCK_SAMPLES = {
    "S001": {
        "patient_id": "P12345",
        "patient_name": "John Doe",
        "patient_gender": "M",
        "patient_dob": "1980-01-15",
        "tests": ["CBC", "GLU", "CRE"]
    },
    "S002": {
        "patient_id": "P67890",
        "patient_name": "Jane Smith",
        "patient_gender": "F",
        "patient_dob": "1990-05-20",
        "tests": ["HBA1C", "TSH"]
    }
}

MOCK_TESTS = {
    "CBC": "Complete Blood Count",
    "GLU": "Glucose",
    "CRE": "Creatinine",
    "HBA1C": "Hemoglobin A1C",
    "TSH": "Thyroid Stimulating Hormone",
    "ALT": "Alanine Aminotransferase",
    "AST": "Aspartate Aminotransferase"
}


def generate_token(username: str) -> str:
    """Generate JWT token for authenticated user."""
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def validate_token(token: str) -> dict:
    """Validate JWT token and return payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="INVALID_LOGIN")


@app.get("/lis_apis/applogin")
async def login(userName: str, password: str):
    """
    Authentication endpoint.
    
    Args:
        userName: User login name
        password: User password
    
    Returns:
        OK_LOGIN|{token} on success
        INVALID_LOGIN on failure
    """
    if userName == VALID_USERNAME and password == VALID_PASSWORD:
        token = generate_token(userName)
        return f"OK_LOGIN|{token}"
    return "INVALID_LOGIN"


@app.get("/lis_apis/tests_lis_download/{sample_id}")
async def get_pending_tests(sample_id: str, token: Optional[str] = Header(None)):
    """
    Get pending tests for a sample.
    
    Args:
        sample_id: Sample identifier
        token: JWT token in header
    
    Returns:
        QUERY_OK|Test_Count|Patient_id|Patient_Name|Patient_Gender|Patient_DOB|Test_code_1|...
        NOT_FOUND if sample not found
        INVALID_LOGIN or EXPIRED_TOKEN on auth failure
    """
    if not token:
        return "INVALID_LOGIN"
    
    try:
        validate_token(token)
    except HTTPException as e:
        return e.detail
    
    if sample_id not in MOCK_SAMPLES:
        return "NOT_FOUND"
    
    sample = MOCK_SAMPLES[sample_id]
    test_count = len(sample["tests"])
    
    response_parts = [
        "QUERY_OK",
        str(test_count),
        sample["patient_id"],
        sample["patient_name"],
        sample["patient_gender"],
        sample["patient_dob"]
    ]
    response_parts.extend(sample["tests"])
    
    return "|".join(response_parts)


@app.post("/lis_apis/results_lis_upload/{path_data}")
async def upload_results(path_data: str, token: Optional[str] = Header(None)):
    """
    Upload test results.
    
    Args:
        path_data: Data in format SampleId|TestCode1=Result1|TestCode2=Result2|...
        token: JWT token in header
    
    Returns:
        Pipe-separated status flags (UPLOADED or NOT_FOUND for each test)
        INVALID_LOGIN or EXPIRED_TOKEN on auth failure
    """
    if not token:
        return "INVALID_LOGIN"
    
    try:
        validate_token(token)
    except HTTPException as e:
        return e.detail
    
    # Parse path_data
    parts = path_data.split("|")
    if len(parts) < 2:
        return "NOT_FOUND"
    
    sample_id = parts[0]
    
    # Check if sample exists
    if sample_id not in MOCK_SAMPLES:
        return "NOT_FOUND"
    
    # Process test results
    status_flags = []
    for i in range(1, len(parts)):
        try:
            if "=" in parts[i]:
                test_code, result = parts[i].split("=", 1)
                # Check if test is in the sample's test list
                if test_code in MOCK_SAMPLES[sample_id]["tests"]:
                    status_flags.append("UPLOADED")
                else:
                    status_flags.append("NOT_FOUND")
            else:
                status_flags.append("NOT_FOUND")
        except ValueError:
            status_flags.append("NOT_FOUND")
    
    return "|".join(status_flags)


@app.get("/lis_apis/get_tests_list")
async def get_tests_list(token: Optional[str] = Header(None)):
    """
    Get all available tests.
    
    Args:
        token: JWT token in header
    
    Returns:
        QUERY_OK|Test_Count|Test_code_1<TAB>Test_Name_1|...
        NOT_FOUND if no tests available
        INVALID_LOGIN or EXPIRED_TOKEN on auth failure
    """
    if not token:
        return "INVALID_LOGIN"
    
    try:
        validate_token(token)
    except HTTPException as e:
        return e.detail
    
    if not MOCK_TESTS:
        return "NOT_FOUND"
    
    test_count = len(MOCK_TESTS)
    response_parts = ["QUERY_OK", str(test_count)]
    
    for test_code, test_name in MOCK_TESTS.items():
        response_parts.append(f"{test_code}\t{test_name}")
    
    return "|".join(response_parts)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Laboratory Analyzer LIS API",
        "version": "1.0.0",
        "endpoints": [
            "GET /lis_apis/applogin",
            "GET /lis_apis/tests_lis_download/{sample_id}",
            "POST /lis_apis/results_lis_upload/{path_data}",
            "GET /lis_apis/get_tests_list"
        ]
    }
