from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_access_history_by_user,
    get_access_history_by_query,
    get_access_history_in_time_range,
    get_access_history_by_query_type,
    get_access_history_by_user_in_time_range,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_access_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_access_history_by_user,
        get_access_history_by_query,
        get_access_history_in_time_range,
        get_access_history_by_query_type,
        get_access_history_by_user_in_time_range,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
