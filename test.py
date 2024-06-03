import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import cv2
from datetime import datetime
import urllib.request as urll
import json

import urllib.parse  # Thêm dòng này
class TroLyAo:
    def __init__(self, root):
        self.root = root
        self.root.title("VNBotAI")
        self.root.configure(bg='lightblue')  # Đặt màu nền cho cửa sổ chính
        self.label = ttk.Label(root, text="VNBotAI", font=("Arial", 14))
        self.label.pack(pady=20)

        self.btn_listen = ttk.Button(root, text="Nghe và Phản hồi", command=self.nghe_va_phan_hoi)
        self.btn_listen.pack(pady=10)

        self.btn_open_excel = ttk.Button(root, text="Mở Excel", command=self.mo_excel)
        self.btn_open_excel.pack(pady=10)

        self.btn_open_word = ttk.Button(root, text="Mở Word", command=self.mo_word)
        self.btn_open_word.pack(pady=10)

        self.btn_open_youtube = ttk.Button(root, text="Mở youtube", command=self.mo_youtube)
        self.btn_open_youtube.pack(pady=10)
        
        self.btn_capture_photo = ttk.Button(root, text="Chụp ảnh", command=self.chup_anh)
        self.btn_capture_photo.pack(pady=10)

        self.btn_send_email = ttk.Button(root, text="Gửi Email", command=self.mo_email_interface)
        self.btn_send_email.pack(pady=10)

        self.btn_time = ttk.Button(root, text="Xem thời gian", command=self.get_time)
        self.btn_time.pack(pady=10)


        self.btn_quit = ttk.Button(root, text="Thoát", command=root.quit)
        self.btn_quit.pack(pady=10)

        self.entry_recipient = None
        self.entry_subject = None
        self.message_text = None
    def tim_kiem_google(self, query):
        self.noi("Đang tìm kiếm trên Google...")
        query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def nghe_va_phan_hoi(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Trợ lý ảo đang nghe...")
            self.root.update()
            print("Trợ lý ảo đang nghe...")
            audio = r.listen(source)

        try:
            self.label.config(text="Trợ lý ảo đang xử lý...")
            self.root.update()
            print("Trợ lý ảo đang xử lý...")
            text = r.recognize_google(audio, language="vi-VN")
            print("Bạn nói:", text)
            self.label.config(text=f"Bạn nói: {text}")
            self.root.update()
            self.phan_hoi(text.lower())
        except sr.UnknownValueError:
            self.label.config(text="Trợ lý ảo không nghe rõ. Hãy thử lại.")
            self.root.update()
            self.noi("Trợ lý ảo không nghe rõ. Hãy thử lại.")
            print("Trợ lý ảo không nghe rõ. Hãy thử lại.")
        except sr.RequestError:
            self.label.config(text="Không có kết nối internet. Vui lòng kiểm tra kết nối của bạn.")
            self.root.update()
            self.noi("Không có kết nối internet. Vui lòng kiểm tra kết nối của bạn.")
            print("Không có kết nối internet. Vui lòng kiểm tra kết nối của bạn.")

    def nhap_giong_noi_tin_nhan(self):
        message = self.nghe_giong_noi()
        if message:
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, message)

    def nhap_giong_noi_both(self):
        recipient = self.nghe_giong_noi()
        if recipient:
            self.entry_recipient.delete(0, tk.END)
            self.entry_recipient.insert(0, recipient)
            self.entry_subject.focus_set()  # Chuyển đến ô tiêu đề
            subject = self.nghe_giong_noi()
            if subject:
                self.entry_subject.delete(0, tk.END)
                self.entry_subject.insert(0, subject)
                self.message_text.focus_set()  # Chuyển đến ô tin nhắn
                self.nhap_giong_noi_tin_nhan()  # Nghe giọng nói cho tin nhắn

    def nghe_giong_noi(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Trợ lý ảo đang nghe...")
            self.root.update()
            print("Trợ lý ảo đang nghe...")
            audio = r.listen(source)

        try:
            self.label.config(text="Trợ lý ảo đang xử lý...")
            self.root.update()
            print("Trợ lý ảo đang xử lý...")
            text = r.recognize_google(audio, language="vi-VN")
            print("Bạn nói:", text)
            self.label.config(text=f"Bạn nói: {text}")
            self.root.update()
            return text
        except sr.UnknownValueError:
            self.label.config(text="Trợ lý ảo không nghe rõ. Hãy thử lại.")
            self.root.update()
            self.noi("Trợ lý ảo không nghe rõ. Hãy thử lại.")
            print("Trợ lý ảo không nghe rõ. Hãy thử lại.")
            return ""
        except sr.RequestError:
            self.label.config(text="Không có kết nối internet. Vui lòng kiểm tra kết nối của bạn.")
            self.root.update()
            self.noi("Không có kết nối internet. Vui lòng kiểm tra kết nối của bạn.")
            print("Không có kết nối internet")

    def phan_hoi(self, input_text):
        if "mở google" in input_text:
            self.noi("Đang mở Google")
            webbrowser.open("https://www.google.com")
        elif "mở excel" in input_text:
            self.noi("Đang mở Excel")
            self.mo_excel()

        elif "mở word" in input_text:
            self.noi("Đang mở Word")
            self.mo_word()
        elif "chào" in input_text:
            self.noi("Chào bạn, tôi là trợ lý ảo. Tôi giúp gì được cho bạn?")
            self.label.config(text="Chào bạn, tôi là trợ lý ảo. Tôi giúp gì được cho bạn?")
        elif "mở youtube" in input_text:
            self.noi("Đang mở youtube")
            self.mo_youtube()
        elif "thời tiết đà nẵng" in input_text:
            self.thoi_tiet_Da_Nang_hom_nay()  # Gọi hàm xem thông tin thời tiết Đà Nẵng 
        elif "mở email" in input_text:
            self.noi("Đang mở trang email của bạn")
            self.mo_email()
        elif "gửi email" in input_text:
            self.noi("Đang mở giao diện gửi email")
            self.mo_email_interface()
        elif "thời tiết" in input_text:
            self.current_weather()     
        elif "chụp ảnh" in input_text:
            self.noi("Đang chụp ảnh")
            self.chup_anh()   
        elif "xem thời gian" in input_text:
            self.get_time()  # Thêm hành động cho lệnh xem thời gian
        elif "đọc bài thơ" in input_text:
            self.noi("Đang đọc bài thơ")
            self.doc_bai_tho()
        elif "dừng" in input_text:
            self.noi("Hẹn gặp lại sau!")
            self.label.config(text="Hẹn gặp lại sau!")
            self.root.quit()
        elif "tìm " in input_text:
            query = input_text.replace("tìm kiếm trên google về", "").strip()
            self.tim_kiem_google(query)
        else:
            self.noi("Xin lỗi, tôi không hiểu. Bạn có thể nói lại không?")
            self.label.config(text="Xin lỗi, tôi không hiểu. Bạn có thể nói lại không?")
    def speak(self, text):
        tts = gTTS(text=text, lang='vi')
        tts.save("output.mp3")
        os.system("start output.mp3")

    def noi(self, text):
        tts = gTTS(text=text, lang='vi')
        tts.save("phan_hoi.mp3")
        playsound.playsound("phan_hoi.mp3")
        os.remove("phan_hoi.mp3")
    def mo_excel(self):
        os.system("start excel")

    def mo_word(self):
        os.system("start winword")

    def mo_youtube(self):
        webbrowser.open("https://youtube.com")  

    def mo_email(self):
     webbrowser.open("https://mail.google.com")  

    def mo_gmail_compose(self, recipient="", subject="", message=""):
        url = f"https://mail.google.com/mail/?view=cm&fs=1&tf=1&to={recipient}&su={subject}&body={message}"
        webbrowser.open(url)

    def mo_email_interface(self):
        self.email_window = tk.Toplevel(self.root)
        self.email_window.title("Gửi Email")

        ttk.Label(self.email_window, text="Người nhận:").pack(pady=5)
        self.entry_recipient = ttk.Entry(self.email_window, width=50)
        self.entry_recipient.pack(pady=5)

        ttk.Label(self.email_window, text="Tiêu đề:").pack(pady=5)
        self.entry_subject = ttk.Entry(self.email_window, width=50)
        self.entry_subject.pack(pady=5)

        ttk.Label(self.email_window, text="Tin nhắn:").pack(pady=5)
        self.message_text = scrolledtext.ScrolledText(self.email_window, wrap=tk.WORD, width=40, height=10)
        self.message_text.pack(pady=5)

        ttk.Button(self.email_window, text="Nhập bằng giọng nói", command=self.nhap_giong_noi_both).pack(pady=5)
        ttk.Button(self.email_window, text="Gửi", command=self.gui_email).pack(pady=5)

    def gui_email(self):
        recipient = self.entry_recipient.get()
        subject = self.entry_subject.get()
        message = self.message_text.get("1.0", tk.END)  # Lấy toàn bộ nội dung trong ô tin nhắn
        self.mo_gmail_compose(recipient, subject, message)
        self.email_window.destroy()
    def thoi_tiet_Da_Nang_hom_nay(self):
        # Giả sử nhiệt độ là 35 độ C, bạn có thể cập nhật hàm này để lấy dữ liệu thực tế từ API thời tiết
        temperature = 35
        weather_report = f"Thời tiết Đà Nẵng hôm nay nhiệt độ là {temperature} độ C."
        self.noi(weather_report)
        self.label.config(text=weather_report)
        print(weather_report)
    def doc_bai_tho(self):
            poem = (
                "Nghìn năm văn hiến nước Nam ta,\n"
                "Bốn bể trời Nam một nhà,\n"
                "Công cha như núi Thái Sơn,\n"
                "Nghĩa mẹ như nước trong nguồn chảy ra,\n"
                "Một lòng thờ mẹ kính cha,\n"
                "Cho tròn chữ hiếu mới là đạo con."
            )
            self.noi(poem)
            self.label.config(text="Đang đọc bài thơ:\n" + poem)
    def chup_anh(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("captured_photo.jpg", frame)
            self.noi("Đã chụp ảnh thành công!")
        else:
            self.noi("Không thể chụp ảnh. Vui lòng thử lại sau.")
        cap.release()

    def get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.noi(f"Bây giờ là {current_time}")
        current_date = now.strftime("%d/%m/%Y")
        self.noi(f"Hôm nay là ngày {current_date}")




def main():
    root = tk.Tk()
    app = TroLyAo(root)
    root.mainloop()

if __name__ == "__main__":
    main()

