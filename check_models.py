from google import genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Không thấy API Key!")
    exit()

print("🚀 Đang kết nối tới Google để lấy danh sách Model...")
client = genai.Client(api_key=api_key)

try:
    # Lấy danh sách tất cả model
    print("\n📋 DANH SÁCH MODEL BẠN ĐƯỢC DÙNG:")
    print("-------------------------------------")
    count = 0
    for model in client.models.list():
        # Chỉ hiện những model có chữ 'flash' hoặc 'pro' để dễ nhìn
        name = model.name.replace("models/", "")
        if "flash" in name or "pro" in name:
            print(f"✅ {name}")
            count += 1
    
    if count == 0:
        print("⚠️ Không tìm thấy model Flash/Pro nào. Hãy in tất cả:")
        for model in client.models.list():
             print(f"- {model.name.replace('models/', '')}")

except Exception as e:
    print(f"❌ Lỗi: {e}")