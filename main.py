import json
import multiprocessing
from multiprocessing import Array, Queue, Value

from capture_bbox_manager import CaptureBBoxManager
from client import Client
from ui import ui
from workflow_manager import GenerateSettings, WorkflowManager

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    workflow_manager = WorkflowManager(f"workflows/{config['init_workflow']}")
    generate_settings = GenerateSettings(**config)
    client = Client()
    bbox_manager = CaptureBBoxManager()  # must be main process, since uses tkinter

    # shared status between BboxManager(tkinter) and gradio
    shared_queue = Queue()
    shared_is_capturing = Value("i", 0)
    shared_bbox = Array("i", [0, 0, 0, 0])

    ui_process = multiprocessing.Process(
        target=ui,
        args=(
            config,
            workflow_manager,
            generate_settings,
            client,
            shared_queue,
            shared_is_capturing,
            shared_bbox,
        ),
    )
    ui_process.start()

    while True:
        message = shared_queue.get()
        if message == "set_bbox":
            bbox_manager.set_bbox(shared_queue, shared_is_capturing, shared_bbox)
