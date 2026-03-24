from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS, SEARCH_INSTRUCTIONS
from .tools import save_research_results, web_search
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents._spinner import spinner

# google_search is a Gemini built-in tool and cannot be combined with function
# tools. For non-Gemini models we fall back to a plain function tool instead.
if cfg.IS_GOOGLE_MODEL:
    from google.adk.tools import google_search
    _search_tool = google_search
else:
    _search_tool = web_search


def _before_research_agent_callback(callback_context):
    """Inform the user which search backend will be used for this research run."""
    if cfg.IS_GOOGLE_MODEL:
        spinner.println("Search: using Google Search")
    else:
        spinner.println("Search: using DuckDuckGo (this may take longer than Google Search)")
        spinner.println("  You can plug in a custom web search tool by replacing the DuckDuckGo"
                        " implementation in src/frosty_ai/objagents/sub_agents/research/tools.py")
    return None


# Inner agent: only uses the search tool (no function tools alongside built-ins,
# which Gemini does not allow).
_ag_sf_research_search = LlmAgent(
    name="RESEARCH_SEARCH_AGENT",
    model=cfg.PRIMARY_MODEL,
    description="Performs web searches about Snowflake and returns the synthesised findings.",
    instruction=SEARCH_INSTRUCTIONS,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    tools=[_search_tool],
)

# Outer agent: orchestrates the search sub-agent and persists results to state.
# It has only function tools (no built-in tools), so the API constraint is respected.
ag_sf_research = LlmAgent(
    name=AGENT_NAME,
    model=cfg.PRIMARY_MODEL,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    before_agent_callback=_before_research_agent_callback,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    tools=[AgentTool(agent=_ag_sf_research_search), save_research_results],
)