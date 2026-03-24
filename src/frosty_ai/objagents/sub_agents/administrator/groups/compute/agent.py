from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.administrator.warehouse.prompt import AGENT_NAME as _WH_NAME, DESCRIPTION as _WH_DESC
from src.frosty_ai.objagents.sub_agents.administrator.computepool.prompt import AGENT_NAME as _CP_NAME, DESCRIPTION as _CP_DESC
from src.frosty_ai.objagents.sub_agents.administrator.resourcemonitor.prompt import AGENT_NAME as _RM_NAME, DESCRIPTION as _RM_DESC
from src.frosty_ai.objagents.sub_agents.administrator.provisionedthroughput.prompt import AGENT_NAME as _PT_NAME, DESCRIPTION as _PT_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.administrator"

ag_sf_compute_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.warehouse.agent", agent_attr="ag_sf_manage_warehouse", name=_WH_NAME, description=_WH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.computepool.agent", agent_attr="ag_sf_manage_compute_pool", name=_CP_NAME, description=_CP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.resourcemonitor.agent", agent_attr="ag_sf_resource_monitor", name=_RM_NAME, description=_RM_DESC),
        LazyAgentTool(module_path=f"{_BASE}.provisionedthroughput.agent", agent_attr="ag_sf_manage_provisioned_throughput", name=_PT_NAME, description=_PT_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
