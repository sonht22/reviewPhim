# File: services/llm_service.py
from abc import ABC, abstractmethod
from typing import List
from core.entities import RecapSegment

class ILLMService(ABC):
    """
    Interface (Khế ước) cho các dịch vụ LLM.
    Mục đích: Giúp ứng dụng không bị phụ thuộc chặt vào một AI cụ thể.
    Sau này muốn đổi từ Gemini sang ChatGPT chỉ cần viết adapter mới, không cần sửa UI.
    """

    @abstractmethod
    def analyze_video_and_generate_script(self, video_path: str) -> List[RecapSegment]:
        """
        Hàm trừu tượng: Nhận vào đường dẫn video -> Trả về danh sách các đoạn phân tích.
        """
        pass