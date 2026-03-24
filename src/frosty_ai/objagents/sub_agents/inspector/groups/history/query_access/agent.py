from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.queryhistory.prompt import AGENT_NAME as _QH_NAME, DESCRIPTION as _QH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.queryaccelerationhistory.prompt import AGENT_NAME as _QAH_NAME, DESCRIPTION as _QAH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.loginhistory.prompt import AGENT_NAME as _LOGH_NAME, DESCRIPTION as _LOGH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.loadhistory.prompt import AGENT_NAME as _LH_NAME, DESCRIPTION as _LH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.copyhistory.prompt import AGENT_NAME as _COPYH_NAME, DESCRIPTION as _COPYH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_query_access_history_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.queryhistory.agent", agent_attr="ag_sf_inspect_query_history", name=_QH_NAME, description=_QH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.queryaccelerationhistory.agent", agent_attr="ag_sf_inspect_query_acceleration_history", name=_QAH_NAME, description=_QAH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.loginhistory.agent", agent_attr="ag_sf_inspect_login_history", name=_LOGH_NAME, description=_LOGH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.loadhistory.agent", agent_attr="ag_sf_inspect_load_history", name=_LH_NAME, description=_LH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.copyhistory.agent", agent_attr="ag_sf_inspect_copy_history", name=_COPYH_NAME, description=_COPYH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
