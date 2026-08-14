import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from reviewer import review_pull_request

load_dotenv()

app = FastAPI(title="GitHub PR Reviewer API")

@app.get("/")
def health_check():
    return {"status": "Agent is running locally and ready!"}

@app.post("/webhook/pr")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()
        
        # Check if the event is a pull request action
        if "pull_request" in payload:
            action = payload.get("action")
            pr_number = payload["pull_request"]["number"]
            repo_name = payload["repository"]["full_name"]
            
            # Trigger review when a PR is opened, reopened, or has new commits pushed
            if action in ["opened", "reopened", "synchronize"]:
                print(f"🚀 Triggering AI review for PR #{pr_number} ({action}) in {repo_name}")
                background_tasks.add_task(review_pull_request, repo_name, pr_number)
                return {"status": "processing", "message": f"Review initiated for PR #{pr_number}"}
            
            return {"status": "ignored", "message": f"PR action '{action}' does not require a review."}
            
        return {"status": "ignored", "message": "Not a pull request event."}
        
    except Exception as e:
        print(f"❌ Error handling webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")