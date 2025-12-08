"""
Test script to demonstrate rate limiting functionality.
Run this while the Flask server is running on port 5001.
"""

import requests
import time

API_URL = "http://localhost:5001/auth/login"

def test_rate_limiting():
    print("=== Rate Limiting Test ===\n")

    # Test with invalid credentials to trigger rate limiting
    test_email = "test@example.com"
    wrong_password = "wrongpassword"

    print(f"Testing rate limiting with email: {test_email}")
    print(f"Using incorrect password to trigger failed attempts\n")
    print("Configuration: Max 5 attempts, 30-minute lockout\n")

    for attempt in range(1, 8):
        print(f"--- Attempt {attempt} ---")

        try:
            response = requests.post(
                API_URL,
                json={"email": test_email, "password": wrong_password},
                timeout=5
            )

            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Response: {data.get('error', data)}")

            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                if retry_after:
                    print(f"Retry-After header: {retry_after} seconds")
                print("\n✓ Account locked due to too many failed attempts!")
                break

            print()
            time.sleep(0.5)  # Small delay between requests

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            print("Make sure the Flask server is running on port 5001")
            return

    print("\n=== Testing Successful Login (clears rate limit) ===\n")

    # Now test with correct password
    correct_password = "password123"

    print(f"Attempting login with correct password...")
    try:
        response = requests.post(
            API_URL,
            json={"email": test_email, "password": correct_password},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        data = response.json()

        if response.status_code == 200:
            print(f"✓ Login successful! Token: {data.get('token', '')[:20]}...")
            print("Rate limit cleared on successful login")
        else:
            print(f"Response: {data.get('error', data)}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rate_limiting()
