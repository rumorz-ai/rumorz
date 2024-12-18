"""
This file is used to generate the examples and openapi.yaml file for the Rumorz AI SDK.
It's run locally and is not meant to be exportable. It is mainly here as a reference

"""
import re

from rumorz.copilot import RumorzCopilot
from rumorz_backend.app import FUNCTION_REGISTRY
from smartpy.utility import os_util
from tinyllm.util.prompt_util import extract_function_signature

EXAMPLES = True
OPENAPI = False
ENUMS = False


rumorz_copilot = RumorzCopilot(model='azure/gpt-4o')

if EXAMPLES:
    examples_path = os_util.joinPaths([os_util.getCurrentDirPath(), 'docs/examples/examples.py'])

    # "Get the top 2 most positive and negative entities in the last day and get a summary for each"
    rumorz_copilot.create_file(
        file_description="""
    Generate a .py script that serves as an example of the capabilities of the SDK. Use the SDK tests as the base, and generate
    an insightful script that showcases the SDK capabilities. In this script, use keyword arguments directly when using 
    the rumroz_client.
    
    The script should have a single main() function and should run the workflow: summary for the top 2 people with the most
    positive and negative sentiment in the last 7 days. 
    The script should print the results of each step.
    
    GUIDELINES:
    - Use enums like lookback=Lookback.ONE_WEEK 
    - Set the api key like api_key=os.environ['RUMORZ_API_KEY']
    """,
        output_path=examples_path
    )

    # Run script
    output = rumorz_copilot.run_script(
        script_path=examples_path
    )

    examples_pmdx = '/home/othmane/Documents/repos/rumorz-ai/docs/examples.mdx'
    with open(examples_path, 'r') as f:
        script_code = f.read()
    with open(examples_pmdx, 'r') as f:
        examples_mdx = f.read()
    script_code = f"```python\n{script_code}\n```"
    examples_mdx = re.sub(r'```python\n.*\n```', script_code, examples_mdx)
    with open(examples_pmdx, 'w') as f:
        f.write(examples_mdx)

if OPENAPI:
    openai_yaml_path = '/home/othmane/Documents/repos/rumorz-ai/docs/api-reference/openapi.yaml'
    to_ignore = ['create_alert', 'create_alert_examples', 'delete_alert', 'update_alert_examples']

    function_signatures = """The endpoint signatures are:"""
    for endpoint, function in FUNCTION_REGISTRY.items():
        if not any([ignore in endpoint for ignore in to_ignore]):
            function_signatures += '\n' + endpoint.replace('v0/','') + ':\n' + str(extract_function_signature(function))

    # Get function signatures

    rumorz_copilot.create_file(
        output_block="yaml",
        file_description=f"""
Generate a complete openai.yaml file with the following requirements:
- All endpoints should be documented as paths
- Put the name of the endpoint under "summary"
- Use the provided function signatures for typing
- server url is https://rumorz.azurewebsites.net/v0
- Include the description of the endpoint under "description:"
- You must include all enums
- Make sure to include API key authentication
- Use the endpoint test from the unit tests to generate examples for each path.

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
security:
  - ApiKeyAuth: []


- The final content should be enclosed within  ```yaml  ``` 
- Use the bitcoin_entity_id from test_sdk in the endpoint Call examples

<Example endpoint>
  /graph/get_feed:
    post:
      tags:
        - Graph
      summary: get_feed
      description: Get the feed of posts related to the specified entities and filters.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                ids:
                  type: array
                  items:
                    type: string
                lookback:
                  type: string
                  enum: [1H, 6H, 12H, 1D, 7D, 30D, 90D]
                  description: Time period to look back
                scores_filter:
                  type: string
                page:
                  type: integer
                limit:
                  type: integer
            example:
              name_search: "Bitcoin"
              symbol_search: "BTC"
              asset_class: "crypto"
              entity_type: "financial_asset"
              page: 1
              limit: 1
      responses:
        '200':
          description: Success
          
<End of Example endpoint>
""",
        output_path=openai_yaml_path
    )

if ENUMS:
    enums_path = '/home/othmane/Documents/repos/rumorz-ai/docs/enums.mdx'
    rumorz_copilot.create_file(
        file_description="""
Generate a complete enums.mdx file with the following requirements:
- All the Enums should be documented
- Enum definitions should be enclosed within ```python ``` blocks
- Use UI friendly, Production standard syntax and layouts

Example enum documentation:

## Lookback

```python
from enum import Enum

class Lookback(Enum):
    '''
    Enum representing different lookback periods for data metrics.
    '''
    ONE_HOUR = "1H"
    SIX_HOURS = "6H"
    TWELVE_HOURS = "12H"
    ONE_DAY = "1D"
    ONE_WEEK = "7D"
    ONE_MONTH = "30D"
    THREE_MONTHS = "90D"
```
    """,
        output_path=enums_path
    )

