import json
import re
from fnmatch import fnmatch
from github import Github, GithubException
from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper
from src.config import Config
from src.utils.logger import logger


@ActionRegistry.register("pull_review", "Review the pull request of github")
class PullReviewAction(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        try:
            # Extract PR details and initialize GitHub client
            pr_details = self._extract_pr_details(message)
            if not pr_details:
                return "Please provide a valid GitHub pull request URL."

            pr = self._get_pull_request(pr_details)
            pr_details.update(self._get_pr_details(pr))

            # Analyze files and collect comments
            all_comments = self._analyze_pr_files(pr, pr_details, web_helper)

            # Create review comments and return result
            return self._process_review_comments(pr, pr_details, all_comments)

        except Exception as e:
            logger.error(f"An error occurred during the code review: {str(e)}", exc_info=True)
            return f"An error occurred during the code review: {str(e)}"

    def _extract_pr_details(self, message: str) -> dict:
        pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.search(pattern, message)
        if match:
            return {
                "owner": match.group(1),
                "repo": match.group(2),
                "pull_number": int(match.group(3)),
            }
        return None

    def _get_pull_request(self, pr_details: dict):
        """Initialize GitHub client and get pull request object"""
        owner = pr_details["owner"].lower()
        if owner not in ["saigon-tech", "saigontech"]:
            raise ValueError("I don't have permission to review this repository.")

        g = Github(Config.GITHUB_TOKEN)
        repo = g.get_repo(f"{pr_details['owner']}/{pr_details['repo']}")
        return repo.get_pull(pr_details["pull_number"])

    def _get_pr_details(self, pr):
        return {
            "title": pr.title,
            "description": pr.body or "",
        }

    def _should_exclude_file(self, file_name):
        exclude_patterns = Config.GITHUB_EXCLUDE_PATTERNS.split(",")
        return any(fnmatch(file_name, pattern.strip()) for pattern in exclude_patterns)

    def _analyze_pr_files(self, pr, pr_details: dict, web_helper: WebHelper) -> list:
        """Analyze files in the pull request and collect review comments"""
        all_comments = []
        for file in pr.get_files():
            if not self._should_exclude_file(file.filename):
                chunk = file.patch
                analysis = self._analyze_code(file, chunk, pr_details, web_helper)
                reviews = analysis.get("reviews", [])

                for review in reviews:
                    all_comments.append(
                        {
                            "path": file.filename,
                            "position": review["lineNumber"],
                            "body": review["reviewComment"],
                        }
                    )
        return all_comments

    def _create_prompt(self, file, chunk, pr_details):
        return f"""
Your task is to review pull requests. Instructions:
- Provide the response in following JSON format:
{{"reviews": [{{"lineNumber":  <line_number>, "reviewComment": "<review comment>"}}]}}
- Do not give positive comments or compliments.
- Provide comments and suggestions ONLY if there is something to improve,
    otherwise "reviews" should be an empty array.
- Write the comment in GitHub Markdown format.
- Use the given description only for the overall context and only comment the code.
- IMPORTANT: NEVER suggest adding comments to the code.
Review the following code diff in the file "{file.filename}" and take the pull request
title and description into account when writing the response.

Pull request title: {pr_details['title']}
Pull request description:
---
{pr_details['description']}
---
Git diff to review:

```diff
{chunk}
```
"""

    def _analyze_code(self, file, chunk, pr_details, web_helper: WebHelper):
        """Send code for AI analysis and parse the response"""
        prompt = self._create_prompt(file, chunk, pr_details)
        response = web_helper.query_ai(
            prompt,
            model="gpt-4o",
            system_message="You are a code review assistant.",
            max_tokens=4096,
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"reviews": []}

    def _create_review_comments(self, pr, comments):
        """Create review comments on the pull request"""
        try:
            pr.create_review(
                commit=pr.get_commits().reversed[0], comments=comments, event="COMMENT"
            )
        except GithubException as e:
            logger.error(f"Error creating review comments: {e}")

    def _process_review_comments(self, pr, pr_details: dict, all_comments: list) -> str:
        """Process review comments and return appropriate message"""
        if all_comments:
            self._create_review_comments(pr, all_comments)
            return (
                f"Code review completed for PR #{pr_details['pull_number']}. "
                f"{len(all_comments)} comments were added."
            )
        else:
            return f"Code review completed for PR #{pr_details['pull_number']}. No issues found."
