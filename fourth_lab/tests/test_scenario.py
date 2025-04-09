from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_user_post_comment_flow():
    # Create user
    user = client.post("/users/", json={"name": "ComplexUser", "email": "complex@example.com"}).json()

    # Create post using user
    post = client.post(f"/users/{user['id']}/posts/", json={"title": "Hello", "content": "Post body"}).json()

    # Create comment using post
    comment = client.post(f"/posts/{post['id']}/comments/", json={"content": "Nice post!"}).json()

    # Get comments to verify
    comments = client.get(f"/posts/{post['id']}/comments/").json()
    assert any(c["content"] == "Nice post!" for c in comments)
