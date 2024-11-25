import importlib.util
import json
import subprocess
import traceback
from textwrap import dedent

from litellm import completion
from pydantic import BaseModel, Field


class RumorzCopilot:

    def __init__(self,
                 model):
        self.model = model

    def load_sdk_source_code(self):
        package_name = "rumorz"
        spec = importlib.util.find_spec(package_name)
        # Find the spec for the package
        if spec and spec.origin:
            sdk_path = spec.origin.replace('__init__.py', '')
        else:
            raise Exception(f"Package {package_name} not found  ")

        client_path = sdk_path + 'client.py'
        enums_path = sdk_path + 'enums.py'
        test_path = sdk_path + 'tests/test_sdk.py'
        # read content
        with open(client_path, 'r') as file:
            client_content = file.read()
        with open(enums_path, 'r') as file:
            enums_content = file.read()
        with open(test_path, 'r') as file:
            test_content = file.read()
        docs = dedent(f"""
<RUMORZ SDK SOURCE CODE>
file_path: {client_path}
{client_content}
<ENUMS>
file_path: {enums_path}
{enums_content}
<TESTS>
file_path: {test_path}
{test_content}
""")

        return docs

    def run_script(self, script_path):
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        return result.stdout

    def generate_script(self, script_description, output_path):

        source_code = self.load_sdk_source_code()

        class SDKCopilotResponse(BaseModel):
            reasoning: str = Field(...,
                                   description="Write a complete reasoning and planning on requirements and steps to write the script based on the documentation and the provided script description")
            script_code: str = Field(..., description="The Python script code")

        response = completion(
            model=self.model,
            response_format=SDKCopilotResponse,
            messages=[
                {"role": "system", "content": f"""
ROLE:
You are an expert in Programming and the Rumorz Python SDK. Rumorz provides Financial markets AI intelligence through
the Graph and an Agent. The Graph gives access to entities (tokens, people, companies, etc.) and their posts, sentiment
etc. The Agent provides summaries and insights on entities. 

TASK
You are tasked to create a fully working Python script based on user input. The script must use the Rumorz Python SDK. 
Your output will be in json

GUIDELINES
- Use pandas sort_values to rank by the desired metric
- Minimize the number of API queries.
- If you hesitate, tell the user to ask again with specific improvements to make in his query
- Your script should always print a success message with details at the end of the execution

DOCUMENTATION
Use the following documentation and Enums to build working queries:
{source_code}
"""},
                {"role": "user",
                 "content": f"The user message to describe the script required: {script_description}"},
            ],

        )

        class RumorzCopilotException(Exception):
            pass

        try:
            script_code = json.loads(response.choices[0].message.content)['script_code']
            with open(output_path, 'w') as f:
                f.write(script_code)
        except Exception as e:
            raise RumorzCopilotException("Error while parsing LLM response ", traceback.format_exc())
