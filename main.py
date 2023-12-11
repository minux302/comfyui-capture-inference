import json
import multiprocessing
from multiprocessing import Queue, Value, Array
from client import Client
from workflow_manager import GenerateSettings, WorkflowManager
from ui import ui
from status_manager import StatusManager
from capture_bbox_manager import CaptureBBoxManager


def run_capture(queue, is_captureing, bbox):
    bbox_manager.run()
    is_captureing.value = 1
    # x1, y1, x2, y2 = bbox_manager.bbox
    bbox_obj = bbox_manager.bbox
    # print(x1, y1, x2, y2)
    bbox[0] = bbox_obj.x1
    bbox[1] = bbox_obj.y1
    bbox[2] = bbox_obj.x2
    bbox[3] = bbox_obj.y2
    queue.put("set_bbox")


def stop_capture(is_captureing, bbox):
    is_captureing.value = 0


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    workflow_manager = WorkflowManager(f"workflows/{config['init_workflow']}")
    generate_settings = GenerateSettings(**config)
    client = Client()
    bbox_manager = CaptureBBoxManager()
    status_manager = StatusManager()

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
            status_manager,
            queue,
            is_capturing,
            bbox
        ),
    )
    ui_process.start()

    while True:
        message = queue.get()
        print("Received message:", message)
        if message == "run_capture":
            run_capture(queue, is_capturing, bbox)
        elif message == "stop_capture":
            stop_capture(queue, is_capturing, bbox)
