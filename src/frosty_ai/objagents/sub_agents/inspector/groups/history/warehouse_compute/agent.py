from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool
from src.frosty_ai.objagents.tools import execute_query

from src.frosty_ai.objagents.sub_agents.inspector.warehousemeteringhistory.prompt import AGENT_NAME as _WMH_NAME, DESCRIPTION as _WMH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.warehouseloadhistory.prompt import AGENT_NAME as _WLH_NAME, DESCRIPTION as _WLH_DESC
from src.frosty_ai.objagents.sub_agents.inspector.automaticclustering.prompt import AGENT_NAME as _AC_NAME, DESCRIPTION as _AC_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_warehouse_compute_history_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.warehousemeteringhistory.agent", agent_attr="ag_sf_inspect_warehouse_metering_history", name=_WMH_NAME, description=_WMH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.warehouseloadhistory.agent", agent_attr="ag_sf_inspect_warehouse_load_history", name=_WLH_NAME, description=_WLH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.automaticclustering.agent", agent_attr="ag_sf_inspect_automatic_clustering_history", name=_AC_NAME, description=_AC_DESC),
        execute_query,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
