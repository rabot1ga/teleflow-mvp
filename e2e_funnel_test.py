#!/usr/bin/env python3
"""
TeleFlow Platform — Funnel E2E Test Script

Tests the funnel pipeline:
/start Command → Funnel Trigger → First Step Message
"""

import requests
import time

BASE_URL = "http://localhost"
AUTH_URL = f"{BASE_URL}:8001"
FUNNEL_URL = f"{BASE_URL}:8005"

def get_token():
    """Login and get access token."""
    print("📝 Step 1: Getting auth token...")
    resp = requests.post(
        f"{AUTH_URL}/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    if resp.status_code == 200:
        token = resp.json()["data"]["access_token"]
        print(f"   ✅ Token received")
        return token
    else:
        print(f"   ❌ Login failed: {resp.text}")
        return None


def create_funnel(token):
    """Create test funnel."""
    print("\n🎯 Step 2: Creating test funnel...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{FUNNEL_URL}/api/v1/funnels/funnels",
        headers=headers,
        json={
            "project_id": "test-project",
            "name": "E2E Test Funnel",
            "trigger_type": "command",
            "trigger_value": "/start",
            "is_active": True
        }
    )
    if resp.status_code == 200:
        funnel = resp.json()["data"]
        print(f"   ✅ Funnel created: {funnel['id']}")
        print(f"      Name: {funnel['name']}")
        return funnel
    else:
        print(f"   ❌ Funnel creation failed: {resp.text}")
        return None


def create_lead_magnet(token):
    """Create test lead magnet."""
    print("\n🎁 Step 3: Creating lead magnet...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{FUNNEL_URL}/api/v1/funnels/lead-magnets",
        headers=headers,
        json={
            "project_id": "test-project",
            "name": "E2E Test Lead Magnet",
            "type": "text",
            "text_content": "🎉 Ваш бонус: секретный материал!",
            "delivery_message": "🎁 Вот ваш лид-магнит:\n\n{text_content}",
            "require_subscription": False
        }
    )
    if resp.status_code == 200:
        magnet = resp.json()["data"]
        print(f"   ✅ Lead magnet created: {magnet['id']}")
        return magnet
    else:
        print(f"   ❌ Lead magnet creation failed: {resp.text}")
        return None


def test_trigger_funnel():
    """Test funnel trigger via internal API."""
    print("\n🚀 Step 4: Testing funnel trigger...")
    resp = requests.post(
        f"{FUNNEL_URL}/funnels/trigger",
        json={
            "telegram_user_id": 123456789,
            "trigger_type": "command",
            "trigger_value": "/start"
        }
    )
    if resp.status_code == 200:
        result = resp.json()
        if result.get("data", {}).get("triggered"):
            print(f"   ✅ Funnel triggered!")
            print(f"      Funnel: {result['data'].get('funnel_name', 'N/A')}")
            return result["data"]
        else:
            print(f"   ⚠️  Funnel not triggered: {result['data'].get('reason', 'unknown')}")
            return None
    else:
        print(f"   ❌ Trigger failed: {resp.text}")
        return None


def check_bot_status():
    """Check if bot is running."""
    print("\n🤖 Step 5: Checking bot status...")
    resp = requests.get(f"{BASE_URL}:8006/health")
    if resp.status_code == 200:
        print(f"   ✅ Bot Gateway is healthy")
        return True
    else:
        print(f"   ❌ Bot Gateway not healthy")
        return False


def main():
    """Run E2E test."""
    print("=" * 60)
    print("🚀 TeleFlow Platform Funnel E2E Test")
    print("=" * 60)
    
    # Get token
    token = get_token()
    if not token:
        return False
    
    # Create funnel
    funnel = create_funnel(token)
    if not funnel:
        return False
    
    # Create lead magnet
    magnet = create_lead_magnet(token)
    # Continue even if magnet creation fails
    
    # Test trigger
    result = test_trigger_funnel()
    
    # Check bot status
    check_bot_status()
    
    print("\n" + "=" * 60)
    print("✅ Funnel E2E Test Completed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
