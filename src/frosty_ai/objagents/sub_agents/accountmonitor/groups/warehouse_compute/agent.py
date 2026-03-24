from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .warehousemeteringhistory.prompt import AGENT_NAME as _WMH_NAME, DESCRIPTION as _WMH_DESC
from .meteringdailyhistory.prompt import AGENT_NAME as _MDH_NAME, DESCRIPTION as _MDH_DESC
from .automaticclustering.prompt import AGENT_NAME as _AC_NAME, DESCRIPTION as _AC_DESC
from .warehouseeventshistory.prompt import AGENT_NAME as _WEH_NAME, DESCRIPTION as _WEH_DESC
from .datatransferhistory.prompt import AGENT_NAME as _DTH_NAME, DESCRIPTION as _DTH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.accountmonitor.groups.warehouse_compute"

ag_sf_am_warehouse_compute_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.warehousemeteringhistory.agent", agent_attr="ag_sf_am_warehouse_metering_history", name=_WMH_NAME, description=_WMH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.meteringdailyhistory.agent", agent_attr="ag_sf_am_metering_daily_history", name=_MDH_NAME, description=_MDH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.automaticclustering.agent", agent_attr="ag_sf_am_automatic_clustering", name=_AC_NAME, description=_AC_DESC),
        LazyAgentTool(module_path=f"{_BASE}.warehouseeventshistory.agent", agent_attr="ag_sf_am_warehouse_events_history", name=_WEH_NAME, description=_WEH_DESC),
        LazyAgentTool(module_path=f"{_BASE}.datatransferhistory.agent", agent_attr="ag_sf_am_data_transfer_history", name=_DTH_NAME, description=_DTH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
