#!/usr/bin/env python3
import json
import requests
import sys
import os

def send_mock_pr(webhook_url=None):
    """Send a mock GitHub PR webhook event to the n8n webhook."""
    
    if not webhook_url:
        print("Error: Please provide the n8n webhook URL")
        print("Usage: python send_mock_pr.py http://localhost:5678/webhook/pr-review")
        return 1
    
    # Load the mock PR data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mock_file_path = os.path.join(os.path.dirname(script_dir), 'mock-github-pr.json')
    
    try:
        with open(mock_file_path, 'r') as f:
            mock_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Mock file not found at {mock_file_path}")
        return 1
    except json.JSONDecodeError:
        print("Error: Invalid JSON in mock file")
        return 1
    
    # Send the webhook request
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'GitHub-Webhook-Mock'
    }
    
    try:
        response = requests.post(webhook_url, json=mock_data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Success! Mock PR webhook sent successfully.")
        else:
            print(f"Warning: Webhook responded with status code {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Error: Failed to send webhook: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(send_mock_pr(webhook_url)) 