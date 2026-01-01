import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# HOẶC: Dán trực tiếp key vào đây nếu bạn chưa làm file .env (chỉ để test)
# api_key = "AIzaSy..... (Key của bạn)" 

if not api_key:
    print("❌ LỖI: Chưa tìm thấy API Key!")
    exit()

print(f"🔑 Đã tìm thấy Key: {api_key[:5]}...*****")

try:
    # 2. Cấu hình
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Dùng bản Flash cho nhanh

    # 3. Gửi tin nhắn test
    print("📡 Đang gửi tin nhắn tới Gemini...")
    response = model.generate_content("Chào Gemini, bạn có hoạt động không? Trả lời ngắn gọn bằng tiếng Việt.")
    
    # 4. Kết quả
    print("\n✅ THÀNH CÔNG! Gemini trả lời:")
    print("-----------------------------")
    print(response.text)
    print("-----------------------------")

except Exception as e:
    print("\n❌ THẤT BẠI. Chi tiết lỗi:")
    print(e)