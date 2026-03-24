from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.cortexsearch.prompt import AGENT_NAME as _CS_NAME, DESCRIPTION as _CS_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.notebook.prompt import AGENT_NAME as _NB_NAME, DESCRIPTION as _NB_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.model.prompt import AGENT_NAME as _MDL_NAME, DESCRIPTION as _MDL_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.dataset.prompt import AGENT_NAME as _DS_NAME, DESCRIPTION as _DS_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.prompt import AGENT_NAME as _SL_NAME, DESCRIPTION as _SL_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.userdefinedfunction.prompt import AGENT_NAME as _UDF_NAME, DESCRIPTION as _UDF_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.externalfunction.prompt import AGENT_NAME as _EF_NAME, DESCRIPTION as _EF_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.datametricfunction.prompt import AGENT_NAME as _DMF_NAME, DESCRIPTION as _DMF_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.sequence.prompt import AGENT_NAME as _SEQ_NAME, DESCRIPTION as _SEQ_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_analytics_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.cortexsearch.agent", agent_attr="ag_sf_manage_cortex_search", name=_CS_NAME, description=_CS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.notebook.agent", agent_attr="ag_sf_manage_notebook", name=_NB_NAME, description=_NB_DESC),
        LazyAgentTool(module_path=f"{_BASE}.model.agent", agent_attr="ag_sf_manage_model", name=_MDL_NAME, description=_MDL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.dataset.agent", agent_attr="ag_sf_manage_dataset", name=_DS_NAME, description=_DS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.streamlit.agent", agent_attr="ag_sf_manage_streamlit", name=_SL_NAME, description=_SL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.userdefinedfunction.agent", agent_attr="ag_sf_manage_user_defined_function", name=_UDF_NAME, description=_UDF_DESC),
        LazyAgentTool(module_path=f"{_BASE}.externalfunction.agent", agent_attr="ag_sf_manage_external_function", name=_EF_NAME, description=_EF_DESC),
        LazyAgentTool(module_path=f"{_BASE}.datametricfunction.agent", agent_attr="ag_sf_manage_data_metric_function", name=_DMF_NAME, description=_DMF_DESC),
        LazyAgentTool(module_path=f"{_BASE}.sequence.agent", agent_attr="ag_sf_manage_sequence", name=_SEQ_NAME, description=_SEQ_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
