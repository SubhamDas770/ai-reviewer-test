import os
from github import Github
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize local Mistral 7B through Ollama
llm = OllamaLLM(model="mistral:7b", temperature=0.1)

def review_pull_request(repo_full_name: str, pr_number: int):
    """
    Fetches the PR diff, runs local Mistral review, and posts comments back to GitHub.
    """
    if not GITHUB_TOKEN:
        print("❌ Error: GITHUB_TOKEN is missing from .env")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    # 1. Extract changed files and patches
    files_changed = pr.get_files()
    diff_summary = []

    for f in files_changed:
        # Only review code files (skip lockfiles or large binaries)
        if f.filename.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java', '.cpp')):
            patch = f.patch if f.patch else "No patch content available."
            diff_summary.append(f"### File: `{f.filename}`\n```diff\n{patch}\n```")

    if not diff_summary:
        print("ℹ️ No reviewable source code files found in this PR.")
        return

    full_diff = "\n\n".join(diff_summary)

    # 2. Build the review prompt for Mistral
    prompt = f"""You are a Senior Staff Software Engineer performing a rigorous Pull Request code review.

Analyze the following Git diff carefully:
{full_diff}

Instructions:
1. Provide a concise overall summary of the changes.
2. Identify any potential bugs, edge cases, security vulnerabilities, or performance bottlenecks.
3. Highlight clean code improvements, best practices, or potential refactors.
4. Be constructive, precise, and format your output using clear Markdown headings and bullet points.

Your Code Review:
"""

    print(f"🤖 Sending PR #{pr_number} diff to Mistral 7B for analysis...")
    review_output = llm.invoke(prompt)

    # 3. Post the review as a comment on the PR
    comment_body = f"## 🤖 Automated AI Code Review (Mistral 7B)\n\n{review_output}\n\n---\n*Reviewed automatically by your local PR Reviewer Agent.*"
    
    pr.create_issue_comment(comment_body)
    print(f"✅ Successfully posted review comment to PR #{pr_number} in {repo_full_name}!")