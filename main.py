from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
import base64

mcp = FastMCP("github_server")

load_dotenv()

GITHUB_API_BASE = "https://api.github.com"
class GithubClient:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, path, params=None):
        url = f"{GITHUB_API_BASE}{path}"
        resp = requests.get(url, headers=self.headers, params=params)

        return resp.json()
    

client = GithubClient()
@mcp.tool()
def list_repos():
    """
    Lists the repositories of the authenticated user.
    """
    repos = client.get("/user/repos?per_page=100")
    return [
        {
            "name": r["name"],
            "full_name": r["full_name"],
            "private": r["private"],
            "url": r["html_url"]
        }
        for r in repos
    ]

# we wont need this after the repo tree function is built
@mcp.tool()
def list_files_in_repos(repo_name):
    """
    Lists the files in a selected repository of the authenticated user.
    """
    user = client.get("/user")
    owner = user["login"]
    contents = client.get(f"/repos/{owner}/{repo_name}/contents")
    return [
        {
            "name": item["name"],
            "path": item["path"],
            "type": item["type"],
            "download_url": item.get("download_url")
        }
        for item in contents
    ]
# change get_file_content to take path as parameter
@mcp.tool()
def get_file_content(repo_name, path):
    """
    Gets content of specific file according to user's need.
    """
    # GET /repos/{owner}/{repo}/contents/{path}
    user = client.get("/user")
    owner = user["login"]
    response = client.get(f"/repos/{owner}/{repo_name}/contents/{path}")

    if "content" not in response:
        return {"path": path, "content": None}
    
    if response["size"] > 200_000:
        return {"path": path, "content": None, "too_large": True}
    content = base64.b64decode(response["content"]).decode("utf8")

    return {
        "path": response["path"],
        "content": content
    }

@mcp.tool()
def get_repo_tree(repo_name, path="", max_depth=4):
    """
    Gets repo tree with max_depth of 4.
    """
    max_depth = int(max_depth)
    IGNORE = {".venv",".env", "__pycache__", ".git", ".gitignore", "venv", "node_modules", "dist", "build", "migrations"}
    user = client.get("/user")
    owner = user["login"]
    # contents = client.get(f"/repos/{owner}/{repo_name}/contents/{path}")
    depth = 0
    def get_tree(current_path, depth):

        nodes = []
        content = client.get(f"/repos/{owner}/{repo_name}/contents/{current_path}")
        if not isinstance(content, list):
            return []
        for item in content:
            if item["name"] in IGNORE:
                continue
            if item["type"] == "file":
                nodes.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": item['type']
                })
            elif item["type"] == "dir":
                if depth < max_depth:
                    sub_tree = get_tree(item["path"], depth+1)
                    nodes.append({
                        "name": item["name"],
                        "path": item["path"],
                        "type": item["type"],
                        "children": sub_tree
                    })

            else:
                pass

        return nodes
    
    return get_tree(path, depth)

if __name__ == "__main__":
    
    user = client.get("/user")
    print(user["login"])
    mcp.run(host="0.0.0.0", port=8000)


