from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_hybrid_table_exists,
    list_all_hybrid_tables,
    get_hybrid_table_properties,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_hybrid_tables = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_hybrid_table_exists,
        list_all_hybrid_tables,
        get_hybrid_table_properties,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
