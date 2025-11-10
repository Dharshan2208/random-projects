import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPO_NAME = os.getenv("REPO_NAME", "owner/repo")

GITHUB_API_BASE = "https://api.github.com"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_commit_messages(repo_name, num_commits=5):
    """Fetch latest commit messages using GitHub REST API."""
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/commits"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    try:
        response = requests.get(url, headers=headers, params={"per_page": num_commits})
        response.raise_for_status()
        commits = response.json()

        messages = [(c["sha"], c["commit"]["message"]) for c in commits]
        return messages
    except Exception as e:
        print(f"Error fetching commits: {e}")
        return []


def roast_commit(message):
    """Send commit message to Groq model for roasting."""
    prompt = (
        f"You're a brutally sarcastic AI roaster. First, show the commit message clearly, "
        f"then roast it immediately after with dark humor, coder sarcasm, and ruthless honesty. "
        f"Keep the roast under 100 characters. No kindness. "
        f"Commit message: '{message}'"
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.9,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error roasting commit: {e}")
        return "This commit is so bad even Bot gave up."


def post_roasts_to_issue(repo_name, roasts):
    """Create a GitHub issue and post roast comments."""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    issue_url = f"{GITHUB_API_BASE}/repos/{repo_name}/issues"
    issue_data = {
        "title": "Repo Commit Roast !!!",
        "body": "Brace yourselves... ",
    }

    try:
        issue_response = requests.post(issue_url, headers=headers, json=issue_data)
        issue_response.raise_for_status()
        issue = issue_response.json()
        issue_number = issue["number"]

        # Add roasts as comments
        for sha, roast in roasts:
            comment_url = (
                f"{GITHUB_API_BASE}/repos/{repo_name}/issues/{issue_number}/comments"
            )
            comment_data = {"body": f"Commit `{sha[:7]}`: {roast}"}
            requests.post(comment_url, headers=headers, json=comment_data)

        return issue["html_url"]
    except Exception as e:
        print(f"Error posting issue/comments: {e}")
        return None


def main():
    num_commits = 3
    commits = get_commit_messages(REPO_NAME, num_commits)

    if not commits:
        print("No commits found or error occurred.")
        return

    print(f"Found {len(commits)} commits. Generating roasts...")
    roasts = [(sha, roast_commit(msg)) for sha, msg in commits]

    issue_url = post_roasts_to_issue(REPO_NAME, roasts)
    if issue_url:
        print(f"Roasts posted successfully: {issue_url}")
    else:
        print("Failed to post roasts.")


if __name__ == "__main__":
    main()
