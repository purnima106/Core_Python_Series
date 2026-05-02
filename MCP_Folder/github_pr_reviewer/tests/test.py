import asyncio
from app.services.github_service import GitHubService

async def main():
    service = GitHubService()
    diff = await service.get_pr_diff(
        "https://github.com/python/cpython/pull/1"
    )
    print(diff[:1000])  # print first part

asyncio.run(main())