from google.adk.agents import LlmAgent
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
from src.frosty_ai.objagents import config as cfg
from src.frosty_ai.objagents.sub_agents.pillar_callbacks import before_model_callback, after_model_callback
from src.frosty_ai.objagents.lazy_agent_tool import LazyAgentTool

from .authenticationpolicy.prompt import AGENT_NAME as _AUTHP_NAME, DESCRIPTION as _AUTHP_DESC
from .networkpolicy.prompt import AGENT_NAME as _NP_NAME, DESCRIPTION as _NP_DESC
from .networkrule.prompt import AGENT_NAME as _NR_NAME, DESCRIPTION as _NR_DESC
from .passwordpolicy.prompt import AGENT_NAME as _PASSP_NAME, DESCRIPTION as _PASSP_DESC
from .securityintegrationexternalapiauthentication.prompt import AGENT_NAME as _SIEAA_NAME, DESCRIPTION as _SIEAA_DESC
from .securityintegrationaws.prompt import AGENT_NAME as _SIAWS_NAME, DESCRIPTION as _SIAWS_DESC
from .externalaccessintegration.prompt import AGENT_NAME as _EAI_NAME, DESCRIPTION as _EAI_DESC
from .securityintegrationexternaloauth.prompt import AGENT_NAME as _SIEO_NAME, DESCRIPTION as _SIEO_DESC
from .apiintegrationamazonapigateway.prompt import AGENT_NAME as _AIAG_NAME, DESCRIPTION as _AIAG_DESC
from .sessionpolicy.prompt import AGENT_NAME as _SESSP_NAME, DESCRIPTION as _SESSP_DESC
from .packagespolicy.prompt import AGENT_NAME as _PKGP_NAME, DESCRIPTION as _PKGP_DESC
from .secret.prompt import AGENT_NAME as _SEC_NAME, DESCRIPTION as _SEC_DESC
from .aggregationpolicy.prompt import AGENT_NAME as _AGGP_NAME, DESCRIPTION as _AGGP_DESC
from .joinpolicy.prompt import AGENT_NAME as _JP_NAME, DESCRIPTION as _JP_DESC

_BASE = "src.frosty_ai.objagents.sub_agents.securityengineer"

ag_sf_security_engineer = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    planner=cfg.get_planner(1024),
    tools=[
        LazyAgentTool(module_path=f"{_BASE}.authenticationpolicy.agent", agent_attr="ag_sf_manage_authentication_policy", name=_AUTHP_NAME, description=_AUTHP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.networkpolicy.agent", agent_attr="ag_sf_manage_network_policy", name=_NP_NAME, description=_NP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.networkrule.agent", agent_attr="ag_sf_manage_network_rule", name=_NR_NAME, description=_NR_DESC),
        LazyAgentTool(module_path=f"{_BASE}.passwordpolicy.agent", agent_attr="ag_sf_manage_password_policy", name=_PASSP_NAME, description=_PASSP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.securityintegrationexternalapiauthentication.agent", agent_attr="ag_sf_manage_security_integration_external_api_authentication", name=_SIEAA_NAME, description=_SIEAA_DESC),
        LazyAgentTool(module_path=f"{_BASE}.securityintegrationaws.agent", agent_attr="ag_sf_manage_security_integration_aws", name=_SIAWS_NAME, description=_SIAWS_DESC),
        LazyAgentTool(module_path=f"{_BASE}.externalaccessintegration.agent", agent_attr="ag_sf_manage_external_access_integration", name=_EAI_NAME, description=_EAI_DESC),
        LazyAgentTool(module_path=f"{_BASE}.securityintegrationexternaloauth.agent", agent_attr="ag_sf_manage_security_integration_external_oauth", name=_SIEO_NAME, description=_SIEO_DESC),
        LazyAgentTool(module_path=f"{_BASE}.apiintegrationamazonapigateway.agent", agent_attr="ag_sf_manage_api_integration_amazon_api_gateway", name=_AIAG_NAME, description=_AIAG_DESC),
        LazyAgentTool(module_path=f"{_BASE}.sessionpolicy.agent", agent_attr="ag_sf_manage_session_policy", name=_SESSP_NAME, description=_SESSP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.packagespolicy.agent", agent_attr="ag_sf_manage_packages_policy", name=_PKGP_NAME, description=_PKGP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.secret.agent", agent_attr="ag_sf_manage_secret", name=_SEC_NAME, description=_SEC_DESC),
        LazyAgentTool(module_path=f"{_BASE}.aggregationpolicy.agent", agent_attr="ag_sf_manage_aggregation_policy", name=_AGGP_NAME, description=_AGGP_DESC),
        LazyAgentTool(module_path=f"{_BASE}.joinpolicy.agent", agent_attr="ag_sf_manage_join_policy", name=_JP_NAME, description=_JP_DESC),
    ],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
