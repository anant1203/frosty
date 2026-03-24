from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_metering_by_warehouse,
    get_metering_in_time_range,
    get_total_credits_by_warehouse,
    get_all_warehouse_names,
    get_credits_by_warehouse_in_time_range,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_warehouse_metering_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_metering_by_warehouse,
        get_metering_in_time_range,
        get_total_credits_by_warehouse,
        get_all_warehouse_names,
        get_credits_by_warehouse_in_time_range,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
