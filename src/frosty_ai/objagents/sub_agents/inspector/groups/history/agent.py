from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.groups.history.query_access.prompt import AGENT_NAME as _QA_NAME, DESCRIPTION as _QA_DESC
from src.frosty_ai.objagents.sub_agents.inspector.groups.history.warehouse_compute.prompt import AGENT_NAME as _WC_NAME, DESCRIPTION as _WC_DESC
from src.frosty_ai.objagents.sub_agents.inspector.groups.history.task_automation.prompt import AGENT_NAME as _TA_NAME, DESCRIPTION as _TA_DESC
from src.frosty_ai.objagents.sub_agents.inspector.groups.history.storage_object.prompt import AGENT_NAME as _SO_NAME, DESCRIPTION as _SO_DESC

_GROUPS = "src.frosty_ai.objagents.sub_agents.inspector.groups.history"

ag_sf_history_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_GROUPS}.query_access.agent", agent_attr="ag_sf_query_access_history_group", name=_QA_NAME, description=_QA_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.warehouse_compute.agent", agent_attr="ag_sf_warehouse_compute_history_group", name=_WC_NAME, description=_WC_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.task_automation.agent", agent_attr="ag_sf_task_automation_history_group", name=_TA_NAME, description=_TA_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.storage_object.agent", agent_attr="ag_sf_storage_object_history_group", name=_SO_NAME, description=_SO_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
