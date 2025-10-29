"""
HL7 API Client Tester
A client for testing the HL7 API server
"""

import requests
import sys
from datetime import datetime


class HL7Client:
    """Client for interacting with HL7 API Server"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Check server health"""
        try:
            response = self.session.get(f'{self.base_url}/health')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def send_message(self, hl7_message):
        """Send HL7 message to server"""
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/hl7/message',
                data=hl7_message.encode('utf-8'),
                headers={'Content-Type': 'text/plain'}
            )
            return response.status_code, response.json()
        except Exception as e:
            return None, {'error': str(e)}
    
    def validate_message(self, hl7_message):
        """Validate HL7 message"""
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/hl7/validate',
                data=hl7_message.encode('utf-8'),
                headers={'Content-Type': 'text/plain'}
            )
            return response.status_code, response.json()
        except Exception as e:
            return None, {'error': str(e)}
    
    def get_messages(self):
        """Get all received messages"""
        try:
            response = self.session.get(f'{self.base_url}/api/v1/hl7/messages')
            return response.status_code, response.json()
        except Exception as e:
            return None, {'error': str(e)}
    
    def clear_messages(self):
        """Clear all received messages"""
        try:
            response = self.session.delete(f'{self.base_url}/api/v1/hl7/messages')
            return response.status_code, response.json()
        except Exception as e:
            return None, {'error': str(e)}


def create_sample_hl7_message():
    """Create a sample HL7 ADT^A01 message"""
    message = (
        "MSH|^~\\&|SENDING_APP|SENDING_FAC|RECEIVING_APP|RECEIVING_FAC|"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}||ADT^A01|MSG00001|P|2.5\r"
        "EVN|A01|{datetime.now().strftime('%Y%m%d%H%M%S')}\r"
        "PID|1||12345^^^MRN||DOE^JOHN^A||19800101|M|||123 MAIN ST^^CITY^ST^12345\r"
        "PV1|1|I|WARD^ROOM^BED||||DOCTOR^ATTENDING|||||||||||VISIT123\r"
    )
    return message


def run_tests(base_url='http://localhost:5000'):
    """Run comprehensive tests"""
    print("=" * 60)
    print("HL7 API CLIENT TESTER")
    print("=" * 60)
    print(f"Testing server at: {base_url}\n")
    
    client = HL7Client(base_url)
    
    # Test 1: Health Check
    print("Test 1: Health Check")
    print("-" * 40)
    health = client.health_check()
    print(f"Response: {health}")
    if 'status' in health and health['status'] == 'healthy':
        print("✓ PASSED\n")
    else:
        print("✗ FAILED\n")
    
    # Test 2: Send HL7 Message
    print("Test 2: Send HL7 Message")
    print("-" * 40)
    sample_message = create_sample_hl7_message()
    print(f"Sending message:\n{sample_message[:100]}...")
    status, response = client.send_message(sample_message)
    print(f"Status: {status}")
    print(f"Response: {response}")
    if status == 200 and response.get('status') == 'success':
        print("✓ PASSED\n")
    else:
        print("✗ FAILED\n")
    
    # Test 3: Validate HL7 Message
    print("Test 3: Validate HL7 Message")
    print("-" * 40)
    status, response = client.validate_message(sample_message)
    print(f"Status: {status}")
    print(f"Response: {response}")
    if status == 200 and response.get('valid'):
        print("✓ PASSED\n")
    else:
        print("✗ FAILED\n")
    
    # Test 4: Get Messages
    print("Test 4: Get Received Messages")
    print("-" * 40)
    status, response = client.get_messages()
    print(f"Status: {status}")
    print(f"Response: {response}")
    if status == 200 and 'messages' in response:
        print("✓ PASSED\n")
    else:
        print("✗ FAILED\n")
    
    # Test 5: Invalid Message
    print("Test 5: Invalid HL7 Message")
    print("-" * 40)
    invalid_message = "INVALID|MESSAGE|DATA"
    status, response = client.send_message(invalid_message)
    print(f"Status: {status}")
    print(f"Response: {response}")
    if status == 400 and 'error' in response:
        print("✓ PASSED (correctly rejected invalid message)\n")
    else:
        print("✗ FAILED\n")
    
    # Test 6: Clear Messages
    print("Test 6: Clear Messages")
    print("-" * 40)
    status, response = client.clear_messages()
    print(f"Status: {status}")
    print(f"Response: {response}")
    if status == 200 and response.get('status') == 'success':
        print("✓ PASSED\n")
    else:
        print("✗ FAILED\n")
    
    print("=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    # Allow custom base URL from command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    run_tests(base_url)
