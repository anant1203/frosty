from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_load_status_of_table,
    get_load_history_of_table,
    get_load_errors_of_table,
    get_most_recent_load_of_table,
    get_row_counts_of_table,
    get_failed_loads_of_table,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_load_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_load_status_of_table,
        get_load_history_of_table,
        get_load_errors_of_table,
        get_most_recent_load_of_table,
        get_row_counts_of_table,
        get_failed_loads_of_table,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
