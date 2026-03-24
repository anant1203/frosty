from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.table.prompt import AGENT_NAME as _TBL_NAME, DESCRIPTION as _TBL_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.dynamictable.prompt import AGENT_NAME as _DT_NAME, DESCRIPTION as _DT_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.externaltable.prompt import AGENT_NAME as _EXTTBL_NAME, DESCRIPTION as _EXTTBL_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.hybridtable.prompt import AGENT_NAME as _HT_NAME, DESCRIPTION as _HT_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.icebergtable.prompt import AGENT_NAME as _IT_NAME, DESCRIPTION as _IT_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.eventtable.prompt import AGENT_NAME as _ET_NAME, DESCRIPTION as _ET_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_table_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.table.agent", agent_attr="ag_sf_manage_table", name=_TBL_NAME, description=_TBL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.dynamictable.agent", agent_attr="ag_sf_manage_dynamic_table", name=_DT_NAME, description=_DT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.externaltable.agent", agent_attr="ag_sf_manage_external_table", name=_EXTTBL_NAME, description=_EXTTBL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.hybridtable.agent", agent_attr="ag_sf_manage_hybrid_table", name=_HT_NAME, description=_HT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.icebergtable.agent", agent_attr="ag_sf_manage_iceberg_table", name=_IT_NAME, description=_IT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.eventtable.agent", agent_attr="ag_sf_manage_event_table", name=_ET_NAME, description=_ET_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
