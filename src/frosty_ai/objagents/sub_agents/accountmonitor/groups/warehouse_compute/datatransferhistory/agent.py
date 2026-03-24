from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_transfers_in_time_range,
    get_transfers_by_source_cloud,
    get_transfers_by_target_cloud,
    get_transfers_by_type,
    get_total_bytes_transferred_in_range,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_data_transfer_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_transfers_in_time_range,
        get_transfers_by_source_cloud,
        get_transfers_by_target_cloud,
        get_transfers_by_type,
        get_total_bytes_transferred_in_range,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
