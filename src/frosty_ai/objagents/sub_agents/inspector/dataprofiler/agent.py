from google.adk.agents import LlmAgent

import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from .tools import profile_table, get_top_values

ag_sf_data_profiler = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    tools=[profile_table, get_top_values],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
