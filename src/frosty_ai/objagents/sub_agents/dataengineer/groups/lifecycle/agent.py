from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.dataengineer.storagelifecyclepolicy.prompt import AGENT_NAME as _SLP_NAME, DESCRIPTION as _SLP_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.snapshot.prompt import AGENT_NAME as _SNAP_NAME, DESCRIPTION as _SNAP_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.snapshotpolicy.prompt import AGENT_NAME as _SNAPP_NAME, DESCRIPTION as _SNAPP_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.snapshotset.prompt import AGENT_NAME as _SNAPS_NAME, DESCRIPTION as _SNAPS_DESC
from src.frosty_ai.objagents.sub_agents.dataengineer.sampledata.prompt import AGENT_NAME as _SD_NAME, DESCRIPTION as _SD_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.dataengineer"

ag_sf_lifecycle_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.storagelifecyclepolicy.agent", agent_attr="ag_sf_manage_storage_lifecycle_policy", name=_SLP_NAME, description=_SLP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.snapshot.agent", agent_attr="ag_sf_manage_snapshot", name=_SNAP_NAME, description=_SNAP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.snapshotpolicy.agent", agent_attr="ag_sf_manage_snapshot_policy", name=_SNAPP_NAME, description=_SNAPP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.snapshotset.agent", agent_attr="ag_sf_manage_snapshot_set", name=_SNAPS_NAME, description=_SNAPS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.sampledata.agent", agent_attr="ag_sf_generate_sample_data", name=_SD_NAME, description=_SD_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
