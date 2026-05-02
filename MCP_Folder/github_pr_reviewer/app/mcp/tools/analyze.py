#in this file we are building
# A function that:
# Sends PR URL to AI
# Gives AI access to your MCP tool (get_pr_diff)
# AI decides:
# call tool
# read diff
# generate review

import os
from fastmcp import FastMCP
from app.mcp.tools.github import mcp  # reuse same MCP instance
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@mcp.tool()
async def analyze_pr(pr_url: str) -> dict:
    """
    Analyze a GitHub PR and provide:
    - summary
    - risk level
    - suggestions
    """

    response = await client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=2000,
        tools=mcp.get_tools(),  # give ALL tools to AI
        messages=[
            {
                "role": "user",
                "content": f"""
                Review this GitHub PR: {pr_url}

                Provide:
                - summary
                - risk level (low/medium/high)
                - key issues
                - suggestions
                """
            }
        ],
    )

    return response.content

    #so basicaly this will be the agentic loop
    #Step 1 → sees PR URL
    #Step 2 → thinks: I need diff
    #Step 3 → calls get_pr_diff
    #Step 4 → reads result
    #Step 5 → writes review