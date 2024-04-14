# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_create_user():
#     create_user_request = {
#         "username": "test@example.com",
#         "password": "testpassword"
#     }
#     response = client.post("/auth/", json=create_user_request)
    
#     assert response.status_code == 201
#     assert response.json() == {"message": "User created successfully"}

# def test_login_for_access_token():
#     form_data = {
#         "username": "test@example.com",
#         "password": "testpassword"
#     }
#     response = client.post("/auth/token", data=form_data)
    
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert "token_type" in response.json()

# def test_get_user():
#     access_token = "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"
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
#     response = client.get("/auth/", headers=headers)
    
#     assert response.status_code == 200
#     assert "username" in response.json()
#     assert "id" in response.json()

# if __name__ == "__main__":
#     test_create_user()
#     test_login_for_access_token()
#     test_get_user()
#     print("All tests passed successfully!")




# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_summarize_main():
#     # Test with valid content
#     content = "This is a test content to be summarized."
#     response = client.post("/summarize", json={"content": content})
#     assert response.status_code == 200
#     assert "choices" in response.json()
#     assert len(response.json()["choices"]) > 0

#     # Test with missing content
#     response = client.post("/summarize", json={})
#     assert response.status_code == 422  # Expecting a validation error

#     # Test with empty content
#     response = client.post("/summarize", json={"content": ""})
#     assert response.status_code == 422  # Expecting a validation error

#     # Test with invalid content type
#     response = client.post("/summarize", json={"content": 123})
#     assert response.status_code == 422  # Expecting a validation error

#     # Add more test cases as needed

# if __name__ == "__main__":
#     test_summarize_endpoint()
#     print("All tests passed successfully!")
