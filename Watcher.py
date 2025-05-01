import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Extractor import process_file

WATCH_FOLDER = "..\code Library"  

IGNORE_FILES = [".env", "config.py", "settings.py"]
EVENT_COOLDOWN_SECONDS = 1  

last_event_time = {}

class WatcherHandler(FileSystemEventHandler):
    def should_process(self, path):
        now = time.time()
        last_time = last_event_time.get(path, 0)
        if now - last_time > EVENT_COOLDOWN_SECONDS:
            last_event_time[path] = now
            return True
        return False

    def on_any_event(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith('.py'):
            return
        if any(ignored in event.src_path for ignored in IGNORE_FILES):
            return
        if event.event_type in ["created", "modified"]:
            if self.should_process(event.src_path):
                print(f"{event.event_type.capitalize()}: {event.src_path}")
                process_file(event.src_path)

def start_watching():
    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()
    print(f"Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watching()
