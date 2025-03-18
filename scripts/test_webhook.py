import requests
import json

# Updated webhook URL to use production endpoint
WEBHOOK_URL = "http://localhost:5678/webhook-test/pr-review"

# Mock GitHub PR event payload with more complete structure
test_payload = {
    "pull_request": {
        "title": "Test PR: Add new feature",
        "body": "This is a test pull request to verify the AI review workflow.",
        "number": 1,
        "additions": 10,
        "deletions": 5,
        "changed_files": 2,  # Changed to integer as GitHub API expects
        "files": [
            {
                "filename": "src/test.py",
                "status": "modified",
                "additions": 5,
                "deletions": 2,
                "changes": 7
            },
            {
                "filename": "README.md",
                "status": "modified",
                "additions": 5,
                "deletions": 3,
                "changes": 8
            }
        ]
    },
    "repository": {
        "owner": {
            "login": "glsorensen"  # GitHub API uses owner.login
        },
        "name": "realworld-django-rest-framework-angular"
    },
    "action": "opened"  # Added to indicate this is a new PR
}

def test_webhook():
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=test_payload,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Event": "pull_request"  # Added GitHub event header
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)  # Print raw response if not JSON
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPlease verify:")
        print("1. n8n is running at http://localhost:5678")
        print("2. The workflow is activated in n8n")
        print("3. The webhook URL matches the one shown in n8n's Webhook node")
        print("4. OpenAI API key is configured in n8n")

if __name__ == "__main__":
    print(f"Sending test request to: {WEBHOOK_URL}")
    test_webhook() 