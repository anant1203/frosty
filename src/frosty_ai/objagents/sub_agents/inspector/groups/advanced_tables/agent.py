from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTION
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from src.frosty_ai.objagents.sub_agents.inspector.externaltables.prompt import AGENT_NAME as _EXTTBL_NAME, DESCRIPTION as _EXTTBL_DESC
from src.frosty_ai.objagents.sub_agents.inspector.eventtables.prompt import AGENT_NAME as _EVT_NAME, DESCRIPTION as _EVT_DESC
from src.frosty_ai.objagents.sub_agents.inspector.hybridtables.prompt import AGENT_NAME as _HT_NAME, DESCRIPTION as _HT_DESC
from src.frosty_ai.objagents.sub_agents.inspector.dynamictables.prompt import AGENT_NAME as _DT_NAME, DESCRIPTION as _DT_DESC
from src.frosty_ai.objagents.sub_agents.inspector.icebergtablefiles.prompt import AGENT_NAME as _ITF_NAME, DESCRIPTION as _ITF_DESC
from src.frosty_ai.objagents.sub_agents.inspector.icebergtablesnapshotrefreshhistory.prompt import AGENT_NAME as _ITSRH_NAME, DESCRIPTION as _ITSRH_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.inspector"

ag_sf_advanced_tables_group = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.externaltables.agent", agent_attr="ag_sf_inspect_external_tables", name=_EXTTBL_NAME, description=_EXTTBL_DESC),
        LazyAgentTool(module_path=f"{_BASE}.eventtables.agent", agent_attr="ag_sf_inspect_event_tables", name=_EVT_NAME, description=_EVT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.hybridtables.agent", agent_attr="ag_sf_inspect_hybrid_tables", name=_HT_NAME, description=_HT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.dynamictables.agent", agent_attr="ag_sf_inspect_dynamic_tables", name=_DT_NAME, description=_DT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.icebergtablefiles.agent", agent_attr="ag_sf_inspect_iceberg_table_files", name=_ITF_NAME, description=_ITF_DESC),
        LazyAgentTool(module_path=f"{_BASE}.icebergtablesnapshotrefreshhistory.agent", agent_attr="ag_sf_inspect_iceberg_table_snapshot_refresh_history", name=_ITSRH_NAME, description=_ITSRH_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
