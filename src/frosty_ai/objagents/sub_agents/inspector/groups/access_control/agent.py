from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.applicableroles.prompt import AGENT_NAME as _AR_NAME, DESCRIPTION as _AR_DESC
from src.frosty_ai.objagents.sub_agents.inspector.enabledroles.prompt import AGENT_NAME as _ER_NAME, DESCRIPTION as _ER_DESC
from src.frosty_ai.objagents.sub_agents.inspector.objectprivileges.prompt import AGENT_NAME as _OP_NAME, DESCRIPTION as _OP_DESC
from src.frosty_ai.objagents.sub_agents.inspector.tableprivileges.prompt import AGENT_NAME as _TP_NAME, DESCRIPTION as _TP_DESC
from src.frosty_ai.objagents.sub_agents.inspector.usageprivileges.prompt import AGENT_NAME as _UP_NAME, DESCRIPTION as _UP_DESC
from src.frosty_ai.objagents.sub_agents.inspector.shares.prompt import AGENT_NAME as _SHR_NAME, DESCRIPTION as _SHR_DESC
from src.frosty_ai.objagents.sub_agents.inspector.replicationgroups.prompt import AGENT_NAME as _RG_NAME, DESCRIPTION as _RG_DESC
from src.frosty_ai.objagents.sub_agents.inspector.replicationgrouprefreshhistory.prompt import AGENT_NAME as _RGRH_NAME, DESCRIPTION as _RGRH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_access_control_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.applicableroles.agent", agent_attr="ag_sf_inspect_applicable_roles", name=_AR_NAME, description=_AR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.enabledroles.agent", agent_attr="ag_sf_inspect_enabled_roles", name=_ER_NAME, description=_ER_DESC),
        LazyAgentTool(module_path=f"{_BASE}.objectprivileges.agent", agent_attr="ag_sf_inspect_object_privileges", name=_OP_NAME, description=_OP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.tableprivileges.agent", agent_attr="ag_sf_inspect_table_privileges", name=_TP_NAME, description=_TP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.usageprivileges.agent", agent_attr="ag_sf_inspect_usage_privileges", name=_UP_NAME, description=_UP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.shares.agent", agent_attr="ag_sf_inspect_shares", name=_SHR_NAME, description=_SHR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.replicationgroups.agent", agent_attr="ag_sf_inspect_replication_groups", name=_RG_NAME, description=_RG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.replicationgrouprefreshhistory.agent", agent_attr="ag_sf_inspect_replication_group_refresh_history", name=_RGRH_NAME, description=_RGRH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
