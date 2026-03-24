from google.adk.agents import LlmAgent
from src.frosty_ai.objagents import config as cfg
from .tools import get_session_state, execute_query
from .moltbook_tools import moltbook_post, moltbook_get_feed, moltbook_get_home, moltbook_get_comments, moltbook_comment
from .lazy_agent_tool import LazyAgentTool
from .prompt import MANAGER_NAME, MANAGER_DESCRIPTION, MANAGER_INSTRUCTIONS

# Import only the lightweight prompt constants from each pillar —
# none of these trigger sub-agent loading.
from .sub_agents.dataengineer.prompt import AGENT_NAME as _DE_NAME, DESCRIPTION as _DE_DESC
from .sub_agents.securityengineer.prompt import AGENT_NAME as _SE_NAME, DESCRIPTION as _SE_DESC
from .sub_agents.administrator.prompt import AGENT_NAME as _ADM_NAME, DESCRIPTION as _ADM_DESC
from .sub_agents.governance.prompt import AGENT_NAME as _GOV_NAME, DESCRIPTION as _GOV_DESC
from .sub_agents.inspector.prompt import AGENT_NAME as _INS_NAME, DESCRIPTION as _INS_DESC
from .sub_agents.research.prompt import AGENT_NAME as _RES_NAME, DESCRIPTION as _RES_DESC
from .sub_agents.accountmonitor.prompt import AGENT_NAME as _MON_NAME, DESCRIPTION as _MON_DESC

ag_sf_manager = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=MANAGER_NAME,
    description=MANAGER_DESCRIPTION,
    instruction=MANAGER_INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        get_session_state,
        execute_query,
        moltbook_post,
        moltbook_comment,
        moltbook_get_comments,
        moltbook_get_feed,
        moltbook_get_home,
        # Monitoring and inspection first — most likely to be hit early
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.accountmonitor.agent",
            agent_attr="ag_sf_account_monitor",
            name=_MON_NAME,
            description=_MON_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.inspector.agent",
            agent_attr="ag_sf_inspector_pillar",
            name=_INS_NAME,
            description=_INS_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.research.agent",
            agent_attr="ag_sf_research",
            name=_RES_NAME,
            description=_RES_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.dataengineer.agent",
            agent_attr="ag_sf_data_engineer",
            name=_DE_NAME,
            description=_DE_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.securityengineer.agent",
            agent_attr="ag_sf_security_engineer",
            name=_SE_NAME,
            description=_SE_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.administrator.agent",
            agent_attr="ag_sf_administrator",
            name=_ADM_NAME,
            description=_ADM_DESC,
        ),
        LazyAgentTool(
            module_path="src.frosty_ai.objagents.sub_agents.governance.agent",
            agent_attr="ag_sf_data_governance",
            name=_GOV_NAME,
            description=_GOV_DESC,
        ),
    ],
)

# This is the root agent exposed to the ADK runtime.
root_agent = ag_sf_manager
