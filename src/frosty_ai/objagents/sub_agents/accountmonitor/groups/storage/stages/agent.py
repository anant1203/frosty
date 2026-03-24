from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_stages_in_schema,
    get_stages_in_database,
    is_existing_stage,
    get_stages_by_type,
    get_stage,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_stages = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_stages_in_schema,
        get_stages_in_database,
        is_existing_stage,
        get_stages_by_type,
        get_stage,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
