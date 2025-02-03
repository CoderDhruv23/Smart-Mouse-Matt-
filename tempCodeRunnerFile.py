from voice.speech_handler import VoiceEngine
from ai.gemini_handler import GeminiAI
from utils.config import WAKE_WORD
from utils.real_time import get_real_time
from utils.timer import Timer  # NEW: Timer functionality
from utils.todo import ToDoList  # NEW: To-Do list functionality

class Assistant:
    def __init__(self):
        self.voice = VoiceEngine()
        self.ai = GeminiAI()
        self.timer = Timer()  # NEW: Initialize timer
        self.todo = ToDoList()  # NEW: Initialize to-do list
    
    def run(self):
        active_session = False
        
        while True:
            user_input = self.voice.listen().strip().lower()  # Convert to lowercase
            
            if not active_session:
                if WAKE_WORD in user_input:
                    active_session = True
                    self.voice.speak("Hello boss!, How can I help you?")
                continue
            
            else:
                if "exit" in user_input:
                    self.voice.speak("Goodbye!")
                    active_session = False
                    continue
                
                # NEW: Timer functionality
                if "set a timer" in user_input or "timer" in user_input:
                    self.voice.speak("For how many minutes?")
                    duration = self.voice.listen().strip()
                    self.timer.start_timer(duration)
                
                # NEW: To-Do list functionality
                elif "add to my to-do list" in user_input:
                    self.voice.speak("What task should I add?")
                    task = self.voice.listen().strip()
                    response = self.todo.add_task(task)
                    self.voice.speak(response)
                
                elif "view my to-do list" in user_input:
                    response = self.todo.view_tasks()
                    self.voice.speak(response)
                
                elif "clear my to-do list" in user_input:
                    response = self.todo.clear_tasks()
                    self.voice.speak(response)
                
                # Existing functionality: Time/date queries
                real_time_response = get_real_time(user_input)
                if real_time_response:
                    self.voice.speak(real_time_response)
                
                # Existing functionality: Default to Gemini
                else:
                    response = self.ai.generate_response(user_input)
                    self.voice.speak(response)

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()