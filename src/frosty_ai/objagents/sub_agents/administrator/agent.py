from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from src.frosty_ai.objagents import config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .groups.identity.prompt import AGENT_NAME as _ID_NAME, DESCRIPTION as _ID_DESC
from .groups.compute.prompt import AGENT_NAME as _COMP_NAME, DESCRIPTION as _COMP_DESC
from .groups.replication.prompt import AGENT_NAME as _REPL_NAME, DESCRIPTION as _REPL_DESC
from .groups.integration.prompt import AGENT_NAME as _INTG_NAME, DESCRIPTION as _INTG_DESC

_GROUPS = "src.frosty_ai.objagents.sub_agents.administrator.groups"

ag_sf_administrator = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        LazyAgentTool(module_path=f"{_GROUPS}.identity.agent", agent_attr="ag_sf_identity_group", name=_ID_NAME, description=_ID_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.compute.agent", agent_attr="ag_sf_compute_group", name=_COMP_NAME, description=_COMP_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.replication.agent", agent_attr="ag_sf_replication_group", name=_REPL_NAME, description=_REPL_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.integration.agent", agent_attr="ag_sf_integration_group", name=_INTG_NAME, description=_INTG_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
