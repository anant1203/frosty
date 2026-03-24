import logging

from google.adk.tools import ToolContext


def web_search(query: str) -> str:
    """Search the web for information about the given query and return a concise summary."""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return "duckduckgo-search is not installed. Run: pip install duckduckgo-search"

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    if not results:
        return "No results found."

    return "\n\n".join(
        f"{r['title']}\n{r['body']}" for r in results
    )


def save_research_results(object_type: str, results: str, tool_context: ToolContext) -> dict:
    """
    Persist research results for a Snowflake object type into the shared session state
    under the key ``app:RESEARCH_RESULTS``.

    The state variable is a dictionary keyed by object type (e.g. ``"TABLE"``,
    ``"STREAM"``) so that downstream specialist agents can retrieve cached research
    without making a redundant web search.

    Args:
        object_type: The Snowflake object type the research covers (e.g. "TABLE",
            "WAREHOUSE", "STREAM").  Will be upper-cased automatically.
        results: The full research text to store.
        tool_context: ADK tool context carrying the shared session state.

    Returns:
        A dictionary with ``success`` (bool) and a confirmation message.
    """
    logger = logging.getLogger(__name__)
    try:
        key = object_type.strip().upper()
        research_results: dict = dict(tool_context.state.get("app:RESEARCH_RESULTS") or {})
        research_results[key] = results
        tool_context.state["app:RESEARCH_RESULTS"] = research_results
        logger.info("save_research_results: saved %d chars for object_type=%s", len(results), key)
        return {
            "success": True,
            "object_type": key,
            "message": f"Research results for '{key}' saved to session state.",
        }
    except Exception as e:
        logger.exception("save_research_results: failed to save results")
        return {
            "success": False,
            "object_type": object_type,
            "error": str(e),
            "message": f"Failed to save research results: {e}",
        }
