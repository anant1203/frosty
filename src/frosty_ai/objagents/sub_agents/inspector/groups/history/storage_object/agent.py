from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.stagestorageusagehistory.prompt import AGENT_NAME as _SSUH_NAME, DESCRIPTION as _SSUH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.tablestoragemetrics.prompt import AGENT_NAME as _TSM_NAME, DESCRIPTION as _TSM_DESC
from src.frosty_ai.objagents.sub_agents.inspector.pipeusagehistory.prompt import AGENT_NAME as _PUH_NAME, DESCRIPTION as _PUH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.materializedviewrefreshhistory.prompt import AGENT_NAME as _MVRH_NAME, DESCRIPTION as _MVRH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.dynamictablerefreshhistory.prompt import AGENT_NAME as _DTRH_NAME, DESCRIPTION as _DTRH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.applicationconfigurationvaluehistory.prompt import AGENT_NAME as _ACVH_NAME, DESCRIPTION as _ACVH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_storage_object_history_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.stagestorageusagehistory.agent", agent_attr="ag_sf_inspect_stage_storage_usage_history", name=_SSUH_NAME, description=_SSUH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.tablestoragemetrics.agent", agent_attr="ag_sf_inspect_table_storage_metrics", name=_TSM_NAME, description=_TSM_DESC),
        LazyAgentTool(module_path=f"{_BASE}.pipeusagehistory.agent", agent_attr="ag_sf_inspect_pipe_usage_history", name=_PUH_NAME, description=_PUH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.materializedviewrefreshhistory.agent", agent_attr="ag_sf_inspect_materialized_view_refresh_history", name=_MVRH_NAME, description=_MVRH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.dynamictablerefreshhistory.agent", agent_attr="ag_sf_inspect_dynamic_table_refresh_history", name=_DTRH_NAME, description=_DTRH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.applicationconfigurationvaluehistory.agent", agent_attr="ag_sf_inspect_application_configuration_value_history", name=_ACVH_NAME, description=_ACVH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
