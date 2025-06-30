from flask import Flask, render_template
from flask_socketio import SocketIO
import speech_recognition as sr
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')  # 使用 threading 模式

@app.route("/")
def index():
    return render_template("index.html")

# 語音辨識並透過 SocketIO 廣播
def recognize_and_emit():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # 可調整參數以延長錄音時間與降低過早切斷
    recognizer.pause_threshold = 1           # 停頓超過 1 秒才認定為結束
    recognizer.non_speaking_duration = 0.5     # 非語音持續 0.5 秒則停止錄音
    # recognizer.energy_threshold = 300        # 若需要可手動設定、或保持自動

    with mic as source:
        print("正在調整麥克風噪音...請稍候")
        recognizer.adjust_for_ambient_noise(source)
        print("開始語音辨識。請說話...")

        while True:
            try:
                print("開始錄音，等待語音停止後將送出辨識...")
                audio = recognizer.listen(source)  # 依據停頓自動判斷結束，不設定短時間上限

                print("辨識中...")
                text = recognizer.recognize_google(audio, language='zh-TW')
                print("你說的是:", text)
                socketio.emit('speech', {'text': text})

            except sr.WaitTimeoutError:
                print("等待語音逾時，未偵測到任何聲音。")
            except sr.UnknownValueError:
                print("無法辨識語音，請再試一次。")
            except sr.RequestError as e:
                print("連線至語音辨識服務失敗：", e)
            except KeyboardInterrupt:
                print("語音辨識已停止")
                break

if __name__ == '__main__':
    threading.Thread(target=recognize_and_emit, daemon=True).start()
    socketio.run(app, host='127.0.0.1', port=5000)
