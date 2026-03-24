from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_task_history_by_name,
    get_failed_tasks,
    get_task_history_in_time_range,
    get_task_history_by_state,
    get_task_history_by_schema,
    get_most_recent_run,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_task_history = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_task_history_by_name,
        get_failed_tasks,
        get_task_history_in_time_range,
        get_task_history_by_state,
        get_task_history_by_schema,
        get_most_recent_run,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
