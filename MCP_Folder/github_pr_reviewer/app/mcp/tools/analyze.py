#in this file we are building
# A function that:
# Sends PR URL to AI
# Gives AI access to your MCP tool (get_pr_diff)
# AI decides:
# call tool
# read diff
# generate review

import os
import json
from app.mcp.tools.github import mcp  # reuse same MCP instance
from groq import AsyncGroq

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


# NOTE: This is NOT an MCP tool — it's a regular async function
# called by the FastAPI route. Only get_pr_diff is an MCP tool.
async def analyze_pr(pr_url: str) -> dict:
    """
    Analyze a GitHub PR and provide:
    - summary
    - risk level
    - suggestions
    """

    # Get MCP tools and convert to Groq/OpenAI function-calling format
    mcp_tools = await mcp.list_tools()
    groq_tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters
            }
        }
        for t in mcp_tools
    ]

    messages = [
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
    ]

    # Agentic loop: keep going until the LLM stops requesting tools
    while True:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            tools=groq_tools,
            messages=messages,
        )

        choice = response.choices[0]
        message = choice.message

        # If the LLM is done (no tool calls), return its final answer
        if choice.finish_reason == "stop" or not message.tool_calls:
            return {"review": message.content}

        # If the LLM wants to use a tool, execute it and feed result back
        if choice.finish_reason == "tool_call":
            # Add assistant's message (with tool_calls) to conversation
            messages.append(message)

            # Process each tool call
            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                # Execute the tool via MCP
                tool_result = await mcp.call_tool(fn_name, fn_args)

                # Feed tool result back as a tool message
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
        else:
            # Unexpected finish reason, return whatever we have
            return {"review": message.content or str(message)}

    # Agentic loop flow:
    # Step 1 → LLM sees PR URL
    # Step 2 → LLM thinks: I need the diff
    # Step 3 → LLM calls get_pr_diff tool
    # Step 4 → We execute it and feed result back
    # Step 5 → LLM reads the diff and writes review
    # Step 6 → We return the final review