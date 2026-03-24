from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_alert_history_by_name,
    get_failed_alerts,
    get_alert_history_in_time_range,
    get_alert_history_by_state,
    get_alert_history_by_schema,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_alert_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_alert_history_by_name,
        get_failed_alerts,
        get_alert_history_in_time_range,
        get_alert_history_by_state,
        get_alert_history_by_schema,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
