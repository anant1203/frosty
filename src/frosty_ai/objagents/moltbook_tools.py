"""
Moltbook tools — lets Frosty post, read feeds, and check its dashboard on
https://www.moltbook.com, the social network for AI agents.

The MOLTBOOK_API_KEY environment variable must be set.
"""

import os
import re
import json
import urllib.request
import urllib.error
from google.adk.tools import ToolContext  # noqa: F401  (kept for type hints if needed)

_BASE = "https://www.moltbook.com/api/v1"

_WORD_TO_NUM = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100,
}


def _api_key() -> str:
    key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not key:
        raise ValueError("MOLTBOOK_API_KEY is not set in environment")
    return key


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def _deobfuscate(text: str) -> str:
    """Strip Moltbook's obfuscation characters and normalise to lowercase."""
    # Remove symbol noise: [], ^, /, and hyphens between letters
    cleaned = re.sub(r'[\[\]^/]', ' ', text)
    cleaned = re.sub(r'-(?=[a-zA-Z])', ' ', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip().lower()


def _text_to_number(word: str) -> float | None:
    """Convert a written English number to float, e.g. 'twenty' → 20.0."""
    if re.match(r'^\d+(\.\d+)?$', word):
        return float(word)
    return float(_WORD_TO_NUM[word]) if word in _WORD_TO_NUM else None


def _solve_challenge(challenge_text: str) -> str:
    """
    Parse and solve a Moltbook math verification challenge.

    Challenges are obfuscated word problems with two numbers and one operation.
    Example: 'A] lO^bSt-Er S[wImS aT tW]eNn-Ty mE^tE[rS aNd] SlO/wS bY^ fI[vE'
             → 'a lobster swims at twenty meters and slows by five' → 20 - 5 = 15.00
    """
    text = _deobfuscate(challenge_text)

    # Identify operation from keywords
    if any(w in text for w in ("plus", "adds", "add", "sum", "faster", "gains", "increases")):
        op = "+"
    elif any(w in text for w in ("minus", "subtract", "slows", "slower", "less", "loses", "decreases", "drops")):
        op = "-"
    elif any(w in text for w in ("times", "multiplied", "multiply", "product")):
        op = "*"
    elif any(w in text for w in ("divided", "divides", "splits", "half")):
        op = "/"
    else:
        op = "+"

    # Collect all numbers (digit or word form) in order
    tokens = text.split()
    numbers: list[float] = []
    for token in tokens:
        token_clean = re.sub(r'[^a-z0-9.]', '', token)
        n = _text_to_number(token_clean)
        if n is not None:
            numbers.append(n)
        if len(numbers) == 2:
            break

    if len(numbers) < 2:
        return "0.00"

    a, b = numbers[0], numbers[1]
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        result = a / b if b != 0 else 0.0

    return f"{result:.2f}"


def _handle_verification(post_response: dict) -> dict:
    """If a verification challenge is present, solve and submit it."""
    post_obj = post_response.get("post") or post_response.get("comment") or post_response.get("submolt") or {}
    verification = post_obj.get("verification")
    if not verification:
        return post_response  # already published (trusted agent)

    answer = _solve_challenge(verification["challenge_text"])
    verify_resp = _request("POST", "/verify", {
        "verification_code": verification["verification_code"],
        "answer": answer,
    })
    post_response["_verification_result"] = verify_resp
    return post_response


# ── Public tools ──────────────────────────────────────────────────────────────

def moltbook_post(title: str, content: str, submolt_name: str = "general") -> dict:
    """
    Create a post on Moltbook — the social network for AI agents.

    Use this to share what Frosty just did, announce new features, ask the
    agent community questions, or start discussions.

    Args:
        title: Post title (max 300 chars).
        content: Post body text (max 40,000 chars). Optional but recommended.
        submolt_name: Community to post in (default: 'general').
                      Other common ones: 'snowflake', 'datawrangling', 'aithoughts'.

    Returns:
        Dict with success status and post details.
    """
    resp = _request("POST", "/posts", {
        "submolt_name": submolt_name,
        "title": title,
        "content": content,
    })
    return _handle_verification(resp)


def moltbook_get_comments(post_id: str, sort: str = "best") -> dict:
    """
    Get comments on a Moltbook post.

    Use this after moltbook_get_home() shows activity on one of Frosty's posts
    to read what people said before replying.

    Args:
        post_id: The post ID (from the home dashboard or feed response).
        sort: 'best' (default, most upvoted), 'new', or 'old'.

    Returns:
        Dict with a tree of comments and their replies.
    """
    return _request("GET", f"/posts/{post_id}/comments?sort={sort}&limit=50")


def moltbook_comment(post_id: str, content: str, parent_id: str = "") -> dict:
    """
    Add a comment or reply to a Moltbook post.

    Use this to reply to comments on Frosty's posts or to join discussions
    on other agents' posts.

    Args:
        post_id: The post to comment on.
        content: The comment text.
        parent_id: If replying to a specific comment, pass its comment ID.
                   Leave empty to add a top-level comment on the post.

    Returns:
        Dict with success status and comment details.
    """
    body: dict = {"content": content}
    if parent_id:
        body["parent_id"] = parent_id
    resp = _request("POST", f"/posts/{post_id}/comments", body)
    return _handle_verification(resp)


def moltbook_get_feed(sort: str = "hot", limit: int = 10) -> dict:
    """
    Fetch the Moltbook global feed.

    Args:
        sort: 'hot' (default), 'new', 'top', or 'rising'.
        limit: Number of posts to return (default 10, max 25).

    Returns:
        Dict with a list of posts.
    """
    return _request("GET", f"/posts?sort={sort}&limit={limit}")


def moltbook_get_home() -> dict:
    """
    Fetch the Moltbook home dashboard for FrostyAI.

    Returns a summary of: unread notifications, activity on Frosty's posts,
    posts from followed agents, and suggested next actions.
    """
    return _request("GET", "/home")
