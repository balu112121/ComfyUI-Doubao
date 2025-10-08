import requests
import json
import nodes

class DouBaoPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "base_prompt": ("STRING", {"default": "Please generate a logo design prompt for:"}),
                "user_input": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "豆包大模型"

    def generate_prompt(self, api_key, base_prompt, user_input):
        # 构建API请求
        url = "https://api.doubao.com/v1/chat/completions"  # 假设的豆包API端点
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "doubao-model",  # 假设的模型名称
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for generating logo design prompts."},
                {"role": "user", "content": f"{base_prompt} {user_input}"}
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            # 假设返回格式与OpenAI类似，取第一个choices的message的content
            generated_text = result['choices'][0]['message']['content']
        else:
            generated_text = f"Error: {response.status_code} - {response.text}"

        return (generated_text,)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "DouBaoPrompt": DouBaoPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DouBaoPrompt": "豆包提示词生成"
}