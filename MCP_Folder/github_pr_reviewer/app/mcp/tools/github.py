from fastmcp import FastMCP
from app.services.github_service import GitHubService

mcp = FastMCP("pr-reviewer")
#this is mcp server instance

github_service = GitHubService()

@mcp.tool()
#This function is available to AI
async def get_pr_diff(pr_url: str) -> str:
    """
    Fetch the diff of a GitHub Pull Request.
    Use this when you need to analyze code changes.
    """
    return await github_service.get_pr_diff(pr_url)