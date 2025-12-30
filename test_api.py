import requests

BASE_URL = "http://localhost:5001"

def test_flow():
    session = requests.Session()
    
    # 1. Signup User A
    print("--- User A Flow ---")
    email_a = "userA@example.com"
    password = "password123"
    session.post(f"{BASE_URL}/signup", json={
        "firstName": "User", "lastName": "A", "email": email_a, "password": password, "age": 25, "gender": "male"
    })
    
    # Login User A
    session.post(f"{BASE_URL}/login", json={"email": email_a, "password": password})
    user_a_id = session.get(f"{BASE_URL}/profile/view").json().get('id')
    print(f"User A ID: {user_a_id}")
    session.post(f"{BASE_URL}/logout") # Logout A

    # 2. Signup User B
    print("\n--- User B Flow ---")
    email_b = "userB@example.com"
    session.post(f"{BASE_URL}/signup", json={
        "firstName": "User", "lastName": "B", "email": email_b, "password": password, "age": 28, "gender": "female"
    })
    
    # Login User B
    session.post(f"{BASE_URL}/login", json={"email": email_b, "password": password})
    user_b_id = session.get(f"{BASE_URL}/profile/view").json().get('id')
    print(f"User B ID: {user_b_id}")
    
    # User B sends request to User A
    print("\n--- Sending Request ---")
    resp = session.post(f"{BASE_URL}/send/interested/{user_a_id}")
    print(f"Send Request: {resp.status_code} - {resp.text}")
    session.post(f"{BASE_URL}/logout") # Logout B
    
    # 3. User A logs in to review
    print("\n--- User A Review Flow ---")
    session.post(f"{BASE_URL}/login", json={"email": email_a, "password": password})
    
    # Check received requests
    received = session.get(f"{BASE_URL}/user/connections/received").json()
    print(f"Received Requests: {received}")
    
    if received['data']:
        request_id = received['data'][0].get('requestId') # Note: Check routing key in user.py
        # Accept request
        print(f"Accepting Request ID: {request_id}")
        resp = session.post(f"{BASE_URL}/request/review/accepted/{request_id}")
        print(f"Review Request: {resp.status_code} - {resp.text}")
        
        # Check Connections
        connections = session.get(f"{BASE_URL}/user/connections").json()
        print(f"Connections: {connections}")
    
    # Check Feed (Should be empty or contain other users if any)
    feed = session.get(f"{BASE_URL}/feed").json()
    print(f"Feed: {feed}")

if __name__ == "__main__":
    test_flow()
