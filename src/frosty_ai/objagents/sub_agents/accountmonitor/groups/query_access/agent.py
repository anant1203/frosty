from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .queryhistory.prompt import AGENT_NAME as _QH_NAME, DESCRIPTION as _QH_DESC
from .accesshistory.prompt import AGENT_NAME as _AH_NAME, DESCRIPTION as _AH_DESC
from .loginhistory.prompt import AGENT_NAME as _LH_NAME, DESCRIPTION as _LH_DESC
from .copyhistory.prompt import AGENT_NAME as _CH_NAME, DESCRIPTION as _CH_DESC
from .loadhistory.prompt import AGENT_NAME as _LOH_NAME, DESCRIPTION as _LOH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.query_access"

ag_sf_am_query_access_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.queryhistory.agent", agent_attr="ag_sf_am_query_history", name=_QH_NAME, description=_QH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.accesshistory.agent", agent_attr="ag_sf_am_access_history", name=_AH_NAME, description=_AH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.loginhistory.agent", agent_attr="ag_sf_am_login_history", name=_LH_NAME, description=_LH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.copyhistory.agent", agent_attr="ag_sf_am_copy_history", name=_CH_NAME, description=_CH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.loadhistory.agent", agent_attr="ag_sf_am_load_history", name=_LOH_NAME, description=_LOH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
