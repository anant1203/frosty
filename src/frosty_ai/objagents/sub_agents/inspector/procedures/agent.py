from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_procedure_exists,
    list_all_procedures,
    get_procedure_properties,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_procedures = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_procedure_exists,
        list_all_procedures,
        get_procedure_properties,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
