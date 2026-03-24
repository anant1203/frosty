from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .groups.query_access.prompt import AGENT_NAME as _QA_NAME, DESCRIPTION as _QA_DESC
from .groups.warehouse_compute.prompt import AGENT_NAME as _WC_NAME, DESCRIPTION as _WC_DESC
from .groups.task_automation.prompt import AGENT_NAME as _TA_NAME, DESCRIPTION as _TA_DESC
from .groups.storage.prompt import AGENT_NAME as _ST_NAME, DESCRIPTION as _ST_DESC
from .groups.security_identity.prompt import AGENT_NAME as _SI_NAME, DESCRIPTION as _SI_DESC
from .groups.infrastructure.prompt import AGENT_NAME as _INF_NAME, DESCRIPTION as _INF_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups"

ag_sf_account_monitor = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.query_access.agent", agent_attr="ag_sf_am_query_access_group", name=_QA_NAME, description=_QA_DESC),
        LazyAgentTool(module_path=f"{_BASE}.warehouse_compute.agent", agent_attr="ag_sf_am_warehouse_compute_group", name=_WC_NAME, description=_WC_DESC),
        LazyAgentTool(module_path=f"{_BASE}.task_automation.agent", agent_attr="ag_sf_am_task_automation_group", name=_TA_NAME, description=_TA_DESC),
        LazyAgentTool(module_path=f"{_BASE}.storage.agent", agent_attr="ag_sf_am_storage_group", name=_ST_NAME, description=_ST_DESC),
        LazyAgentTool(module_path=f"{_BASE}.security_identity.agent", agent_attr="ag_sf_am_security_identity_group", name=_SI_NAME, description=_SI_DESC),
        LazyAgentTool(module_path=f"{_BASE}.infrastructure.agent", agent_attr="ag_sf_am_infrastructure_group", name=_INF_NAME, description=_INF_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
