from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_logins_by_user,
    get_failed_logins,
    get_failed_logins_by_user,
    get_logins_by_client_ip,
    get_logins_in_time_range,
    get_logins_by_client_type,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_login_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_logins_by_user,
        get_failed_logins,
        get_failed_logins_by_user,
        get_logins_by_client_ip,
        get_logins_in_time_range,
        get_logins_by_client_type,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
