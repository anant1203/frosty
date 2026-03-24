from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.administrator.failovergroup.prompt import AGENT_NAME as _FG_NAME, DESCRIPTION as _FG_DESC
from src.frosty_ai.objagents.sub_agents.administrator.replicationgroup.prompt import AGENT_NAME as _RG_NAME, DESCRIPTION as _RG_DESC
from src.frosty_ai.objagents.sub_agents.administrator.connection.prompt import AGENT_NAME as _CONN_NAME, DESCRIPTION as _CONN_DESC
from src.frosty_ai.objagents.sub_agents.administrator.organizationprofile.prompt import AGENT_NAME as _OP_NAME, DESCRIPTION as _OP_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.administrator"

ag_sf_replication_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.failovergroup.agent", agent_attr="ag_sf_manage_failover_group", name=_FG_NAME, description=_FG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.replicationgroup.agent", agent_attr="ag_sf_manage_replication_group", name=_RG_NAME, description=_RG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.connection.agent", agent_attr="ag_sf_manage_connection", name=_CONN_NAME, description=_CONN_DESC),
        LazyAgentTool(module_path=f"{_BASE}.organizationprofile.agent", agent_attr="ag_sf_manage_organization_profile", name=_OP_NAME, description=_OP_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
