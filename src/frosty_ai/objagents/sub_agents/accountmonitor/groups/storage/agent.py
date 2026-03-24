from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .storageusage.prompt import AGENT_NAME as _SU_NAME, DESCRIPTION as _SU_DESC
from .tablestoragemetrics.prompt import AGENT_NAME as _TSM_NAME, DESCRIPTION as _TSM_DESC
from .stages.prompt import AGENT_NAME as _ST_NAME, DESCRIPTION as _ST_DESC
from .pipes.prompt import AGENT_NAME as _PI_NAME, DESCRIPTION as _PI_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.storage"

ag_sf_am_storage_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.storageusage.agent", agent_attr="ag_sf_am_storage_usage", name=_SU_NAME, description=_SU_DESC),
        LazyAgentTool(module_path=f"{_BASE}.tablestoragemetrics.agent", agent_attr="ag_sf_am_table_storage_metrics", name=_TSM_NAME, description=_TSM_DESC),
        LazyAgentTool(module_path=f"{_BASE}.stages.agent", agent_attr="ag_sf_am_stages", name=_ST_NAME, description=_ST_DESC),
        LazyAgentTool(module_path=f"{_BASE}.pipes.agent", agent_attr="ag_sf_am_pipes", name=_PI_NAME, description=_PI_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
