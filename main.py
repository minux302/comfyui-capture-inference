import json

from client import Client
from workflow_manager import GenerateSettings, WorkflowManager
from ui import ui
from status_manager import StatusManager


with open("config.json", "r") as f:
    config = json.load(f)
workflow_manager = WorkflowManager(f"workflows/{config['init_workflow']}")
generate_settings = GenerateSettings(**config)
client = Client()
status_manager = StatusManager()

ui = ui(
    config,
    workflow_manager,
    generate_settings,
    client,
    status_manager,
)
ui.queue()
ui.launch()
