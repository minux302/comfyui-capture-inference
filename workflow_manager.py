from pydantic import BaseModel
from PIL import Image
from util import pil_to_base64
import numpy as np
import random
import json

NODE_NAME_LIST = [
    "CheckpointLoaderSimple",
    "KSampler",
    "CLIPTextEncode",
    "ETN_LoadImageBase64",
    "ControlNetApplyAdvanced"
]


class GenerateSettings(BaseModel):
    ckpt_name: str
    prompt: str = "1girl"
    denoising_strength: float = 1.0
    control_strength: float = 1.0
    seed: int = -1
    sampler_name: str = "lcm"


class WorkflowManager:
    def __init__(self, workflow_path):
        self.load_workflow(workflow_path)

    def create(
        self,
        input_img: np.ndarray,
        generate_settings: GenerateSettings,
    ):
        self.workflow[self._node_id_dict["CheckpointLoaderSimple"]]["inputs"][
            "ckpt_name"
        ] = generate_settings.ckpt_name
        self.workflow[self._node_id_dict["CLIPTextEncode"]]["inputs"][
            "text"
        ] = generate_settings.prompt
        if generate_settings.seed == -1:
            seed = random.randint(0, 100000)
        else:
            seed = generate_settings.seed
        self.workflow[self._node_id_dict["KSampler"]]["inputs"]["seed"] = seed
        self.workflow[self._node_id_dict["KSampler"]]["inputs"][
            "denoise"
        ] = generate_settings.denoising_strength
        self.workflow[self._node_id_dict["ETN_LoadImageBase64"]]["inputs"][
            "image"
        ] = pil_to_base64(Image.fromarray(input_img))

        if self._node_id_dict["ControlNetApplyAdvanced"] is not None:
            self.workflow[self._node_id_dict["ControlNetApplyAdvanced"]]["inputs"][
                "strength"
            ] = generate_settings.control_strength
        return self.workflow

    def load_workflow(self, workflow_path: str):
        with open(workflow_path, "r") as f:
            self.workflow = json.load(f)
        self._node_id_dict = create_node_dict(self.workflow)


def get_key_from_class_type(workflow, class_type):
    for key, value in workflow.items():
        if value["class_type"] == class_type:
            return key
    return None


def create_node_dict(workflow):
    return {
        node_name: get_key_from_class_type(workflow, node_name)
        for node_name in NODE_NAME_LIST
    }
