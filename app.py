import speech_recognition as sr
import threading

def recognize_from_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("正在調整麥克風噪音...請稍候")
        recognizer.adjust_for_ambient_noise(source)
        print("開始語音辨識。請說話...")

        while True:
            try:
                print("\n正在傾聽...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("辨識中...")
                text = recognizer.recognize_google(audio, language='zh-TW')
                print("你說的是:", text)
            except sr.WaitTimeoutError:
                pass
                print("等待語音逾時，未偵測到說話。")
            except sr.UnknownValueError:
                print("無法辨識語音，請再試一次。")
            except sr.RequestError as e:
                print("無法連線至語音辨識服務：", e)
            except KeyboardInterrupt:
                print("\n已停止語音辨識。")
                break

if __name__ == "__main__":
    recognize_from_microphone()
