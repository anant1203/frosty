from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.fileformat.prompt import AGENT_NAME as _FF_NAME, DESCRIPTION as _FF_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.externalstage.prompt import AGENT_NAME as _EXTSTG_NAME, DESCRIPTION as _EXTSTG_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.internalstage.prompt import AGENT_NAME as _INTSTG_NAME, DESCRIPTION as _INTSTG_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.copyinto.prompt import AGENT_NAME as _CI_NAME, DESCRIPTION as _CI_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.snowpipe.prompt import AGENT_NAME as _SNWP_NAME, DESCRIPTION as _SNWP_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_ingestion_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.fileformat.agent", agent_attr="ag_sf_manage_file_format", name=_FF_NAME, description=_FF_DESC),
        LazyAgentTool(module_path=f"{_BASE}.externalstage.agent", agent_attr="ag_sf_manage_external_stage", name=_EXTSTG_NAME, description=_EXTSTG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.internalstage.agent", agent_attr="ag_sf_manage_internal_stage", name=_INTSTG_NAME, description=_INTSTG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.copyinto.agent", agent_attr="ag_sf_manage_copy_into", name=_CI_NAME, description=_CI_DESC),
        LazyAgentTool(module_path=f"{_BASE}.snowpipe.agent", agent_attr="ag_sf_manage_snowpipe", name=_SNWP_NAME, description=_SNWP_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
