import logging
import os
from pathlib import Path

import hydra
from mlx_lm import generate, load
from omegaconf import DictConfig

from src.blender_utils.render import run_script_and_render_image
from src.blender_utils.run_script import run_script_and_save_obj
from src.config import get_brightness
from src.llm_utils import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../config", config_name="run_blendernet.yaml")
def main(cfg_dict: DictConfig):
    model, tokenizer = load(cfg_dict.model_path)

    env_prompt = os.environ.get("PROMPT", None)
    if env_prompt is not None:
        cfg_dict.prompt = env_prompt

    if cfg_dict.prompt is None:
        raise ValueError(f"Prompt is required! Current prompt: {cfg_dict.prompt}")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": cfg_dict.prompt}]

    logger.info(f"Prompt: {cfg_dict.prompt}")
    logger.info(f"Obj name: {cfg_dict.obj_name}")
    logger.info(f"Brightness: {cfg_dict.brightness}")
    logger.info(f"Blender executable: {cfg_dict.blender_exe_path}")
    logger.info(f"Output path: {cfg_dict.output_path}")
    logger.info(f"Verbose: {cfg_dict.verbose}")

    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    response = generate(
        model, tokenizer=tokenizer, prompt=prompt, verbose=cfg_dict.verbose, max_tokens=cfg_dict.max_tokens
    )

    logger.info(f"Response:\n\n   {response}\n")
    blender_executable = Path(cfg_dict.blender_exe_path)

    output_dir = Path(cfg_dict.output_path).resolve() / cfg_dict.obj_name
    output_dir.mkdir(parents=True, exist_ok=True)
    obj_path = run_script_and_save_obj(
        response, cfg_dict.obj_name, output_dir, blender_executable
    )
    logger.info(f"Saved object at {obj_path}")

    run_script_and_render_image(
        response,
        obj_name=cfg_dict.obj_name,
        output_folder=output_dir,
        obj_path=obj_path,
        blender_executable=blender_executable,
        brightness=get_brightness(cfg_dict.brightness),
    )


if __name__ == "__main__":
    main()
