from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .databases.prompt import AGENT_NAME as _DB_NAME, DESCRIPTION as _DB_DESC
from .schemata.prompt import AGENT_NAME as _SC_NAME, DESCRIPTION as _SC_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.infrastructure"

ag_sf_am_infrastructure_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.databases.agent", agent_attr="ag_sf_am_databases", name=_DB_NAME, description=_DB_DESC),
        LazyAgentTool(module_path=f"{_BASE}.schemata.agent", agent_attr="ag_sf_am_schemata", name=_SC_NAME, description=_SC_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
