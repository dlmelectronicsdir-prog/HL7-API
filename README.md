# HL7-API
HL7 API Server and Client Tester

## Overview
This project provides a complete HL7 (Health Level 7) API server and client testing framework. It includes:
- A Flask-based REST API server for receiving and processing HL7 messages
- A Python client for testing the API server
- Comprehensive unit tests
- Sample HL7 messages

## Features
- **HL7 Message Processing**: Parse and validate HL7 v2.x messages
- **REST API Endpoints**: 
  - Health check
  - Send HL7 messages
  - Validate HL7 messages
  - Retrieve received messages
  - Clear message history
- **Client Tester**: Interactive testing tool with multiple test scenarios
- **Unit Tests**: Full pytest test suite

## Installation

### Prerequisites
- Python 3.7 or higher
- pip

### Setup
1. Clone the repository:
```bash
git clone https://github.com/dlmelectronicsdir-prog/HL7-API.git
cd HL7-API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API Server
Start the server on port 5000:
```bash
python server.py
```

The server will be available at `http://localhost:5000`

### Running the Client Tester
In a separate terminal, run the client tester:
```bash
python client.py
```

Or specify a custom server URL:
```bash
python client.py http://your-server:5000
```

### Running Tests
Run the unit tests:
```bash
pytest test_server.py -v
```

Run tests with coverage:
```bash
pytest test_server.py --cov=server --cov-report=html
```

## API Endpoints

### Health Check
```
GET /health
```
Returns server health status

### Send HL7 Message
```
POST /api/v1/hl7/message
Content-Type: text/plain

[HL7 message content]
```
Receives and parses an HL7 message

### Validate HL7 Message
```
POST /api/v1/hl7/validate
Content-Type: text/plain

[HL7 message content]
```
Validates an HL7 message without storing it

### Get All Messages
```
GET /api/v1/hl7/messages
```
Returns all received messages

### Clear Messages
```
DELETE /api/v1/hl7/messages
```
Clears all received messages

## Example HL7 Message
```
MSH|^~\&|SENDING_APP|SENDING_FAC|RECEIVING_APP|RECEIVING_FAC|20250101120000||ADT^A01|MSG00001|P|2.5
EVN|A01|20250101120000
PID|1||12345^^^MRN||DOE^JOHN^A||19800101|M|||123 MAIN ST^^CITY^ST^12345
PV1|1|I|WARD^ROOM^BED||||DOCTOR^ATTENDING|||||||||||VISIT123
```

## Testing Scenarios
The client tester runs the following tests:
1. Health check
2. Send valid HL7 message
3. Validate HL7 message
4. Retrieve received messages
5. Send invalid message (error handling)
6. Clear messages

## Development

### Project Structure
```
HL7-API/
├── server.py          # Flask API server
├── client.py          # Client tester
├── test_server.py     # Unit tests
├── requirements.txt   # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

### Dependencies
- Flask: Web framework for the API server
- hl7: HL7 message parsing library
- requests: HTTP client for testing
- pytest: Testing framework

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
