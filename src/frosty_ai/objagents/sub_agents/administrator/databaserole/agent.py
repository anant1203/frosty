import logging
import pathlib
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.tools import execute_query, get_research_results
from google.adk.tools import AgentTool
from src.frosty_ai.objagents.sub_agents.research import ag_sf_research

logger = logging.getLogger(__name__)

_skills_dir = pathlib.Path(__file__).parents[6] / "skills"
logger.debug("[DATABASE_ROLE] Loading skill: snowflake-create-database-role")
_skill_toolset = SkillToolset(
    skills=[load_skill_from_dir(_skills_dir / "snowflake-create-database-role")]
)
logger.debug("[DATABASE_ROLE] Skill loaded successfully")

ag_sf_manage_database_role = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(512),
    tools=([_skill_toolset] if cfg.USE_SKILLS else []) + [AgentTool(agent=ag_sf_research), execute_query, get_research_results],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
