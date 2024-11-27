from rumorz.copilot import RumorzCopilot
import tinyllm

examples_path = "/home/othmane/Documents/repos/rumorz-ai/rumorz/docs/examples/examples.py"

rumorz_copilot = RumorzCopilot(model='azure/gpt-4o')

# "Get the top 2 most positive and negative entities in the last day and get a summary for each"
rumorz_copilot.generate_script(
    script_description="""
Generate a script that serves as an example of the capabilities of the SDK. Use the SDK tests as the base, and generate
an insightful script that showcases the SDK capabilities. In this script, use keyword arguments directly when using 
the rumroz_client.

The script should have a single main() function and should run the workflow: summary for the top 2 people with the most
positive and negative sentiment in the 7 days. 
The script should print the results of each step.
    """,
    output_path=examples_path
)

# Run script
#rumorz_copilot.run_script(
#    script_path=examples_path
#)