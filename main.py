import json
import multiprocessing
from multiprocessing import Queue, Value, Array
from client import Client
from workflow_manager import GenerateSettings, WorkflowManager
from ui import ui
from capture_bbox_manager import CaptureBBoxManager


def set_bbox(queue, is_captureing, bbox):
    bbox_manager.run()
    is_captureing.value = 1
    bbox_obj = bbox_manager.bbox
    bbox[0] = bbox_obj.x1
    bbox[1] = bbox_obj.y1
    bbox[2] = bbox_obj.x2
    bbox[3] = bbox_obj.y2
    queue.put("done")


with open("config.json", "r") as f:
    config = json.load(f)
workflow_manager = WorkflowManager(f"workflows/{config['init_workflow']}")
generate_settings = GenerateSettings(**config)
client = Client()
bbox_manager = CaptureBBoxManager()  # must be main process, since uses tkinter

# status shared between processes
queue = Queue()
is_capturing = Value('i', 0)
bbox = Array('i', [0, 0, 0, 0])

ui_process = multiprocessing.Process(
    target=ui,
    args=(
        config,
        workflow_manager,
        generate_settings,
        client,
        queue,
        is_capturing,
        bbox
    ),
)
ui_process.start()

while True:
    message = queue.get()
    if message == "set_bbox":
        set_bbox(queue, is_capturing, bbox)
