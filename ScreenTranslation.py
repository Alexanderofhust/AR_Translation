import pytesseract
from PIL import ImageGrab, Image, ImageDraw, ImageFont
import requests

# 配置Tesseract的路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 请根据实际路径修改

class ARTranslator:
    def __init__(self, api_url):
        self.api_url = api_url

    def capture_screen(self):
        """捕获屏幕截图并保存为文件"""
        screen = ImageGrab.grab()
        screen.save('screenshot.png')
        return 'screenshot.png'

    def extract_text_from_image(self, image_path):
        """使用Tesseract-OCR从图像中提取文字"""
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
        return text

    def translate_text(self, text, target_language='zh-CHS'):
        """使用有道翻译API进行翻译"""
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'q': text,
            'from': 'auto',  # 自动识别源语言
            'to': target_language,
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['translation'][0]
        else:
            return None

    def overlay_translation(self, image_path, translation):
        """将翻译结果显示在原画面上"""
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 15)  # 选择合适的字体和大小
        width, height = image.size

        # 将翻译结果显示在屏幕下方
        for line in translation.split('\n'):
            text_width, text_height = draw.textsize(line, font=font)
            x = (width - text_width) / 2
            y = height - text_height * 5  # 根据需要调整位置
            draw.text((x, y), line, (255, 255, 255), font=font)
            y += text_height * 5

        image.save('translated_screenshot.png')
        return 'translated_screenshot.png'

    def translate_screenshot(self):
        """整合所有步骤"""
        image_path = self.capture_screen()
        text = self.extract_text_from_image(image_path)
        translation = self.translate_text(text)
        return self.overlay_translation(image_path, translation)

def main():
    api_url = "YOUR_YODU_TRANSLATE_API_URL"  # 替换成你的有道翻译API的实际URL
    translator = ARTranslator(api_url)
    translated_image_path = translator.translate_screenshot()
    print(f"Translated image saved as {translated_image_path}")

if __name__ == "__main__":
    main()