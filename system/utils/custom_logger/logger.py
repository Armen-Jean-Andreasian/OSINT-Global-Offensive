import os
import threading
import traceback
from datetime import datetime


def force_create_dir(path: str):
    """Ensures that a directory exists."""
    os.makedirs(path, exist_ok=True)


class BaseLogger:
    def __init__(self, module_name: str, log_output_dir: str = "./logs"):

        self._log_dir = os.path.join(log_output_dir, f"{module_name}_logs")

        self._error_log_file = os.path.join(self._log_dir, f"{module_name}.error.log")
        self._info_log_file = os.path.join(self._log_dir, f"{module_name}.info.log")
        self._stack_trace_dir = os.path.join(self._log_dir, f"{module_name}_error_traces")

        force_create_dir(self._stack_trace_dir)

        self._thread_logs = threading.local()
        self._thread_logs.logs = []

    def log(self, message: str):
        """Stores log messages in a thread-local storage."""
        if not hasattr(self._thread_logs, "logs"):
            self._thread_logs.logs = []
        self._thread_logs.logs.append(message)

    def clear_logs(self):
        """Clears thread-local log storage."""
        if hasattr(self._thread_logs, "logs"):
            self._thread_logs.logs.clear()


class InfoLogger(BaseLogger):
    def __init__(self, module_name: str, log_output_dir: str = "./logs"):
        super().__init__(module_name, log_output_dir)

    def info(self, message: str):
        """Logs an info message."""
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{log_time} : {message}"

        with open(self._info_log_file, "a", encoding="utf-8") as file:
            file.write(log_entry + "\n")

        self.log(log_entry)


class ErrorLogger(BaseLogger):
    def __init__(self, module_name: str, log_output_dir: str = "./logs"):
        super().__init__(module_name, log_output_dir)

    def error(self, message: str):
        """Logs an error message and saves full traceback in a separate file."""
        error_title = message.split("\n")[0]
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_traceback = traceback.format_exc(limit=5)

        if not error_traceback.strip() or "NoneType: None" in error_traceback:
            error_traceback = "No traceback available"

        error_summary = error_title.split(":")[0].strip().replace(" ", "_")[:50]
        stack_trace_filename = f"{error_time.replace(':', '-')}_{error_summary}.log"
        stack_trace_path = os.path.join(self._stack_trace_dir, stack_trace_filename)

        force_create_dir(os.path.dirname(stack_trace_path))

        with open(stack_trace_path, "w", encoding="utf-8") as f:
            f.write(error_traceback)

        error_content = f"{error_time} : {error_title} - See {stack_trace_path} file."

        with open(self._error_log_file, "a", encoding="utf-8") as file:
            file.write(error_content + "\n")

        self.clear_logs()


class Logger(InfoLogger, ErrorLogger): ...
