from rumorz.copilot import RumorzCopilot
import tinyllm

my_daily_summary_script_path = "/home/othmane/Documents/repos/rumorz-ai/rumorz-sdk/docs/examples/examples.py"

rumorz_copilot = RumorzCopilot(model='azure/gpt-4o')

# "Get the top 2 most positive and negative entities in the last day and get a summary for each"
rumorz_copilot.generate_script(
    script_description="Generate a script that runs the same queries as the SDK tests, except keywords arguments are directly implemented",
    output_path=my_daily_summary_script_path
)

# Run script
#rumorz_copilot.run_script(
#    script_path=my_daily_summary_script_path
#)