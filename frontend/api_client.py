import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL")


def login_user(username: str, password: str):
    if not BASE_URL:
        raise RuntimeError("BACKEND_URL is not set")

    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": username,
            "password": password,
        },
        timeout=10,
    )

    if response.status_code != 200:
        return None

    return response.json()


def query_backend(token: str, query: str):
    if not BASE_URL:
        raise RuntimeError("BACKEND_URL is not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{BASE_URL}/query",
        headers=headers,
        json={"query": query},
        timeout=20,
    )

    if response.status_code != 200:
        return None

    return response.json()
