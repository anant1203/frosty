from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .grantstousers.prompt import AGENT_NAME as _GTU_NAME, DESCRIPTION as _GTU_DESC
from .grantstoroles.prompt import AGENT_NAME as _GTR_NAME, DESCRIPTION as _GTR_DESC
from .roles.prompt import AGENT_NAME as _RO_NAME, DESCRIPTION as _RO_DESC
from .users.prompt import AGENT_NAME as _US_NAME, DESCRIPTION as _US_DESC
from .sessions.prompt import AGENT_NAME as _SE_NAME, DESCRIPTION as _SE_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.security_identity"

ag_sf_am_security_identity_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.grantstousers.agent", agent_attr="ag_sf_am_grants_to_users", name=_GTU_NAME, description=_GTU_DESC),
        LazyAgentTool(module_path=f"{_BASE}.grantstoroles.agent", agent_attr="ag_sf_am_grants_to_roles", name=_GTR_NAME, description=_GTR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.roles.agent", agent_attr="ag_sf_am_roles", name=_RO_NAME, description=_RO_DESC),
        LazyAgentTool(module_path=f"{_BASE}.users.agent", agent_attr="ag_sf_am_users", name=_US_NAME, description=_US_DESC),
        LazyAgentTool(module_path=f"{_BASE}.sessions.agent", agent_attr="ag_sf_am_sessions", name=_SE_NAME, description=_SE_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
