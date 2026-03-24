from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_metering_in_date_range,
    get_metering_by_service_type,
    get_metering_by_name,
    get_total_credits_billed_in_date_range,
    get_all_metering_history,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_metering_daily_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_metering_in_date_range,
        get_metering_by_service_type,
        get_metering_by_name,
        get_total_credits_billed_in_date_range,
        get_all_metering_history,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
