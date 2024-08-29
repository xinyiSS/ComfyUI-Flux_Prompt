from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class FluxPromptEnhancer:
    def __init__(self):
        # 模型路径
        model_path = "F:/ComfyUI_windows_portable/ComfyUI/models/LLM/Flux-Prompt-Enhance"
        
        # 尝试加载分词器，禁用Fast分词器版本
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_length": ("INT", {"default": 256, "min": 1, "max": 1024, "step": 1}),
                "repetition_penalty": ("FLOAT", {"default": 1.2, "min": 1.0, "max": 3.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "enhance_prompt"

    CATEGORY = "Text/Enhancement"

    def enhance_prompt(self, prompt, max_length, repetition_penalty):
        # 初始化pipeline时传入调节参数
        enhancer = pipeline(
            'text2text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            repetition_penalty=repetition_penalty,
            device=0  # 使用GPU（如果可用）
        )
        prefix = "enhance prompt: "
        answer = enhancer(prefix + prompt, max_length=max_length)
        return (answer[0]['generated_text'],)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "FluxPromptEnhancer": FluxPromptEnhancer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPromptEnhancer": "Flux Prompt Enhancer"
}
