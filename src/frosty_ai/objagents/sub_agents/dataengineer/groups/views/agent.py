from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.view.prompt import AGENT_NAME as _VW_NAME, DESCRIPTION as _VW_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.materializedview.prompt import AGENT_NAME as _MV_NAME, DESCRIPTION as _MV_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.semanticview.prompt import AGENT_NAME as _SV_NAME, DESCRIPTION as _SV_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_view_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.view.agent", agent_attr="ag_sf_manage_view", name=_VW_NAME, description=_VW_DESC),
        LazyAgentTool(module_path=f"{_BASE}.materializedview.agent", agent_attr="ag_sf_manage_materialized_view", name=_MV_NAME, description=_MV_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semanticview.agent", agent_attr="ag_sf_manage_semantic_view", name=_SV_NAME, description=_SV_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
