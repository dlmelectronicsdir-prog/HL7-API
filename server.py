"""
HL7 API Server
A Flask-based API server for handling HL7 messages
"""

from flask import Flask, request, jsonify
import hl7
from datetime import datetime, timezone

app = Flask(__name__)

# Store received messages for testing purposes
received_messages = []


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200


@app.route('/api/v1/hl7/message', methods=['POST'])
def receive_hl7_message():
    """
    Receive and parse HL7 message
    
    Expected format: HL7 message in request body
    Returns: Parsed message details
    """
    try:
        # Get message from request body
        message_data = request.data.decode('utf-8')
        
        if not message_data:
            return jsonify({
                'error': 'No message data provided'
            }), 400
        
        # Parse HL7 message
        message = hl7.parse(message_data)
        
        # Extract basic information
        message_type = str(message.segment('MSH')[9]) if message.segment('MSH') else 'Unknown'
        
        # Store message
        message_record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message_type': message_type,
            'raw_message': message_data,
            'segment_count': len(message)
        }
        received_messages.append(message_record)
        
        return jsonify({
            'status': 'success',
            'message_type': message_type,
            'segment_count': len(message),
            'timestamp': message_record['timestamp']
        }), 200
        
    except Exception as e:
        # Log the full error for debugging but return a sanitized message
        app.logger.error(f'Failed to parse HL7 message: {str(e)}')
        return jsonify({
            'error': 'Failed to parse HL7 message'
        }), 400


@app.route('/api/v1/hl7/messages', methods=['GET'])
def get_messages():
    """Get all received messages"""
    return jsonify({
        'count': len(received_messages),
        'messages': received_messages
    }), 200


@app.route('/api/v1/hl7/messages', methods=['DELETE'])
def clear_messages():
    """Clear all received messages"""
    global received_messages
    count = len(received_messages)
    received_messages = []
    return jsonify({
        'status': 'success',
        'cleared_count': count
    }), 200


@app.route('/api/v1/hl7/validate', methods=['POST'])
def validate_hl7_message():
    """
    Validate HL7 message without storing it
    
    Expected format: HL7 message in request body
    Returns: Validation result
    """
    try:
        message_data = request.data.decode('utf-8')
        
        if not message_data:
            return jsonify({
                'valid': False,
                'error': 'No message data provided'
            }), 400
        
        # Parse HL7 message
        message = hl7.parse(message_data)
        
        # Basic validation checks
        validation_result = {
            'valid': True,
            'message_type': str(message.segment('MSH')[9]) if message.segment('MSH') else None,
            'segment_count': len(message),
            'has_msh': message.segment('MSH') is not None,
            'segments': [str(seg[0]) for seg in message]
        }
        
        return jsonify(validation_result), 200
        
    except Exception as e:
        # Log the full error for debugging but return a sanitized message
        app.logger.error(f'Failed to validate HL7 message: {str(e)}')
        return jsonify({
            'valid': False,
            'error': 'Invalid HL7 message format'
        }), 200


if __name__ == '__main__':
    import os
    # Only run in debug mode if explicitly set
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
