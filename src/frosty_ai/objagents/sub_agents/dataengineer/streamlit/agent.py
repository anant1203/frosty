import os
from google.adk.agents import SequentialAgent
from google.genai import types
from .prompt import AGENT_NAME, DESCRIPTION
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.code_generator import ag_sf_streamlit_code_generator
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.stage_creator import ag_sf_streamlit_stage_creator
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.procedure_creator import ag_sf_streamlit_procedure_creator
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.file_uploader import ag_sf_streamlit_file_uploader
from src.frosty_ai.objagents.sub_agents.dataengineer.streamlit.app_deployer import ag_sf_streamlit_app_deployer


def _require_gemini(callback_context):
    """Block Streamlit app generation for non-Gemini providers.

    BuiltInCodeExecutor used by the code generator is a Gemini-native ADK
    feature — it will fail with any other provider. Return an explanatory
    message to the manager so the user gets a clear error instead of a
    cryptic runtime failure.
    """
    provider = os.environ.get("MODEL_PROVIDER", "google").strip().lower()
    if provider != "google":
        return types.Content(
            role="model",
            parts=[types.Part(text=(
                f"⚠️ Streamlit app generation is unavailable with the current model provider (`{provider}`). "
                "The code generation step relies on ADK's `BuiltInCodeExecutor`, which is a Gemini-native "
                "feature and cannot run with OpenAI or Anthropic models.\n\n"
                "To enable Streamlit app generation for non-Gemini providers, replace `BuiltInCodeExecutor` "
                "in `src/frosty_ai/objagents/sub_agents/dataengineer/streamlit/code_generator/agent.py` "
                "with a custom `CodeExecutor` implementation — for example, a subprocess-based executor "
                "or a sandboxed Docker runner. See the ADK documentation for `BaseCodeExecutor`."
            ))],
        )
    return None


ag_sf_manage_streamlit = SequentialAgent(
    name=AGENT_NAME,
    description=DESCRIPTION,
    before_agent_callback=_require_gemini,
    sub_agents=[
        ag_sf_streamlit_code_generator,    # Step 1: generate Python app code
        ag_sf_streamlit_stage_creator,     # Step 2: create internal stage
        ag_sf_streamlit_procedure_creator, # Step 3: create upload helper procedure
        ag_sf_streamlit_file_uploader,     # Step 4: upload app file to stage
        ag_sf_streamlit_app_deployer,      # Step 5: deploy Streamlit object
    ],
)
