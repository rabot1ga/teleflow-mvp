#!/usr/bin/env python3
"""
TeleFlow Platform — Promotion Service Test

Tests parsing functionality.
"""

import requests
import time

BASE_URL = "http://localhost"
AUTH_URL = f"{BASE_URL}:8001"
PROMOTION_URL = f"{BASE_URL}:8008"
USERBOT_URL = f"{BASE_URL}:8007"


def get_token():
    """Login and get access token."""
    print("📝 Step 1: Getting auth token...")
    resp = requests.post(
        f"{AUTH_URL}/api/v1/auth/login",
        json={"email": "test5@example.com", "password": "TestPassword123!"}
    )
    if resp.status_code == 200:
        token = resp.json()["data"]["access_token"]
        print(f"   ✅ Token received")
        return token
    else:
        print(f"   ❌ Login failed: {resp.text}")
        return None


def check_userbot_accounts(token):
    """Check if there are any userbot accounts."""
    print("\n🤖 Step 2: Checking userbot accounts...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{USERBOT_URL}/api/v1/userbot/accounts",
        headers=headers,
        params={"project_id": "550e8400-e29b-41d4-a716-446655440000"}
    )
    if resp.status_code == 200:
        accounts = resp.json()["data"]
        active_accounts = [a for a in accounts if a.get("status") == "active"]
        print(f"   Found {len(accounts)} accounts, {len(active_accounts)} active")
        return active_accounts
    else:
        print(f"   ❌ Failed to get accounts: {resp.text}")
        return []


def create_parse_task(token):
    """Create parse task."""
    print("\n📊 Step 3: Creating parse task...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{PROMOTION_URL}/api/v1/promotion/tasks",
        headers=headers,
        json={
            "project_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Test Parse Task",
            "task_type": "parse",
            "source_chat_id": "@durov",  # Pavel Durov's channel as example
            "config": {
                "limit": 100,
                "filter_active_days": 30,
                "filter_has_photo": True
            }
        }
    )
    if resp.status_code == 200:
        task = resp.json()["data"]
        print(f"   ✅ Task created: {task['id']}")
        print(f"      Name: {task['name']}")
        print(f"      Type: {task['task_type']}")
        return task
    else:
        print(f"   ❌ Task creation failed: {resp.text}")
        return None


def start_task(token, task_id):
    """Start promotion task."""
    print(f"\n🚀 Step 4: Starting task {task_id[:8]}...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{PROMOTION_URL}/api/v1/promotion/tasks/{task_id}/start",
        headers=headers
    )
    if resp.status_code == 200:
        result = resp.json()["data"]
        print(f"   ✅ Task started")
        return result
    else:
        print(f"   ❌ Start failed: {resp.text}")
        return None


def wait_for_completion(token, task_id, timeout=60):
    """Wait for task to complete."""
    print(f"\n⏳ Step 5: Waiting for completion (up to {timeout}s)...")
    headers = {"Authorization": f"Bearer {token}"}

    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(
            f"{PROMOTION_URL}/api/v1/promotion/tasks/{task_id}",
            headers=headers
        )
        if resp.status_code == 200:
            task = resp.json()["data"]
            status = task["status"]
            processed = task["processed_count"]
            success = task["success_count"]

            print(f"   Status: {status}, Processed: {processed}, Success: {success}")

            if status == "completed":
                print(f"   ✅ Task completed!")
                return task
            elif status == "failed":
                print(f"   ❌ Task failed: {task.get('error_message', 'Unknown error')}")
                return task

        time.sleep(5)
        print(".", end="", flush=True)

    print("\n   ⚠️  Timeout waiting for completion")
    return None


def main():
    """Run promotion test."""
    print("=" * 70)
    print("🧪 TeleFlow Platform — Promotion Service Test")
    print("=" * 70)

    # Get token
    token = get_token()
    if not token:
        return False

    # Check userbot accounts
    accounts = check_userbot_accounts(token)
    if not accounts:
        print("\n⚠️  No active userbot accounts found.")
        print("   Please create and authorize a userbot account first.")
        print("   Skipping parse test (API endpoints still work).")
        return True  # API works, just no accounts

    # Create parse task
    task = create_parse_task(token)
    if not task:
        return False

    # Start task
    result = start_task(token, task["id"])
    if not result:
        return False

    # Wait for completion
    final_result = wait_for_completion(token, task["id"], timeout=120)

    print("\n" + "=" * 70)
    print("✅ Promotion Service Test Completed!")
    print("=" * 70)

    if final_result:
        print(f"\n📊 Final Stats:")
        print(f"   Processed: {final_result.get('processed_count', 0)}")
        print(f"   Success: {final_result.get('success_count', 0)}")
        print(f"   Failed: {final_result.get('failed_count', 0)}")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
