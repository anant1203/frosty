import logging
import pathlib
from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset

logger = logging.getLogger(__name__)
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from src.frosty_ai.objagents import config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .groups.infrastructure.prompt import AGENT_NAME as _INFRA_NAME, DESCRIPTION as _INFRA_DESC
from .groups.tables.prompt import AGENT_NAME as _TBL_GRP_NAME, DESCRIPTION as _TBL_GRP_DESC
from .groups.views.prompt import AGENT_NAME as _VW_GRP_NAME, DESCRIPTION as _VW_GRP_DESC
from .groups.ingestion.prompt import AGENT_NAME as _ING_NAME, DESCRIPTION as _ING_DESC
from .groups.automation.prompt import AGENT_NAME as _AUTO_NAME, DESCRIPTION as _AUTO_DESC
from .groups.analytics.prompt import AGENT_NAME as _ANALYTICS_NAME, DESCRIPTION as _ANALYTICS_DESC
from .groups.lifecycle.prompt import AGENT_NAME as _LC_NAME, DESCRIPTION as _LC_DESC

_GROUPS = "src.frosty_ai.objagents.sub_agents.dataengineer.groups"

_skills_dir = pathlib.Path(__file__).parents[5] / "skills"
logger.debug("[DATA_ENGINEER] Loading skill: snowflake-naming-conventions")
_naming_skill_toolset = SkillToolset(
    skills=[load_skill_from_dir(_skills_dir / "snowflake-naming-conventions")]
)
logger.debug("[DATA_ENGINEER] Skill loaded successfully")

ag_sf_data_engineer = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=([_naming_skill_toolset] if cfg.USE_SKILLS else []) + [
        LazyAgentTool(module_path=f"{_GROUPS}.infrastructure.agent", agent_attr="ag_sf_infrastructure_group", name=_INFRA_NAME, description=_INFRA_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.tables.agent", agent_attr="ag_sf_table_group", name=_TBL_GRP_NAME, description=_TBL_GRP_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.views.agent", agent_attr="ag_sf_view_group", name=_VW_GRP_NAME, description=_VW_GRP_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.ingestion.agent", agent_attr="ag_sf_ingestion_group", name=_ING_NAME, description=_ING_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.automation.agent", agent_attr="ag_sf_automation_group", name=_AUTO_NAME, description=_AUTO_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.analytics.agent", agent_attr="ag_sf_analytics_group", name=_ANALYTICS_NAME, description=_ANALYTICS_DESC),
        LazyAgentTool(module_path=f"{_GROUPS}.lifecycle.agent", agent_attr="ag_sf_lifecycle_group", name=_LC_NAME, description=_LC_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
