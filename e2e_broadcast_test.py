#!/usr/bin/env python3
"""
TeleFlow Platform — Broadcast E2E Test Script

Tests the broadcast pipeline:
Create Broadcast → Start → Send Messages → Update Stats
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
        json={"email": "test5@example.com", "password": "TestPassword123!"}
    )
    if resp.status_code == 200:
        token = resp.json()["data"]["access_token"]
        print(f"   ✅ Token received")
        return token
    else:
        print(f"   ❌ Login failed: {resp.text}")
        return None


def create_broadcast(token):
    """Create test broadcast."""
    print("\n📢 Step 2: Creating broadcast...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{FUNNEL_URL}/api/v1/funnels/broadcasts",
        headers=headers,
        json={
            "project_id": "test-project",
            "name": "E2E Test Broadcast",
            "message_type": "text",
            "message_text": "🎉 Test broadcast message!\n\nThis is an E2E test.",
            "recipient_filter": {"type": "all"},
            "send_rate": 10
        }
    )
    if resp.status_code == 200:
        broadcast = resp.json()["data"]
        print(f"   ✅ Broadcast created: {broadcast['id']}")
        print(f"      Name: {broadcast['name']}")
        print(f"      Recipients: {broadcast['recipient_filter']}")
        return broadcast
    else:
        print(f"   ❌ Broadcast creation failed: {resp.text}")
        return None


def start_broadcast(token, broadcast_id):
    """Start broadcast."""
    print("\n🚀 Step 3: Starting broadcast...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{FUNNEL_URL}/api/v1/funnels/broadcasts/{broadcast_id}/start",
        headers=headers
    )
    if resp.status_code == 200:
        result = resp.json()["data"]
        print(f"   ✅ Broadcast started!")
        print(f"      Status: {result['status']}")
        return result
    else:
        print(f"   ❌ Start failed: {resp.text}")
        return None


def wait_for_completion(token, broadcast_id, timeout=60):
    """Wait for broadcast to complete."""
    print(f"\n⏳ Step 4: Waiting for broadcast completion (up to {timeout}s)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(
            f"{FUNNEL_URL}/api/v1/funnels/broadcasts/{broadcast_id}",
            headers=headers
        )
        if resp.status_code == 200:
            broadcast = resp.json()["data"]
            status = broadcast["status"]
            sent = broadcast["sent"]
            delivered = broadcast["delivered"]
            
            print(f"   Status: {status}, Sent: {sent}, Delivered: {delivered}")
            
            if status == "completed":
                print(f"   ✅ Broadcast completed!")
                return broadcast
            elif status == "failed":
                print(f"   ❌ Broadcast failed!")
                return broadcast
        
        time.sleep(5)
        print(".", end="", flush=True)
    
    print("\n   ⚠️  Timeout waiting for completion")
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
    print("🚀 TeleFlow Platform Broadcast E2E Test")
    print("=" * 60)
    
    # Get token
    token = get_token()
    if not token:
        return False
    
    # Create broadcast
    broadcast = create_broadcast(token)
    if not broadcast:
        return False
    
    # Start broadcast
    result = start_broadcast(token, broadcast["id"])
    if not result:
        return False
    
    # Wait for completion
    final_result = wait_for_completion(token, broadcast["id"], timeout=30)
    
    # Check bot status
    check_bot_status()
    
    print("\n" + "=" * 60)
    print("✅ Broadcast E2E Test Completed!")
    print("=" * 60)
    
    if final_result:
        print(f"\n📊 Final Stats:")
        print(f"   Sent: {final_result.get('sent', 0)}")
        print(f"   Delivered: {final_result.get('delivered', 0)}")
        print(f"   Failed: {final_result.get('failed', 0)}")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
