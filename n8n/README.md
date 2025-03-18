# n8n Workflows

This directory contains n8n workflow configurations for the project.

## PR Review Workflow

The PR Review workflow automatically reviews pull requests using AI and posts the review as a comment.

### Setup Instructions

1. Install n8n:

   ```bash
   npm install n8n -g
   ```

2. Start n8n:

   ```bash
   n8n start
   ```

3. Import the workflow:

   - Open n8n at http://localhost:5678
   - Go to Workflows
   - Click "Import from File"
   - Select `workflows/pr-review.json`

4. Configure Credentials:

   - Add OpenAI API credentials
   - Add GitHub credentials with PR review permissions

5. Get the Webhook URL:

   - Click on the Webhook node
   - Click "Execute Node"
   - Copy the webhook URL

6. Add the webhook URL to GitHub Secrets:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets and variables > Actions
   - Add a new secret named `N8N_WEBHOOK_URL`
   - Paste the webhook URL

### Workflow Components

1. **Webhook Node**

   - Receives PR data from GitHub Actions
   - Path: `pr-review`

2. **OpenAI Node**

   - Reviews the PR using GPT-4
   - Provides detailed analysis of:
     - Code quality
     - Security considerations
     - Performance implications
     - Suggested improvements
     - Best practices

3. **GitHub Node**
   - Posts the AI review as a comment on the PR
   - Uses markdown formatting for better readability

### Customization

You can customize the workflow by:

1. Modifying the OpenAI prompt in the workflow file
2. Adjusting the temperature and max tokens
3. Adding additional nodes for:
   - Code style checking
   - Security scanning
   - Performance testing
   - Documentation generation

### Troubleshooting

1. If the webhook isn't receiving data:

   - Check the GitHub Actions logs
   - Verify the webhook URL is correct
   - Ensure the secret is properly set

2. If OpenAI fails:

   - Verify API credentials
   - Check token limits
   - Review the prompt format

3. If GitHub posting fails:
   - Verify GitHub credentials
   - Check repository permissions
   - Review the PR number format
