from google import genai
from google.genai import types
import json
import re
import time
import os
import mimetypes
from typing import List

from core.entities import RecapSegment, TimeRange
from services.llm_service import ILLMService

class GeminiAdapter(ILLMService):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("❌ Lỗi: API Key bị thiếu.")
        
        self.client = genai.Client(api_key=api_key)
        
        # --- [CHỐT HẠ: DÙNG MODEL NÀY] ---
        # Dựa trên danh sách bạn vừa gửi, đây là model ngon nhất:
        self.model_name = "gemini-flash-latest"
        
        # Mẹo: Nếu vẫn bị lỗi 429 (hết lượt), hãy đổi thành dòng dưới:
        # self.model_name = "gemini-2.0-flash-lite"

    def _upload_video(self, video_path: str):
        print(f"🚀 Đang upload video: {os.path.basename(video_path)}...")
        mime_type, _ = mimetypes.guess_type(video_path)
        if not mime_type: mime_type = "video/mp4"

        try:
            with open(video_path, "rb") as f:
                file_obj = self.client.files.upload(
                    file=f,
                    config=types.UploadFileConfig(
                        mime_type=mime_type,
                        display_name="input_video"
                    )
                )
            
            print("⏳ Đang chờ Google xử lý video...", end="", flush=True)
            while True:
                file_check = self.client.files.get(name=file_obj.name)
                if file_check.state.name == "ACTIVE":
                    print(f"\n✅ Video đã sẵn sàng! (URI: {file_check.uri})")
                    return file_check
                if file_check.state.name == "FAILED":
                    raise ValueError(f"❌ Upload thất bại: {file_check.error.message}")
                time.sleep(2)
                print(".", end="", flush=True)
                
        except Exception as e:
            print(f"\n❌ Lỗi Upload: {str(e)}")
            raise e

    def analyze_video_and_generate_script(self, video_path: str) -> List[RecapSegment]:
        try:
            video_file = self._upload_video(video_path)
        except Exception:
            return []

        prompt = """
        Bạn là AI Video Editor chuyên nghiệp. 
        Nhiệm vụ: Xem video và tóm tắt cốt truyện thành các câu thoại ngắn (script) hài hước.
        OUTPUT FORMAT: JSON Array.
        [{"id": 1, "script": "...", "start_time": "00:00:00", "end_time": "00:00:05", "visual_description": "..."}]
        """

        print(f"🧠 Gemini ({self.model_name}) đang phân tích phim...")

        # --- [CƠ CHẾ TỰ ĐỘNG THỬ LẠI KHI BỊ 429] ---
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[video_file, prompt],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                
                # Nếu chạy đến đây là thành công, thoát vòng lặp retry
                clean_text = re.sub(r"```json|```", "", response.text).strip()
                data = json.loads(clean_text)
                
                results = []
                for item in data:
                    seg = RecapSegment(
                        id=item.get('id', 0),
                        script=item.get('script', ''),
                        visual_time=TimeRange(item.get('start_time', '00:00:00'), item.get('end_time', '00:00:00')),
                        visual_description=item.get('visual_description', '')
                    )
                    results.append(seg)
                
                print(f"✅ Thành công! Đã tạo {len(results)} segments.")
                return results

            except Exception as e:
                error_str = str(e)
                # Kiểm tra nếu là lỗi 429 (Resource Exhausted)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = 10 * (attempt + 1) # Lần 1 chờ 10s, lần 2 chờ 20s...
                    print(f"\n⚠️ Quá tải (429). Đang chờ {wait_time}s để thử lại lần {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    # Nếu là lỗi khác thì báo luôn
                    print(f"❌ Lỗi khi gọi AI: {e}")
                    return []
        
        print("❌ Đã thử lại nhiều lần nhưng vẫn thất bại.")
        return []