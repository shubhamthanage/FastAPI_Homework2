#!/usr/bin/env python3
"""
Test script for the new signature generation API endpoint
"""

import json
import subprocess
import sys

def test_signature_api():
    """Test the signature generation API endpoint"""
    
    # Test payload
    test_payload = {
        "amount": 150.50,
        "currency": "EUR",
        "order_id": "test_order_456",
        "payment_method": "paypal"
    }
    
    print("=== Testing Signature Generation API ===\n")
    print("Test payload:")
    print(json.dumps(test_payload, indent=2))
    print()
    
    # Try to call the API using curl
    try:
        # Convert payload to JSON string
        json_data = json.dumps(test_payload)
        
        # Call the API endpoint
        result = subprocess.run([
            'curl', '-s', '-X', 'POST',
            'http://localhost:8000/api/v1/payments/generate-signature',
            '-H', 'Content-Type: application/json',
            '-d', json_data
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ API call successful!")
            print("Response:")
            print(result.stdout)
            
            # Parse the response
            try:
                response_data = json.loads(result.stdout)
                signature = response_data.get('signature')
                payload = response_data.get('payload')
                
                print(f"\n📝 Generated signature: {signature}")
                print(f"📦 Payload used: {json.dumps(payload, indent=2)}")
                
            except json.JSONDecodeError:
                print("❌ Could not parse API response as JSON")
                
        else:
            print("❌ API call failed!")
            print(f"Error: {result.stderr}")
            print(f"Exit code: {result.returncode}")
            
    except FileNotFoundError:
        print("❌ curl command not found. Please install curl or test manually.")
    except Exception as e:
        print(f"❌ Error testing API: {e}")
    
    print("\n=== Manual Testing Instructions ===")
    print("1. Start your FastAPI server: uvicorn app.main:app --reload")
    print("2. Open Swagger UI: http://localhost:8000/docs")
    print("3. Test the POST /api/v1/payments/generate-signature endpoint")
    print("4. Use the returned signature to test the payment endpoint")

if __name__ == "__main__":
    test_signature_api()
