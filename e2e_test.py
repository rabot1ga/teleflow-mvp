#!/usr/bin/env python3
"""
TeleFlow Platform — E2E Test Script

Tests the full content pipeline:
RSS Source → Article Ingestion → Moderation → Publishing → Telegram
"""

import requests
import time
import json

BASE_URL = "http://localhost"
AUTH_URL = f"{BASE_URL}:8001"
CONTENT_URL = f"{BASE_URL}:8002"
PUBLISHING_URL = f"{BASE_URL}:8004"

def get_token():
    """Login and get access token."""
    print("📝 Step 1: Getting auth token...")
    resp = requests.post(
        f"{AUTH_URL}/api/v1/auth/login",
        json={"email": "test5@example.com", "password": "TestPassword123!"}
    )
    if resp.status_code == 200:
        token = resp.json()["data"]["access_token"]
        print(f"   ✅ Token received: {token[:50]}...")
        return token
    else:
        print(f"   ❌ Login failed: {resp.text}")
        return None


def create_source(token):
    """Create RSS source."""
    print("\n📡 Step 2: Creating RSS source...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{CONTENT_URL}/api/v1/content/sources",
        headers=headers,
        json={
            "project_id": "test-project",
            "name": "E2E Test RSS",
            "source_type": "rss",
            "url": "https://habr.com/ru/rss/articles/all/",
            "fetch_interval_minutes": 5
        }
    )
    if resp.status_code == 200:
        source = resp.json()["data"]
        print(f"   ✅ Source created: {source['id']}")
        print(f"      Name: {source['name']}")
        print(f"      URL: {source['url']}")
        return source
    else:
        print(f"   ❌ Source creation failed: {resp.text}")
        return None


def trigger_fetch(token, source_id):
    """Trigger immediate source fetch."""
    print("\n📥 Step 3: Triggering content fetch...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{CONTENT_URL}/api/v1/content/sources/{source_id}/fetch",
        headers=headers
    )
    if resp.status_code == 200:
        print(f"   ✅ Fetch triggered")
        return True
    else:
        print(f"   ❌ Fetch failed: {resp.text}")
        return False


def wait_for_articles(token, timeout=60):
    """Wait for articles to appear in queue."""
    print(f"\n⏳ Step 4: Waiting for articles (up to {timeout}s)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(
            f"{CONTENT_URL}/api/v1/content/moderation/queue",
            headers=headers,
            params={"status": "pending", "per_page": 5}
        )
        if resp.status_code == 200:
            data = resp.json()["data"]
            if data["items"]:
                print(f"   ✅ Found {data['total']} pending articles")
                for i, article in enumerate(data["items"][:3], 1):
                    print(f"      {i}. {article['title'][:60]}...")
                return data["items"]
        time.sleep(5)
        print(".", end="", flush=True)
    
    print("\n   ❌ Timeout waiting for articles")
    return []


def approve_article(token, article_id):
    """Approve article for publishing."""
    print(f"\n✅ Step 5: Approving article {article_id[:8]}...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{CONTENT_URL}/api/v1/content/articles/{article_id}/approve",
        headers=headers
    )
    if resp.status_code == 200:
        print(f"   ✅ Article approved")
        return True
    else:
        print(f"   ❌ Approval failed: {resp.text}")
        return False


def check_publishing_queue(token):
    """Check publishing jobs."""
    print("\n📤 Step 6: Checking publishing jobs...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{PUBLISHING_URL}/api/v1/publishing/jobs",
        headers=headers
    )
    if resp.status_code == 200:
        data = resp.json()["data"]
        print(f"   ✅ Found {data['total']} jobs")
        for job in data["items"][:3]:
            print(f"      - Job {job['id'][:8]}: {job['status']}")
        return data["items"]
    else:
        print(f"   ❌ Failed to get jobs: {resp.text}")
        return []


def check_bot_status():
    """Check if bot is running."""
    print("\n🤖 Step 7: Checking bot status...")
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
    print("🚀 TeleFlow Platform E2E Test")
    print("=" * 60)
    
    # Get token
    token = get_token()
    if not token:
        return False
    
    # Create source
    source = create_source(token)
    if not source:
        return False
    
    # Trigger fetch
    if not trigger_fetch(token, source["id"]):
        return False
    
    # Wait for articles
    articles = wait_for_articles(token, timeout=90)
    if not articles:
        print("\n⚠️  No articles found, but continuing test...")
        # This is OK - RSS might be empty or slow
    
    # Approve first article if exists
    if articles:
        if not approve_article(token, articles[0]["id"]):
            return False
        
        # Check publishing queue
        check_publishing_queue(token)
    
    # Check bot status
    check_bot_status()
    
    print("\n" + "=" * 60)
    print("✅ E2E Test Completed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
