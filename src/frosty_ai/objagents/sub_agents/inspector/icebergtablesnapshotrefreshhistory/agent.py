from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_iceberg_table_snapshot_refresh_history,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_iceberg_table_snapshot_refresh_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_iceberg_table_snapshot_refresh_history,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
