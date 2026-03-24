from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_queries_by_user,
    get_queries_by_warehouse,
    get_failed_queries,
    get_queries_in_time_range,
    get_long_running_queries,
    get_queries_by_type,
    get_queries_by_database,
    get_credits_by_warehouse,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_query_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_queries_by_user,
        get_queries_by_warehouse,
        get_failed_queries,
        get_queries_in_time_range,
        get_long_running_queries,
        get_queries_by_type,
        get_queries_by_database,
        get_credits_by_warehouse,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
