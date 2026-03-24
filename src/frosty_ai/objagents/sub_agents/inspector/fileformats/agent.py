from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    check_fileformat_exists,
    list_all_fileformats,
    get_fileformat_properties,
    filter_fileformats_by_type,
    list_fileformats_by_owner,
    get_fileformat_format_options,
    get_fileformat_timestamps
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_inspect_file_format = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        check_fileformat_exists,
        list_all_fileformats,
        get_fileformat_properties,
        filter_fileformats_by_type,
        list_fileformats_by_owner,
        get_fileformat_format_options,
        get_fileformat_timestamps
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
