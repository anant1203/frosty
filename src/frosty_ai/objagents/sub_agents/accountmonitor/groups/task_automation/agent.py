from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .taskhistory.prompt import AGENT_NAME as _TH_NAME, DESCRIPTION as _TH_DESC
from .serverlesstaskhistory.prompt import AGENT_NAME as _STH_NAME, DESCRIPTION as _STH_DESC
from .alerthistory.prompt import AGENT_NAME as _ALTH_NAME, DESCRIPTION as _ALTH_DESC
from .materializedviewrefresh.prompt import AGENT_NAME as _MVR_NAME, DESCRIPTION as _MVR_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.task_automation"

ag_sf_am_task_automation_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.taskhistory.agent", agent_attr="ag_sf_am_task_history", name=_TH_NAME, description=_TH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.serverlesstaskhistory.agent", agent_attr="ag_sf_am_serverless_task_history", name=_STH_NAME, description=_STH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.alerthistory.agent", agent_attr="ag_sf_am_alert_history", name=_ALTH_NAME, description=_ALTH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.materializedviewrefresh.agent", agent_attr="ag_sf_am_materialized_view_refresh", name=_MVR_NAME, description=_MVR_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
