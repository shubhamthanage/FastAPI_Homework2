#!/usr/bin/env python3
"""
Helper script to generate x-signature for testing the payments API in Swagger UI
"""

import hmac
import hashlib
import json

def generate_signature(payload, secret="devsecret"):
    """
    Generate HMAC-SHA256 signature for the given payload
    
    Args:
        payload (dict): The JSON payload you want to send
        secret (str): The webhook secret (default: "devsecret")
    
    Returns:
        str: The hex digest signature to use as x-signature header
    """
    # Convert payload to JSON string, then to bytes
    json_string = json.dumps(payload)
    json_bytes = json_string.encode('utf-8')
    
    # Compute HMAC-SHA256 signature
    signature = hmac.new(
        secret.encode('utf-8'),
        json_bytes,
        hashlib.sha256
    ).hexdigest()
    
    return signature

def main():
    print("=== Payments API Signature Generator ===\n")
    
    # Your exact payload from the curl command
    exact_payload = {
        "amount": 10,
        "currency": "INR",
        "order_id": "1",
        "payment_method": "UPI"
    }
    
    print("Your exact payload:")
    print(json.dumps(exact_payload, indent=2))
    print()
    
    # Generate signature for your exact payload
    signature = generate_signature(exact_payload)
    print("Generated x-signature for your payload:")
    print(f"x-signature: {signature}")
    print()
    
    print("=== Updated curl command ===")
    print("Use this exact curl command:")
    print()
    print(f'curl -X POST \\')
    print(f"  'http://127.0.0.1:8000/api/v1/payments/payment' \\")
    print(f"  -H 'accept: application/json' \\")
    print(f"  -H 'x-signature: {signature}' \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -d '{json.dumps(exact_payload)}'")
    print()
    
    print("=== How to use in Swagger UI ===")
    print("1. Copy the signature above")
    print("2. In Swagger UI, click 'Try it out'")
    print("3. Paste the signature in the x-signature field")
    print("4. Paste the JSON payload in the request body")
    print("5. Click 'Execute'")
    print()
    
    print("=== Important Notes ===")
    print("- The signature is specific to the exact JSON payload")
    print("- Even a single space difference will require a new signature")
    print("- Always use the generate-signature endpoint for new payloads")

if __name__ == "__main__":
    main()
