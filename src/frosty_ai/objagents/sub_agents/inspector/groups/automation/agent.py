from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.tasks.prompt import AGENT_NAME as _TASK_NAME, DESCRIPTION as _TASK_DESC
from src.frosty_ai.objagents.sub_agents.inspector.streams.prompt import AGENT_NAME as _STR_NAME, DESCRIPTION as _STR_DESC
from src.frosty_ai.objagents.sub_agents.inspector.procedures.prompt import AGENT_NAME as _PROC_NAME, DESCRIPTION as _PROC_DESC
from src.frosty_ai.objagents.sub_agents.inspector.functions.prompt import AGENT_NAME as _FN_NAME, DESCRIPTION as _FN_DESC
from src.frosty_ai.objagents.sub_agents.inspector.cortexsearch.prompt import AGENT_NAME as _CS_NAME, DESCRIPTION as _CS_DESC
from src.frosty_ai.objagents.sub_agents.inspector.cortexsearchscoringprofiles.prompt import AGENT_NAME as _CSSP_NAME, DESCRIPTION as _CSSP_DESC
from src.frosty_ai.objagents.sub_agents.inspector.cortexsearchrefreshhistory.prompt import AGENT_NAME as _CSRH_NAME, DESCRIPTION as _CSRH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_inspector_automation_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.tasks.agent", agent_attr="ag_sf_inspect_task", name=_TASK_NAME, description=_TASK_DESC),
        LazyAgentTool(module_path=f"{_BASE}.streams.agent", agent_attr="ag_sf_inspect_stream", name=_STR_NAME, description=_STR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.procedures.agent", agent_attr="ag_sf_inspect_procedures", name=_PROC_NAME, description=_PROC_DESC),
        LazyAgentTool(module_path=f"{_BASE}.functions.agent", agent_attr="ag_sf_inspect_functions", name=_FN_NAME, description=_FN_DESC),
        LazyAgentTool(module_path=f"{_BASE}.cortexsearch.agent", agent_attr="ag_sf_inspect_cortex_search", name=_CS_NAME, description=_CS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.cortexsearchscoringprofiles.agent", agent_attr="ag_sf_inspect_cortex_search_scoring_profiles", name=_CSSP_NAME, description=_CSSP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.cortexsearchrefreshhistory.agent", agent_attr="ag_sf_inspect_cortex_search_refresh_history", name=_CSRH_NAME, description=_CSRH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
