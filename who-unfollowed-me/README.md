# Who Unfollowed Me on GitHub?

This Python script helps you track who unfollows you on GitHub.It fetches your current followers, compares them with previous day's record, and sends you an email notification if any unfollowers are detected.(Peak Joblessness)


## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Dharshan2208/who-unfollowed-me.git
    cd who-unfollowed-me
    ```

2.  **Create a virtual environment and activate it (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory of the project based on the `.env.example` file:

```
GITHUB_USERNAME = "your_github_username"
GITHUB_TOKEN = "your_github_personal_access_token"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "your_email@gmail.com"
```

*   **`GITHUB_USERNAME`**: Your GitHub username.
*   **`GITHUB_TOKEN`**: A GitHub Personal Access Token (PAT) with `user:follow` scope. You can generate one [here](https://github.com/settings/tokens). This is crucial to avoid API rate limits.
*   **`EMAIL_SENDER`**: The email address from which notifications will be sent (e.g., your Gmail address).
*   **`EMAIL_PASSWORD`**: The app password for your sender email. For Gmail, you'll need to generate an **App Password** if you have 2-Factor Authentication enabled.
*   **`EMAIL_RECEIVER`**: The email address where you want to receive unfollower notifications.

## Usage

To run the script, simply execute `main.py`:

```bash
python main.py
```

It's recommended to set up a scheduled task (e.g., using `cron` on Linux/macOS or Task Scheduler on Windows) to run this script daily.

### Example `cron` setup (Linux):

1.  Open your crontab for editing:
    ```bash
    crontab -e
    ```
2.  Add the following line to run the script daily at a specific time (e.g., 08:00 AM):
    ```cron
    0 8 * * * /usr/bin/python3 /path/to/your/who-unfollowed-me/main.py >> /path/to/your/who-unfollowed-me/cron.log 2>&1
    ```
    *   Replace `/usr/bin/python3` with the path to your Python interpreter (you can find it using `which python3` or `which python` in your activated virtual environment).
    *   Replace `/path/to/your/who-unfollowed-me/` with the actual path to your project directory.
    *   The `>> cron.log 2>&1` part redirects output to a log file, which is useful for debugging.

## Note

- I created this because I noticed some people unfollowing me, and I wanted a way to know who they were.
- I am jobless....so made this