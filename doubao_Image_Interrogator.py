import requests
import torch
import json
from PIL import Image
import io
import base64

class DouBaoImageInterrogator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "your-doubao-api-key"}),
                "model_name": ("STRING", {"default": "doubao-image-captioning-model"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "interrogate"
    CATEGORY = "DouBao"

    def interrogate(self, image, api_key, model_name):
        # 将ComfyUI的图像张量转换为PIL图像
        image_tensor = image[0]  # 取第一张图片
        image_np = image_tensor.cpu().numpy() * 255
        image_np = image_np.astype('uint8')
        pil_image = Image.fromarray(image_np)

        # 将PIL图像转换为base64编码的字符串
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # 构建API请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model_name,
            "image": img_str,
            # 其他可能的参数，根据API文档调整
        }

        # 发送请求
        response = requests.post("https://api.doubao.com/vision/interrogate", headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            # 假设返回的JSON中有一个"description"字段
            description = result.get("description", "")
            return (description,)
        else:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

# 注册节点
NODE_CLASS_MAPPINGS = {
    "DouBaoImageInterrogator": DouBaoImageInterrogator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DouBaoImageInterrogator": "豆包图像反推提示词"
}