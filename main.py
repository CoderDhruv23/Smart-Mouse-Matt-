from voice.speech_handler import VoiceEngine
from ai.gemini_handler import GeminiAI
from utils.config import WAKE_WORD, SERIAL_PORT
from utils.real_time import get_real_time
from utils.timer import Timer
from utils.todo import ToDoList
from utils.serial_handler import SerialManager
import time
from datetime import datetime

class Assistant:
    def __init__(self):
        print("[System] Initializing assistant...")
        self.voice = VoiceEngine()
        print("[System] Voice engine initialized")
        self.ai = GeminiAI()
        self.timer = Timer()  # Updated timer with cancellation
        self.todo = ToDoList()
        
        
        # Serial connection
        try:
            self.serial = SerialManager(port=SERIAL_PORT)
            print(f"[Hardware] Connected to {SERIAL_PORT}")
        except Exception as e:
            print(f"[Error] Serial connection failed: {str(e)}")
            self.serial = None
        
        self.active_session = False
        print("[System] Assistant ready")

    def _get_greeting(self):
        """Return time-appropriate greeting"""
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "Good morning! How can I help you?"
        elif 12 <= current_hour < 17:
            return "Good afternoon! How can I help you?"
        else:
            return "Good evening! How can I help you?"

    def run(self):
        print("[System] Entering main loop...")
        while True:
            try:
                time.sleep(0.1)
                
                # Session activation
                if not self.active_session:
                    print("[Status] Waiting for activation...")
                    
                    # Voice activation
                    input_text = self.voice.listen(timeout=2).strip().lower()
                    # Updated code for multiple wake words
                    if any(wake_word in input_text for wake_word in WAKE_WORD):
                        print("[Activation] Voice trigger")
                        self.active_session = True
                        self.voice.speak(self._get_greeting())
                        continue
                    
                    # Hardware activation
                    if self.serial and self.serial.active_session:
                        print("[Activation] Touch sensor trigger")
                        self.active_session = True
                        self.serial.active_session = False
                        self.voice.speak(self._get_greeting())
                        continue
                    
                    continue

                # Active session handling
                print("[Status] Session active - listening...")
                user_input = self.voice.listen().strip().lower()
                
                if not user_input:
                    continue
                
                print(f"[Input] User said: {user_input}")

                # Exit command
                if "exit" in user_input or "goodbye" in user_input:
                    self.voice.speak("Goodbye! Have a great day!")
                    self.timer.cancel_timers()  # Stop all timers on exit
                    self.active_session = False
                    print("[Status] Session ended")
                    continue

                # Sensor data
                if "temperature" in user_input or "humidity" in user_input:
                    temp = self.serial.temperature if self.serial else None
                    hum = self.serial.humidity if self.serial else None
                    
                    response = []
                    if "temperature" in user_input:
                        response.append(f"{temp}°C" if temp else "Temperature data unavailable")
                    if "humidity" in user_input:
                        response.append(f"{hum}% humidity" if hum else "Humidity data unavailable")
                    
                    self.voice.speak(" ".join(response))
                    continue

                # Timer functionality (updated)
                if "timer" in user_input:
                    if "cancel" in user_input:
                        self.timer.cancel_timers()
                        self.voice.speak("All active timers cancelled")
                    else:
                        self.voice.speak("For how many minutes?")
                        duration = self.voice.listen(timeout=5).strip()
                        if duration.isdigit():
                            if self.timer.start_timer(int(duration)):
                                self.voice.speak(f"Timer started for {duration} minutes")
                            else:
                                self.voice.speak("Invalid timer duration")
                        else:
                            self.voice.speak("Please say a number")
                    continue

                # To-Do list
                if "to-do list" in user_input or "todo" in user_input:
                    if "add" in user_input:
                        self.voice.speak("What task should I add?")
                        task = self.voice.listen(timeout=5).strip()
                        if task:
                            response = self.todo.add_task(task)
                        else:
                            response = "I didn't hear a task to add"
                        self.voice.speak(response)
                    
                    elif "view" in user_input:
                        tasks = self.todo.view_tasks()
                        self.voice.speak(tasks if tasks else "Your to-do list is empty")
                    
                    elif "complete" in user_input:
                        self.voice.speak("Which task number?")
                        try:
                            task_id = int(self.voice.listen(timeout=5).strip())
                            response = self.todo.complete_task(task_id)
                        except:
                            response = "Invalid task number"
                        self.voice.speak(response)
                    
                    elif "delete" in user_input:
                        self.voice.speak("Which task number?")
                        try:
                            task_id = int(self.voice.listen(timeout=5).strip())
                            response = self.todo.delete_task(task_id)
                        except:
                            response = "Invalid task number"
                        self.voice.speak(response)
                    
                    elif "clear" in user_input:
                        self.voice.speak("Confirm clear all? Say 'yes'")
                        confirmation = self.voice.listen(timeout=3).strip().lower()
                        if "yes" in confirmation:
                            response = self.todo.clear_tasks()
                        else:
                            response = "Operation cancelled"
                        self.voice.speak(response)
                    
                    continue

                # Time/date
                time_response = get_real_time(user_input)
                if time_response:
                    self.voice.speak(time_response)
                    continue

                # Default AI response
                response = self.ai.generate_response(user_input)
                self.voice.speak(response)

            except KeyboardInterrupt:
                print("\n[System] Shutting down...")
                self.timer.cancel_timers()
                if self.serial:
                    self.serial.running = False
                break
            except Exception as e:
                print(f"[Critical Error] {str(e)}")
                self.voice.speak("Let me try that again")
                self.active_session = False

if __name__ == "__main__":
    try:
        print("[System] Starting AI assistant...")
        assistant = Assistant()
        assistant.run()
    except Exception as e:
        print(f"[Fatal Error] {str(e)}")