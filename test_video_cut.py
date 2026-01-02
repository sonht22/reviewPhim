from moviepy.editor import VideoFileClip
import os

def cut_video_hello_world(input_path, output_path):
    print(f"🎬 Đang mở video: {input_path}")
    
    try:
        # 1. Load Video
        # Dùng with để đảm bảo file được đóng lại sau khi dùng xong
        with VideoFileClip(input_path) as video:
            
            # 2. Kiểm tra độ dài
            duration = video.duration
            print(f"⏱️ Độ dài gốc: {duration} giây")
            
            # Nếu video ngắn hơn 5s thì cắt hết, ngược lại cắt 5s đầu
            end_time = 5 if duration > 5 else duration
            
            # 3. Cắt (Subclip)
            # subclip(t_start, t_end) -> Cắt từ giây 0 đến giây 5
            clip = video.subclip(0, end_time)
            
            # 4. Xuất file (Render)
            print("⚙️ Đang render... (Vui lòng đợi)")
            clip.write_videofile(
                output_path, 
                codec="libx264",      # Chuẩn nén hình ảnh phổ biến nhất
                audio_codec="aac",    # Chuẩn nén âm thanh (quan trọng để có tiếng)
                temp_audiofile='temp-audio.m4a', 
                remove_temp=True,
                fps=24                # Set cứng FPS cho nhẹ, hoặc bỏ đi để giữ nguyên
            )
            
        print(f"✅ Xong! File đã lưu tại: {output_path}")

    except Exception as e:
        print(f"❌ Lỗi xử lý video: {str(e)}")

# --- CHẠY THỬ ---
if __name__ == "__main__":
    # Bạn đổi tên file bên dưới thành tên video có thật trong máy bạn nhé
    INPUT_FILE = "1214 (1).mp4"  
    OUTPUT_FILE = "test_hello_world.mp4"

    if os.path.exists(INPUT_FILE):
        cut_video_hello_world(INPUT_FILE, OUTPUT_FILE)
    else:
        print(f"❌ Không tìm thấy file video đầu vào: {INPUT_FILE}")
        print("👉 Hãy copy 1 video vào thư mục dự án và đổi tên biến INPUT_FILE trong code.")