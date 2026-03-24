from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_sessions_by_user,
    get_sessions_by_client_application,
    get_sessions_in_time_range,
    get_sessions_by_authentication_method,
    get_session_by_id,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_sessions = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_sessions_by_user,
        get_sessions_by_client_application,
        get_sessions_in_time_range,
        get_sessions_by_authentication_method,
        get_session_by_id,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
