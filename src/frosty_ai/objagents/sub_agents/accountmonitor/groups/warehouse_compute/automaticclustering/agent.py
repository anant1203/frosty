from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
from .tools import (
    get_clustering_history_for_table,
    get_clustering_history_in_time_range,
    get_total_credits_for_table,
    get_clustering_history_by_database,
)
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback

ag_sf_am_automatic_clustering = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        get_clustering_history_for_table,
        get_clustering_history_in_time_range,
        get_total_credits_for_table,
        get_clustering_history_by_database,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
