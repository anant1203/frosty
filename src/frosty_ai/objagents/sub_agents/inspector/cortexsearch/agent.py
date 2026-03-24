from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_cortex_search_exists,
    list_cortex_search_in_schema,
    get_cortex_search_properties,
    filter_cortex_search_by_indexing_state
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_cortex_search = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_cortex_search_exists,
        list_cortex_search_in_schema,
        get_cortex_search_properties,
        filter_cortex_search_by_indexing_state
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
