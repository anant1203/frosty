from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from src.frosty_ai.objagents import config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .tags.prompt import AGENT_NAME as _TAGS_NAME, DESCRIPTION as _TAGS_DESC
from .contact.prompt import AGENT_NAME as _CONTACT_NAME, DESCRIPTION as _CONTACT_DESC
from .maskingpolicy.prompt import AGENT_NAME as _MP_NAME, DESCRIPTION as _MP_DESC
from .privacypolicy.prompt import AGENT_NAME as _PP_NAME, DESCRIPTION as _PP_DESC
from .projectionpolicy.prompt import AGENT_NAME as _PROJP_NAME, DESCRIPTION as _PROJP_DESC
from .rowaccesspolicy.prompt import AGENT_NAME as _RAP_NAME, DESCRIPTION as _RAP_DESC
from .dataexchange.prompt import AGENT_NAME as _DX_NAME, DESCRIPTION as _DX_DESC
from .listing.prompt import AGENT_NAME as _LIST_NAME, DESCRIPTION as _LIST_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.governance"

ag_sf_data_governance = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.tags.agent", agent_attr="ag_sf_manage_tags", name=_TAGS_NAME, description=_TAGS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.contact.agent", agent_attr="ag_sf_manage_contacts", name=_CONTACT_NAME, description=_CONTACT_DESC),
        LazyAgentTool(module_path=f"{_BASE}.maskingpolicy.agent", agent_attr="ag_sf_manage_masking_policy", name=_MP_NAME, description=_MP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.privacypolicy.agent", agent_attr="ag_sf_manage_privacy_policy", name=_PP_NAME, description=_PP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.projectionpolicy.agent", agent_attr="ag_sf_manage_projection_policy", name=_PROJP_NAME, description=_PROJP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.rowaccesspolicy.agent", agent_attr="ag_sf_manage_row_access_policy", name=_RAP_NAME, description=_RAP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.dataexchange.agent", agent_attr="ag_sf_manage_data_exchange", name=_DX_NAME, description=_DX_DESC),
        LazyAgentTool(module_path=f"{_BASE}.listing.agent", agent_attr="ag_sf_manage_listing", name=_LIST_NAME, description=_LIST_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
