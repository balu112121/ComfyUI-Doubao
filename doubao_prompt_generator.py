import requests
import json
import torch
from comfy.nodes import Node
import comfy.utils

# 豆包提示词生成节点
class DoubaoPromptGenerator(Node):
    """
    使用豆包大模型生成AI提示词的节点
    
    输入:
        - api_key: 豆包API密钥
        - prompt_requirement: 提示词需求描述
        - style: 提示词风格 (可选)
        - length: 生成提示词的大致长度 (可选)
        - temperature: 生成随机性参数 (0-1，可选)
    
    输出:
        - generated_prompt: 生成的提示词
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "prompt_requirement": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "style": ("STRING", {"default": "详细、生动、富有画面感", "multiline": False}),
                "length": ("INT", {"default": 100, "min": 50, "max": 500, "step": 10}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.1, "max": 1.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "提示词生成/豆包"

    def generate_prompt(self, api_key, prompt_requirement, style="详细、生动、富有画面感", 
                        length=100, temperature=0.7):
        """生成提示词的主函数"""
        if not api_key:
            raise ValueError("请输入有效的豆包API密钥")
            
        if not prompt_requirement:
            raise ValueError("请输入提示词需求")
        
        try:
            # 构建提示词生成的指令
            instruction = f"""请根据以下需求生成一个适合AI图像生成的提示词：
需求：{prompt_requirement}
风格要求：{style}
大致长度：约{length}字
请确保生成的提示词详细、准确，能够引导AI生成符合预期的内容。
"""
            
            # 调用豆包API
            generated_prompt = self.call_doubao_api(api_key, instruction, temperature)
            
            # 清理生成结果
            generated_prompt = self.clean_prompt(generated_prompt)
            
            return (generated_prompt,)
            
        except Exception as e:
            print(f"生成提示词时出错: {str(e)}")
            raise

    def call_doubao_api(self, api_key, prompt, temperature=0.7):
        """调用豆包API生成内容"""
        # 豆包API端点 (请根据实际API地址修改)
        url = "https://api.doubao.com/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "ernie-bot",  # 可根据实际模型名称修改
            "messages": [
                {"role": "system", "content": "你是一个专业的AI提示词生成助手，擅长生成高质量的图像生成提示词。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # 抛出HTTP错误
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {str(e)}，响应内容: {response.text}")

    def clean_prompt(self, prompt):
        """清理生成的提示词，去除多余内容"""
        # 去除首尾空白
        prompt = prompt.strip()
        
        # 去除可能的前缀，如"生成的提示词："等
        prefixes = ["提示词：", "生成的提示词：", "结果："]
        for prefix in prefixes:
            if prompt.startswith(prefix):
                prompt = prompt[len(prefix):].strip()
                break
                
        return prompt

# 注册节点
NODE_CLASS_MAPPINGS = {
    "DoubaoPromptGenerator": DoubaoPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoubaoPromptGenerator": "豆包提示词生成器"
}

if __name__ == "__main__":
    # 测试代码
    import os
    from dotenv import load_dotenv
    
    # 加载环境变量（仅用于测试）
    load_dotenv()
    api_key = os.getenv("DOUBAO_API_KEY")
    
    if api_key:
        generator = DoubaoPromptGenerator()
        try:
            prompt = generator.generate_prompt(
                api_key=api_key,
                prompt_requirement="一只在太空漂浮的猫，未来科技风格",
                style="超现实主义，细节丰富，8K分辨率",
                length=150,
                temperature=0.8
            )
            print("生成的提示词：")
            print(prompt[0])
        except Exception as e:
            print(f"测试失败: {e}")
    else:
        print("请设置DOUBAO_API_KEY环境变量进行测试")
