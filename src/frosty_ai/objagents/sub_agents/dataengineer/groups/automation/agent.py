from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.task.prompt import AGENT_NAME as _TASK_NAME, DESCRIPTION as _TASK_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.stream.prompt import AGENT_NAME as _STR_NAME, DESCRIPTION as _STR_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.storedprocedure.prompt import AGENT_NAME as _SP_NAME, DESCRIPTION as _SP_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_automation_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.task.agent", agent_attr="ag_sf_manage_task", name=_TASK_NAME, description=_TASK_DESC),
        LazyAgentTool(module_path=f"{_BASE}.stream.agent", agent_attr="ag_sf_manage_stream", name=_STR_NAME, description=_STR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.storedprocedure.agent", agent_attr="ag_sf_manage_stored_procedure", name=_SP_NAME, description=_SP_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
