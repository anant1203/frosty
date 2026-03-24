import logging
import pathlib

from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset

import src.frosty_ai.objagents.config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from .tools import discover_schema, run_data_query, generate_business_rules_draft

logger = logging.getLogger(__name__)

_skills_dir = pathlib.Path(__file__).parents[6] / "skills"
logger.debug("[DATA_ANALYST] Loading skill: snowflake-data-analyst")
_analyst_skill_toolset = SkillToolset(
    skills=[load_skill_from_dir(_skills_dir / "snowflake-data-analyst")]
)
logger.debug("[DATA_ANALYST] Skill loaded successfully")

ag_sf_data_analyst = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    tools=([_analyst_skill_toolset] if cfg.USE_SKILLS else []) + [
        discover_schema,
        run_data_query,
        generate_business_rules_draft,
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
