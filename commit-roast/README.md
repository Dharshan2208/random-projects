# Repo Commit Bot

A savage GitHub bot that fetches your latest commits, sends them to the **Groq AI**, and posts **ruthless roasts** as GitHub issue comments.
Because sometimes, your commit messages deserve to be humbled.

---

## What It Does

1. Fetches your latest commits using the **GitHub REST API**.
2. Sends each commit message to **Groq’s Llama 3** model for roasting.
3. Creates a new **GitHub issue** titled “ Repo Roast Bot Strikes!”
4. Posts each roast as a comment, tagging your commit SHA.

Example output:
```
Commit: fixed login bug
Roast: Congrats, you broke it first just to fix it. True developer vibes.
```

---

## Why?

- Because code reviews are too polite — and sometimes you need a bot that tells the *raw truth*.
  Perfect for friends, hackathons, or just trolling your own bad commit messages.
- Because I was frustrated by DSA as well as my life.
---

## Environment Variables

| Variable | Description |
|-----------|--------------|
| `GITHUB_TOKEN` | Personal Access Token with repo + issues write access |
| `GROQ_API_KEY` | Your Groq API key |
| `REPO_NAME` | Repository in `username/repo` format |

---

**Note:**
 - Your GitHub token must have `repo` and `issues:write` permissions.
 - If using a fine-grained token, enable *Read/Write access to Issues* and *Read access to Contents*.

---



