import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL")

def login_user(username: str, password: str):
    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": username, "password": password},
    )
    if response.status_code != 200:
        return None
    return response.json()


def query_backend(token: str, query: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/query",
        headers=headers,
        json={"query": query},
    )
    if response.status_code != 200:
        return None
    return response.json()


def get_users(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    if response.status_code != 200:
        return None
    return response.json()


def add_user_api(token: str, username: str, role: str, password: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/users/",
        headers=headers,
        json={
            "username": username,
            "role": role,
            "password": password,
        },
    )
    return response


def delete_user_api(token: str, username: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{BASE_URL}/users/{username}",
        headers=headers,
    )
    return response
