from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool
from .tools import get_created_objects_from_memory, get_successful_operations

from .groups.schema_objects.prompt import AGENT_NAME as _SO_NAME, DESCRIPTION as _SO_DESC
from .groups.advanced_tables.prompt import AGENT_NAME as _AT_NAME, DESCRIPTION as _AT_DESC
from .groups.semantic.prompt import AGENT_NAME as _SEM_NAME, DESCRIPTION as _SEM_DESC
from .groups.automation.prompt import AGENT_NAME as _AUTO_NAME, DESCRIPTION as _AUTO_DESC
from .groups.access_control.prompt import AGENT_NAME as _AC_NAME, DESCRIPTION as _AC_DESC
from .groups.history.prompt import AGENT_NAME as _HIST_NAME, DESCRIPTION as _HIST_DESC
from .dataprofiler.prompt import AGENT_NAME as _DP_NAME, DESCRIPTION as _DP_DESC
from .nl2sql.prompt import AGENT_NAME as _DA_NAME, DESCRIPTION as _DA_DESC

_GROUPS = "src.frosty_ai.objagents.sub_agents.inspector.groups"
_INSPECTOR = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_inspector_pillar = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        get_created_objects_from_memory,
        get_successful_operations,
        LazyAgentTool(module_path=f"{_GROUPS}.schema_objects.agent", agent_attr="ag_sf_schema_objects_group", name=_SO_NAME, description=_SO_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.advanced_tables.agent", agent_attr="ag_sf_advanced_tables_group", name=_AT_NAME, description=_AT_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.semantic.agent", agent_attr="ag_sf_semantic_group", name=_SEM_NAME, description=_SEM_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.automation.agent", agent_attr="ag_sf_inspector_automation_group", name=_AUTO_NAME, description=_AUTO_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.access_control.agent", agent_attr="ag_sf_access_control_group", name=_AC_NAME, description=_AC_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.history.agent", agent_attr="ag_sf_history_group", name=_HIST_NAME, description=_HIST_DESC),
        LazyAgentTool(module_path=f"{_INSPECTOR}.dataprofiler.agent", agent_attr="ag_sf_data_profiler", name=_DP_NAME, description=_DP_DESC),
        LazyAgentTool(module_path=f"{_INSPECTOR}.nl2sql.agent", agent_attr="ag_sf_data_analyst", name=_DA_NAME, description=_DA_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
