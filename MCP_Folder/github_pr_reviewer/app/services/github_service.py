#this is the github layer, it will handle the github api calls (the class)
import httpx
import re
import os

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")

    def parse_pr_url(self, pr_url:str):
#owner = user
# repo = repo
# pr_number = 45

# Why?
# 👉 GitHub API needs this format
        """
        Extract owner, repo, PR number from URL
        Example:
        https://github.com/owner/repo/pull/123
        """
        pattern = r"https://github.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.search(pattern, pr_url)
        if not match:
            raise ValueError("Invalid PR URL")
        owner, repo, pr_number = match.groups()
        return owner, repo, pr_number

    async def get_pr_diff(self, pr_url: str):
        owner, repo, pr_number = self.parse_pr_url(pr_url)

        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"

        headers = {
            "Accept": "application/vnd.github.v3.diff"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"GitHub API error: {response.text}")

            return response.text