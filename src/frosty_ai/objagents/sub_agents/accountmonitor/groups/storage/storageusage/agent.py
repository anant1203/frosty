from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_storage_usage_in_time_range,
    get_latest_storage_usage,
    get_average_database_bytes_in_range,
    get_all_storage_usage,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_storage_usage = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_storage_usage_in_time_range,
        get_latest_storage_usage,
        get_average_database_bytes_in_range,
        get_all_storage_usage,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
