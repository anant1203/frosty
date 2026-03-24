from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.administrator.user.prompt import AGENT_NAME as _USER_NAME, DESCRIPTION as _USER_DESC
from src.frosty_ai.objagents.sub_agents.administrator.role.prompt import AGENT_NAME as _ROLE_NAME, DESCRIPTION as _ROLE_DESC
from src.frosty_ai.objagents.sub_agents.administrator.databaserole.prompt import AGENT_NAME as _DR_NAME, DESCRIPTION as _DR_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.administrator"

ag_sf_identity_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.user.agent", agent_attr="ag_sf_manage_user", name=_USER_NAME, description=_USER_DESC),
        LazyAgentTool(module_path=f"{_BASE}.role.agent", agent_attr="ag_sf_manage_role", name=_ROLE_NAME, description=_ROLE_DESC),
        LazyAgentTool(module_path=f"{_BASE}.databaserole.agent", agent_attr="ag_sf_manage_database_role", name=_DR_NAME, description=_DR_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
