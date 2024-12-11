import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

GITHUB_API_URL = "https://api.github.com"

def create_github_issue(repo_owner, repo_name, title, body, token=None):
    """
    Create a GitHub issue in a specified repository.
    """
    token = token or getattr(settings, "GITHUB_ACCESS_TOKEN", None)
    if not token:
        raise ValueError("GitHub Access Token is required")

    url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": f"Failed to create issue: {response.status_code}",
            "details": response.json()
        }

@csrf_exempt
def create_issue_view(request):
    """
    Django view to create a GitHub issue via POST request.
    Expects JSON data with 'title' and 'body' fields.
    """
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            title = data.get("title")
            body = data.get("body")

            # Validate the required fields
            if not title or not body:
                return JsonResponse({"error": "Title and body are required"}, status=400)

            # Repository details (replace with your own repo information)
            repo_owner = "your-github-username"
            repo_name = "your-repo-name"

            # Call the function to create the GitHub issue
            result = create_github_issue(repo_owner, repo_name, title, body)

            # Return success or error response
            if "error" not in result:
                return JsonResponse({
                    "message": "Issue created successfully",
                    "issue_url": result.get("html_url")
                }, status=201)
            else:
                return JsonResponse({
                    "error": result["error"],
                    "details": result["details"]
                }, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
