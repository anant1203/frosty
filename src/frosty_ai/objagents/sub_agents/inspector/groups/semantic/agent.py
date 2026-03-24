from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.semanticviews.prompt import AGENT_NAME as _SEMVW_NAME, DESCRIPTION as _SEMVW_DESC
from src.frosty_ai.objagents.sub_agents.inspector.semantictables.prompt import AGENT_NAME as _SEMTBL_NAME, DESCRIPTION as _SEMTBL_DESC
from src.frosty_ai.objagents.sub_agents.inspector.semanticdimensions.prompt import AGENT_NAME as _SEMDIM_NAME, DESCRIPTION as _SEMDIM_DESC
from src.frosty_ai.objagents.sub_agents.inspector.semanticfacts.prompt import AGENT_NAME as _SEMFACT_NAME, DESCRIPTION as _SEMFACT_DESC
from src.frosty_ai.objagents.sub_agents.inspector.semanticmetrics.prompt import AGENT_NAME as _SEMMET_NAME, DESCRIPTION as _SEMMET_DESC
from src.frosty_ai.objagents.sub_agents.inspector.semanticrelationships.prompt import AGENT_NAME as _SEMREL_NAME, DESCRIPTION as _SEMREL_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_semantic_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.semanticviews.agent", agent_attr="ag_sf_inspect_semantic_views", name=_SEMVW_NAME, description=_SEMVW_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semantictables.agent", agent_attr="ag_sf_inspect_semantic_tables", name=_SEMTBL_NAME, description=_SEMTBL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semanticdimensions.agent", agent_attr="ag_sf_inspect_semantic_dimensions", name=_SEMDIM_NAME, description=_SEMDIM_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semanticfacts.agent", agent_attr="ag_sf_inspect_semantic_facts", name=_SEMFACT_NAME, description=_SEMFACT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semanticmetrics.agent", agent_attr="ag_sf_inspect_semantic_metrics", name=_SEMMET_NAME, description=_SEMMET_DESC),
        LazyAgentTool(module_path=f"{_BASE}.semanticrelationships.agent", agent_attr="ag_sf_inspect_semantic_relationships", name=_SEMREL_NAME, description=_SEMREL_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
