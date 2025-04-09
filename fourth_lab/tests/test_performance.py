import time
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_posts_performance():
    start = time.time()
    for _ in range(50):
        response = client.get("/posts/?skip=0&limit=5")
        assert response.status_code == 200
    duration = time.time() - start
    print(f"Time taken for 50 GETs: {duration:.2f}s")
    assert duration < 5  # adjust as needed
