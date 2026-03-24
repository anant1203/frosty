from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from .prompt import AGENT_NAME, DESCRIPTION, INSTRUCTIONS
import src.frosty_ai.objagents.config as cfg

# NOTE: BuiltInCodeExecutor cannot be combined with other tools on the same agent.
# This agent is intentionally tool-free — code execution IS the tool.
ag_sf_streamlit_code_generator = LlmAgent(
    model=cfg.PRIMARY_MODEL,
    name=AGENT_NAME,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    code_executor=BuiltInCodeExecutor(),
)
