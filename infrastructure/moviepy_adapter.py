import os
from moviepy.editor import VideoFileClip

class MoviePyAdapter:
    def cut_video(self, input_path: str, start_time: float, end_time: float, output_path: str):
        
        # 1. Kiểm tra file gốc
        if not os.path.exists(input_path):
            return False, f"❌ Không tìm thấy file gốc: {input_path}", None

        print(f"🎬 [MoviePy] Input: {os.path.basename(input_path)}")

        # =================================================================================
        # [CẤU HÌNH ĐƯỜNG DẪN CỨNG - HARDCODED PATH]
        # =================================================================================
        # Sử dụng os.path.normpath để Windows tự sửa dấu gạch chéo xuôi/ngược cho chuẩn
        ROOT_DIR = r"D:\CU SƠN\tool\reviewPhim"
        BUFFER_DIR_NAME = "buffermemory" # Tên folder viết liền, không dấu cách
        
        # Đường dẫn tuyệt đối đến folder buffermemory
        buffer_dir = os.path.normpath(os.path.join(ROOT_DIR, BUFFER_DIR_NAME))

        # Đường dẫn file tạm (để giấu file rác temp-audio.m4a vào đây luôn cho gọn)
        temp_audio_path = os.path.join(buffer_dir, "temp-audio.m4a")
        # =================================================================================

        try:
            # Tạo folder nếu chưa có
            if not os.path.exists(buffer_dir):
                os.makedirs(buffer_dir)
                print(f"📁 Đã tạo folder mới: {buffer_dir}")
            else:
                print(f"📂 Folder đích: {buffer_dir}")

            # Tạo đường dẫn file Audio đầu ra (.mp3)
            filename_only = os.path.basename(output_path)
            audio_filename = os.path.splitext(filename_only)[0] + ".mp3"
            
            # ĐƯỜNG DẪN CUỐI CÙNG (FINAL PATH)
            audio_output_path = os.path.join(buffer_dir, audio_filename)

            # Debug: In ra để kiểm tra
            print(f"🎯 Target Audio Path: {audio_output_path}")

        except Exception as e:
            return False, f"❌ Lỗi tạo đường dẫn: {str(e)}", None

        # --- BẮT ĐẦU XỬ LÝ VIDEO ---
        try:
            with VideoFileClip(input_path) as video:
                duration = video.duration
                if end_time > duration: end_time = duration
                
                # Cắt đoạn
                new_clip = video.subclip(start_time, end_time)

                # 1. Xuất Video (.mp4)
                # Lưu ý: temp_audiofile=temp_audio_path -> Đẩy file rác vào folder buffer luôn
                print(f"🎥 Đang render Video...")
                new_clip.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    temp_audiofile=temp_audio_path, # <--- QUAN TRỌNG: Giấu file temp vào đây
                    remove_temp=True,
                    fps=24,
                    preset="ultrafast",
                    logger=None
                )

                # 2. Xuất Audio (.mp3)
                print(f"🎵 Đang tách Audio...")
                if new_clip.audio:
                    new_clip.audio.write_audiofile(
                        audio_output_path,
                        codec='mp3',
                        logger=None
                    )
                    
                    # Kiểm tra lại xem file đã nằm đúng chỗ chưa
                    if os.path.exists(audio_output_path):
                        print(f"✅ Audio đã lưu tại: {audio_output_path}")
                    else:
                        print(f"⚠️ LẠ THẬT! Code báo xong nhưng không thấy file ở: {audio_output_path}")
                else:
                    print("⚠️ Video không có tiếng.")
                    audio_output_path = None

            return True, output_path, audio_output_path

        except Exception as e:
            error_msg = f"❌ Lỗi MoviePy: {str(e)}"
            print(error_msg)
            return False, error_msg, None