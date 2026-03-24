from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME,DESCRIPTION,INSTRUCTIONS
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.tools import execute_query, get_research_results
from google.adk.tools import AgentTool
from src.frosty_ai.objagents.sub_agents.research import ag_sf_research


ag_sf_manage_snapshot = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(512),
    tools=[AgentTool(agent=ag_sf_research), execute_query, get_research_results],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
