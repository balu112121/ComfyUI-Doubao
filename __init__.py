# ComfyUI-Doubao 节点
# 初始化文件
from .doubao_prompt_generator import DoubaoPromptGenerator

NODE_CLASS_MAPPINGS = {
    "DoubaoPromptGenerator": DoubaoPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoubaoPromptGenerator": "豆包提示词生成器"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']