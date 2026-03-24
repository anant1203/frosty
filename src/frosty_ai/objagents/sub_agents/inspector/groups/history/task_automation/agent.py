from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.taskhistory.prompt import AGENT_NAME as _TASKH_NAME, DESCRIPTION as _TASKH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.alerthistory.prompt import AGENT_NAME as _ALERTH_NAME, DESCRIPTION as _ALERTH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.serverlesstaskhistory.prompt import AGENT_NAME as _SLTH_NAME, DESCRIPTION as _SLTH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.completetaskgraphs.prompt import AGENT_NAME as _CTG_NAME, DESCRIPTION as _CTG_DESC
from src.frosty_ai.objagents.sub_agents.inspector.taskdependents.prompt import AGENT_NAME as _TASKD_NAME, DESCRIPTION as _TASKD_DESC
from src.frosty_ai.objagents.sub_agents.inspector.notificationhistory.prompt import AGENT_NAME as _NH_NAME, DESCRIPTION as _NH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_task_automation_history_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.taskhistory.agent", agent_attr="ag_sf_inspect_task_history", name=_TASKH_NAME, description=_TASKH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.alerthistory.agent", agent_attr="ag_sf_inspect_alert_history", name=_ALERTH_NAME, description=_ALERTH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.serverlesstaskhistory.agent", agent_attr="ag_sf_inspect_serverless_task_history", name=_SLTH_NAME, description=_SLTH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.completetaskgraphs.agent", agent_attr="ag_sf_inspect_complete_task_graphs", name=_CTG_NAME, description=_CTG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.taskdependents.agent", agent_attr="ag_sf_inspect_task_dependents", name=_TASKD_NAME, description=_TASKD_DESC),
        LazyAgentTool(module_path=f"{_BASE}.notificationhistory.agent", agent_attr="ag_sf_inspect_notification_history", name=_NH_NAME, description=_NH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
