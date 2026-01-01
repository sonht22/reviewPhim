from google import genai
from google.genai import types
import json
import re
import os
import time
from typing import List
# Giả định bạn đã có các class này trong project
from core.entities import RecapSegment, TimeRange
from services.llm_service import ILLMService

class GeminiAdapter(ILLMService):
    def __init__(self, api_key: str):
        # Khởi tạo Client
        self.client = genai.Client(api_key=api_key)
        # CHỐT: Dùng bản 2.0 Flash (Experimental) - Nhanh & Free
        self.model_name = "gemini-2.0-flash-exp" 

    def _upload_file(self, path: str):
        print(f"🚀 Đang upload video lên Gemini: {path}...")
        
        # Upload file
        # Lưu ý: SDK mới tự xử lý mime type, nhưng file video nên là mp4
        file = self.client.files.upload(file=path)
        
        # Đợi file xử lý (Active)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(2)
            file = self.client.files.get(name=file.name)
            
        if file.state.name == "FAILED":
            raise ValueError("Upload thất bại! File video có vấn đề hoặc sai định dạng.")
            
        print(f"\n✅ Video đã sẵn sàng: {file.uri}")
        return file

    def analyze_video_and_generate_script(self, video_path: str) -> List[RecapSegment]:
        # 1. Upload
        try:
            video_file = self._upload_file(video_path)
        except Exception as e:
            print(f"❌ Lỗi Upload: {e}")
            return []
        
        # 2. Tạo Prompt (Lệnh) - Đã tối ưu cho Review Phim
        prompt = """
        Bạn là AI Editor chuyên nghiệp. Hãy xem video và tóm tắt cốt truyện theo phong cách hài hước, nhanh gọn.
        
        OUTPUT FORMAT: JSON List.
        Mỗi phần tử gồm: 
        - id: số thứ tự
        - script: lời thoại tóm tắt (ngắn gọn, khoảng 10-15 từ/câu)
        - start_time: format HH:MM:SS
        - end_time: format HH:MM:SS
        - visual_description: mô tả cảnh phim
        
        Yêu cầu quan trọng: 
        1. Chỉ trả về JSON thuần.
        2. Timestamp phải khớp chính xác với hành động trong video.
        """
        
        print(f"🧠 Gemini ({self.model_name}) đang xem phim và viết kịch bản...")
        
        # 3. Gọi API
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[video_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json" # Ép trả về JSON chuẩn
                )
            )

            # 4. Xử lý kết quả
            text_resp = response.text
            # Clean Markdown (phòng hờ)
            clean_text = re.sub(r"```json|```", "", text_resp).strip()
            
            data = json.loads(clean_text)
            
            # Convert sang Entity (CDM)
            segments = []
            for item in data:
                # Validate dữ liệu cơ bản
                start = item.get('start_time', '00:00:00')
                end = item.get('end_time', '00:00:05')
                
                seg = RecapSegment(
                    id=item.get('id', 0),
                    script=item.get('script', ''),
                    visual_time=TimeRange(start, end),
                    visual_description=item.get('visual_description', "")
                )
                segments.append(seg)
            
            print(f"✅ Đã tạo được {len(segments)} segments!")
            return segments

        except Exception as e:
            print(f"❌ Lỗi khi phân tích: {e}")
            # In ra raw response để debug nếu lỗi JSON
            if 'text_resp' in locals():
                print(f"Raw data: {text_resp[:100]}...") 
            return []