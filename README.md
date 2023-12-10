# comfy-capture-inference
A tool that captures the screen and infers via api to ComfyUI. Operation and display is done in Gradio.


## Requirements 
### client (this repo)
```
$ pip install -r requirements.txt
```

### server (ComfyUI)
```
# Setup https://github.com/comfyanonymous/ComfyUI
# Install below custom nodes.
# - https://github.com/Fannovel16/comfyui_controlnet_aux.git
# - https://github.com/Acly/comfyui-tooling-nodes
# Put
# - `Comfyui/models/loras/lcm-lora-sdv1-5.safetensors`
# - `Comfyui/models/controlnet/control_v11p_sd15_lineart.pth`
# - `Comfyui/models/controlnet/control_v11p_sd15_scribble.pth`
```


## Usage
Describe the configuration in the config file. The model should be placed according to the ComfyUI configuration.
```
# config.json
{
    "init_workflow": "sd15_img2img.json",
    "ckpt_name": "sdhk_v40.safetensors",
    "seed": -1
}
```

```
# client
$ python main.py

# server (comfyUI)
$ python main.py
```


## Custom Workflow
If a custom workflow is placed under a workflow, inference can be performed using that workflow. The following requirements must be met Please refer to the sample workflows.

- I/O nodes must be `LoadImageBase64` and `SendImageWebSocket`.
- Each I/O node must be one.