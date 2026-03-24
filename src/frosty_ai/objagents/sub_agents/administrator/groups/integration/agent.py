from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.administrator.notificationintegration.prompt import AGENT_NAME as _NI_NAME, DESCRIPTION as _NI_DESC
from src.frosty_ai.objagents.sub_agents.administrator.imagerepository.prompt import AGENT_NAME as _IR_NAME, DESCRIPTION as _IR_DESC
from src.frosty_ai.objagents.sub_agents.administrator.service.prompt import AGENT_NAME as _SVC_NAME, DESCRIPTION as _SVC_DESC
from src.frosty_ai.objagents.sub_agents.administrator.applicationpackage.prompt import AGENT_NAME as _AP_NAME, DESCRIPTION as _AP_DESC
from src.frosty_ai.objagents.sub_agents.administrator.alerts.prompt import AGENT_NAME as _ALERTS_NAME, DESCRIPTION as _ALERTS_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.administrator"

ag_sf_integration_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.notificationintegration.agent", agent_attr="ag_sf_manage_notification_integration", name=_NI_NAME, description=_NI_DESC),
        LazyAgentTool(module_path=f"{_BASE}.imagerepository.agent", agent_attr="ag_sf_manage_image_repository", name=_IR_NAME, description=_IR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.service.agent", agent_attr="ag_sf_manage_service", name=_SVC_NAME, description=_SVC_DESC),
        LazyAgentTool(module_path=f"{_BASE}.applicationpackage.agent", agent_attr="ag_sf_manage_application_package", name=_AP_NAME, description=_AP_DESC),
        LazyAgentTool(module_path="src.frosty_ai.objagents.sub_agents.administrator.alerts.agent", agent_attr="ag_sf_manage_alerts", name=_ALERTS_NAME, description=_ALERTS_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
