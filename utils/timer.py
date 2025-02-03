import time
import threading
from voice.speech_handler import VoiceEngine

class Timer:
    def __init__(self):
        self.voice = VoiceEngine()
        self.active_timers = {}
        self.timer_id = 0
        self.lock = threading.Lock()

    def start_timer(self, minutes):
        """Start a countdown timer with voice alerts"""
        try:
            if not isinstance(minutes, int) or minutes <= 0:
                raise ValueError("Invalid duration")
            
            timer_id = self._get_timer_id()
            
            def _countdown():
                total_seconds = minutes * 60
                start_msg = f"Timer started for {minutes} minute{'s' if minutes > 1 else ''}"
                self.voice.speak(start_msg)
                
                while total_seconds > 0:
                    time.sleep(1)
                    total_seconds -= 1
                    
                    # Voice updates at intervals
                    if total_seconds in [1800, 900, 300, 60, 30, 10]:  # 30m, 15m, 5m, 1m, 30s, 10s
                        mins, secs = divmod(total_seconds, 60)
                        if mins > 0:
                            update = f"{mins} minute{'s' if mins > 1 else ''} remaining"
                        else:
                            update = f"{secs} seconds remaining"
                        self.voice.speak(update)
                
                self.voice.speak("Timer complete!")
                self._remove_timer(timer_id)

            thread = threading.Thread(target=_countdown)
            self._add_timer(timer_id, thread)
            thread.start()
            return True
            
        except Exception as e:
            return False

    def _get_timer_id(self):
        with self.lock:
            self.timer_id += 1
            return self.timer_id

    def _add_timer(self, timer_id, thread):
        with self.lock:
            self.active_timers[timer_id] = thread

    def _remove_timer(self, timer_id):
        with self.lock:
            if timer_id in self.active_timers:
                del self.active_timers[timer_id]

    def cancel_timers(self):
        """Cancel all active timers"""
        with self.lock:
            for timer_id, thread in self.active_timers.items():
                if thread.is_alive():
                    thread.join(0.1)
            self.active_timers.clear()