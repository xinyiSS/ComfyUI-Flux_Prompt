from .flux_prompt_enhancer import FluxPromptEnhancer
from .flux_prompt_generator import FluxPromptGenerator

NODE_CLASS_MAPPINGS = {
    "FluxPromptEnhancer": FluxPromptEnhancer,
    "FluxPromptGenerator": FluxPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPromptEnhancer": "Flux Prompt Enhancer",
    "FluxPromptGenerator": "Flux Prompt Generator"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

