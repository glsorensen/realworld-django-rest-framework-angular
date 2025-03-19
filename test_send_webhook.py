#!/usr/bin/env python3
import requests
import sys
import json
import os

def send_test_webhook(webhook_url=None):
    """Send a mock GitHub PR webhook event."""
    
    if not webhook_url:
        print("Error: Please provide the webhook URL")
        print("Usage: python test_send_webhook.py https://example.hooks.n8n.cloud/webhook/path")
        return 1
    
    # Try to load the mock PR data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mock_file_path = os.path.join(script_dir, 'mock-github-pr.json')
    
    try:
        with open(mock_file_path, 'r') as f:
            mock_data = json.load(f)
            print(f"Loaded mock data from {mock_file_path}")
    except FileNotFoundError:
        print(f"Mock file not found at {mock_file_path}, using simple test data instead")
        # Simple test payload as fallback
        mock_data = {
            "event": "test",
            "message": "This is a test webhook payload",
            "timestamp": "2023-06-01T12:00:00Z"
        }
    except json.JSONDecodeError:
        print("Invalid JSON in mock file, using simple test data instead")
        mock_data = {
            "event": "test",
            "message": "This is a test webhook payload",
            "timestamp": "2023-06-01T12:00:00Z"
        }
    
    # Send the webhook request
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'GitHub-Webhook-Mock'
    }
    
    try:
        print(f"Sending webhook to {webhook_url}...")
        response = requests.post(webhook_url, json=mock_data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Success! Webhook sent successfully.")
        else:
            print(f"Warning: Webhook responded with status code {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Error: Failed to send webhook: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(send_test_webhook(webhook_url)) 