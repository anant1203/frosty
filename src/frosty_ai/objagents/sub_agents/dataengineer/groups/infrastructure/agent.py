from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.database.prompt import AGENT_NAME as _DB_NAME, DESCRIPTION as _DB_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.schema.prompt import AGENT_NAME as _SCH_NAME, DESCRIPTION as _SCH_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.externalvolume.prompt import AGENT_NAME as _EV_NAME, DESCRIPTION as _EV_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_infrastructure_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.database.agent", agent_attr="ag_sf_manage_database", name=_DB_NAME, description=_DB_DESC),
        LazyAgentTool(module_path=f"{_BASE}.schema.agent", agent_attr="ag_sf_manage_schema", name=_SCH_NAME, description=_SCH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.externalvolume.agent", agent_attr="ag_sf_manage_external_volume", name=_EV_NAME, description=_EV_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
