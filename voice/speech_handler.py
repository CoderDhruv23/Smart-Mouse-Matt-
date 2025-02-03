import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.microphone = sr.Microphone()

    def listen(self, timeout=5):
        """Listen for speech with configurable timeout"""
        try:
            with self.microphone as source:
                print("\n[DEBUG] Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio).lower()
            print(f"[DEBUG] Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("[DEBUG] Listening timeout")
            return ""
        except sr.UnknownValueError:
            print("[DEBUG] Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"[ERROR] API unavailable: {e}")
            return ""
        except Exception as e:
            print(f"[CRITICAL] Audio error: {e}")
            return ""

    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"[DEBUG] Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[ERROR] Speech synthesis failed: {e}")