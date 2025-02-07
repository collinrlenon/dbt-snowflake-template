import os
import sys
import requests
from typing import Optional


def get_pr_from_sha(sha: str, repo: str, token: str) -> Optional[str]:
    """
    Get PR number associated with a commit SHA using GitHub REST API.
    Returns PR number as string if found, empty string if not found, None if error.
    """
    try:
        # Split repo into owner/repo
        owner, repo_name = repo.split('/')
        
        # GitHub API endpoint
        url = f"https://api.github.com/repos/{owner}/{repo_name}/commits/{sha}/pulls"
        
        # Headers for GitHub API
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {token}"
        }
        
        # Make API request
        response = requests.get(url, headers=headers)
        
        # Check for rate limiting
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
            print(f"Error: GitHub API rate limit exceeded. Reset at: {response.headers['X-RateLimit-Reset']}", 
                  file=sys.stderr)
            return None
            
        # Check for successful response
        response.raise_for_status()
        
        # Parse response
        prs = response.json()
        
        # Return first PR number if any PRs found, empty string otherwise
        return str(prs[0]['number']) if prs else ''
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None


def main():
    # Get required environment variables
    sha = os.getenv('GITHUB_COMMIT_SHA')
    repo = os.getenv('GITHUB_REPOSITORY')
    token = os.getenv('GITHUB_TOKEN')
    
    # Validate environment variables
    if not all([sha, repo, token]):
        print("Error: Missing required environment variables (GITHUB_SHA, GITHUB_REPOSITORY, or GITHUB_TOKEN)", 
              file=sys.stderr)
        sys.exit(1)
    
    # Get PR number
    pr_number = get_pr_from_sha(sha, repo, token)
    
    if pr_number is None:
        # Error occurred, exit with non-zero status
        sys.exit(1)
    
    # Print PR number (or empty string) to stdout
    print(pr_number)


main()