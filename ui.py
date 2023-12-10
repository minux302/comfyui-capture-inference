import os
import functools
import gradio as gr

from workflow_manager import GenerateSettings, WorkflowManager
from status_manager import StatusManager
from client import Client


workflow_list = os.listdir("workflows")
status_manager = StatusManager()


def run_capture():
    status_manager.run_capture()


def stop_capture():
    status_manager.stop_capture()


def load_workflow(workflow_name: str, workflow_manager: WorkflowManager):
    # For convenience of gradio's event handler, set the variable specified
    # by functool to the back
    workflow_manager.load_workflow(f"workflows/{workflow_name}")
    if "control" in workflow_name:
        return gr.update(visible=True)
    else:
        return gr.update(visible=False)


def run_generate(
    workflow_manager: WorkflowManager,
    generate_settings: GenerateSettings,
    client: Client,
):
    capture_img = status_manager.capture_img
    is_captureing = status_manager.is_capturing

    if capture_img is None or not is_captureing:
        result_img = status_manager.result_img
        if result_img is not None:
            img_h, img_w, _ = result_img.shape
            return gr.update(value=result_img, height=img_h, width=img_w)
        else:
            return

    workflow = workflow_manager.create(
        input_img=capture_img,
        generate_settings=generate_settings,
    )
    prompt_id = client.enqueue(workflow)
    result_img = client.polling(prompt_id)
    status_manager.result_img = result_img
    img_h, img_w, _ = result_img.shape
    return gr.update(value=result_img, height=img_h, width=img_w)


def ui(
    config: dict,
    workflow_manager: WorkflowManager,
    generate_settings: GenerateSettings,
    client: Client,
):
    with gr.Blocks() as ui:
        capture_button = gr.Button("capture")
        stop_button = gr.Button("stop")
        prompt = gr.Textbox(label="prompt", value="1girl")
        ckpt_name = gr.Textbox(label="ckpt_name", value=config["ckpt_name"])
        denoising_strength = gr.Slider(
            minimum=0, maximum=1, value=1.0, label="denoising strength"
        )
        control_strength = gr.Slider(
            minimum=0, maximum=1, value=1.0, label="control strength", visible=False
        )
        workflow_dropdown = gr.Dropdown(
            choices=[x for x in workflow_list],
            label="workflow",
            value=config["init_workflow"],
        )
        image_output = gr.Image()
        capture_button.click(fn=run_capture, inputs=[], outputs=[])
        stop_button.click(fn=stop_capture, inputs=[], outputs=[])
        prompt.change(
            fn=lambda x: setattr(generate_settings, "prompt", x),
            inputs=[prompt],
            outputs=None,
        )
        ckpt_name.change(
            fn=lambda x: setattr(generate_settings, "ckpt_name", x),
            inputs=[ckpt_name],
            outputs=None,
        )
        denoising_strength.change(
            fn=lambda x: setattr(generate_settings, "denoising_strength", x),
            inputs=[denoising_strength],
            outputs=None,
        )
        control_strength.change(
            fn=lambda x: setattr(generate_settings, "control_strength", x),
            inputs=[control_strength],
            outputs=None,
        )
        workflow_dropdown.change(
            fn=functools.partial(load_workflow, workflow_manager=workflow_manager),
            inputs=[workflow_dropdown],
            outputs=[control_strength],
        )
        ui.load(
            fn=lambda: run_generate(workflow_manager, generate_settings, client),
            inputs=[],
            outputs=image_output,
            every=0.01,
        )
    return ui
