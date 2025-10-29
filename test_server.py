"""
Unit tests for HL7 API Server
"""

import pytest
import json
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_hl7_message():
    """Sample HL7 ADT^A01 message"""
    return (
        "MSH|^~\\&|SENDING_APP|SENDING_FAC|RECEIVING_APP|RECEIVING_FAC|"
        "20250101120000||ADT^A01|MSG00001|P|2.5\r"
        "EVN|A01|20250101120000\r"
        "PID|1||12345^^^MRN||DOE^JOHN^A||19800101|M|||123 MAIN ST^^CITY^ST^12345\r"
        "PV1|1|I|WARD^ROOM^BED||||DOCTOR^ATTENDING|||||||||||VISIT123\r"
    )


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_receive_valid_hl7_message(client, sample_hl7_message):
    """Test receiving a valid HL7 message"""
    # Clear messages first
    client.delete('/api/v1/hl7/messages')
    
    response = client.post(
        '/api/v1/hl7/message',
        data=sample_hl7_message,
        content_type='text/plain'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message_type'] == 'ADT^A01'
    assert data['segment_count'] > 0


def test_receive_empty_message(client):
    """Test receiving an empty message"""
    response = client.post(
        '/api/v1/hl7/message',
        data='',
        content_type='text/plain'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_receive_invalid_hl7_message(client):
    """Test receiving an invalid HL7 message"""
    response = client.post(
        '/api/v1/hl7/message',
        data='INVALID|MESSAGE',
        content_type='text/plain'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_validate_hl7_message(client, sample_hl7_message):
    """Test validating an HL7 message"""
    response = client.post(
        '/api/v1/hl7/validate',
        data=sample_hl7_message,
        content_type='text/plain'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is True
    assert data['message_type'] == 'ADT^A01'
    assert data['has_msh'] is True
    assert 'segments' in data


def test_validate_invalid_message(client):
    """Test validating an invalid message"""
    response = client.post(
        '/api/v1/hl7/validate',
        data='INVALID',
        content_type='text/plain'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is False
    assert 'error' in data


def test_get_messages(client, sample_hl7_message):
    """Test getting all received messages"""
    # Clear messages first
    client.delete('/api/v1/hl7/messages')
    
    # Send a message
    client.post(
        '/api/v1/hl7/message',
        data=sample_hl7_message,
        content_type='text/plain'
    )
    
    # Get messages
    response = client.get('/api/v1/hl7/messages')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'count' in data
    assert 'messages' in data
    assert data['count'] >= 1


def test_clear_messages(client, sample_hl7_message):
    """Test clearing all messages"""
    # Send a message
    client.post(
        '/api/v1/hl7/message',
        data=sample_hl7_message,
        content_type='text/plain'
    )
    
    # Clear messages
    response = client.delete('/api/v1/hl7/messages')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'cleared_count' in data
    
    # Verify messages are cleared
    response = client.get('/api/v1/hl7/messages')
    data = json.loads(response.data)
    assert data['count'] == 0
