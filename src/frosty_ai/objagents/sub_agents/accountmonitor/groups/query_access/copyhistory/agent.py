from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_copy_history_for_table,
    get_failed_copies,
    get_copy_history_in_time_range,
    get_copy_history_by_pipe,
    get_copy_errors_for_table,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_copy_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_copy_history_for_table,
        get_failed_copies,
        get_copy_history_in_time_range,
        get_copy_history_by_pipe,
        get_copy_errors_for_table,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
