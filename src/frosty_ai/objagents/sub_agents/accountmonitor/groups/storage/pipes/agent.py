from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_pipes_in_schema,
    is_existing_pipe,
    get_pipe,
    get_autoingest_pipes,
    get_pipes_by_owner,
    get_deleted_pipes,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_pipes = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_pipes_in_schema,
        is_existing_pipe,
        get_pipe,
        get_autoingest_pipes,
        get_pipes_by_owner,
        get_deleted_pipes,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
