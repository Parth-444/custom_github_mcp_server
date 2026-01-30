# GitHub Repo File Explorer (MCP Tool)

This project provides simple MCP tools to interact with a GitHub repository using the GitHub REST API.

## Features

- Authenticate using a GitHub token

- List files in the root of a user-owned repository

- Fetch and read the content of a specific file (e.g. README.md)

## Current Scope

- Works only with repositories owned by the authenticated user

- Assumes simple repo structures (no orgs, no forks, no deep recursion)

- Designed for lightweight, LLM-friendly responses

## Tools

- list_files_in_repos(repo_name) – Lists files and folders in the repository root

- get_file_content(repo_name, file_name) – Fetches and returns decoded file content

## Notes

- File contents are automatically Base64-decoded

- Intended as a minimal, extensible foundation for MCP-based GitHub tooling
