import logging
import os
import traceback
import threading
from datetime import datetime


def force_create_file(file):
    """Ensures that the given file exists by creating missing directories and an empty file."""
    os.makedirs(os.path.dirname(file), exist_ok=True)
    open(file, "a").close()


def force_create_dir(direct):
    """Ensures that the given directory exists."""
    os.makedirs(direct, exist_ok=True)


class Logger:
    """
    Logs INFO messages to the console.
    On ERROR:
        - Logs the full traceback. (may become a bottleneck)
        - Includes all INFO logs from the same call stack.

    Workflow:
        - cls._thread_logs : per-thread storage (for INFO logs). During execution logs are being kept in it.
            - If error: they are extracted to include to error.log file. The method  .clear_logs is called automatically
            - If okay: they are being deleted. You MUST call .clear_logs manually to release the logs
    """

    _thread_logs = threading.local()

    def __init__(self, module_name: str):
        self.error_log_file = f"logs/error_logs_{module_name}/.error.log"
        force_create_file(self.error_log_file)
        self.stack_trace_dir = f"logs/stack_traces_{module_name}/"
        force_create_dir(self.stack_trace_dir)

        # console logger (INFO+)
        self.console_logger = logging.getLogger(module_name)
        if not self.console_logger.hasHandlers():
            self.console_logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.console_logger.addHandler(console_handler)

        # file logger (ERROR+)
        self.error_logger = logging.getLogger(f"{module_name}_error")
        if not self.error_logger.hasHandlers():
            self.error_logger.setLevel(logging.ERROR)
            file_handler = logging.FileHandler(self.error_log_file)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s\n%(message)s\n"))
            self.error_logger.addHandler(file_handler)

    def info(self, message: str):
        """
        Logs info messages to console, also keeps them for error logs.
        """
        self.console_logger.info(message)

        # store INFO log in thread-local storage
        if not hasattr(self._thread_logs, "logs"):
            self._thread_logs.logs = []
        self._thread_logs.logs.append(message)

    def error(self, message: str):
        """Logs an error message and saves full traceback in a separate file."""

        error_title = message.split("\n")[0]
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_traceback = traceback.format_exc()

        # If there's no real traceback, remove it to avoid extra lines
        if not error_traceback.strip() or "NoneType: None" in error_traceback:
            error_traceback = "No traceback available"

        # name of stack trace file
        error_summary = error_title.split(":")[0].strip().replace(" ", "_")[:50]
        stack_trace_filename = f"{error_time.replace(':', '-')}_{error_summary}.log"
        stack_trace_path = os.path.join(self.stack_trace_dir, stack_trace_filename)

        # writing stack trace to stack trace file
        def write_trace():
            with open(stack_trace_path, "w", encoding="utf-8") as f:
                f.write(error_traceback)

        try:
            write_trace()
        except FileNotFoundError:
            os.makedirs(os.path.dirname(stack_trace_path), exist_ok=True)
            write_trace()

        # writing to error.log file
        error_content = f"{error_time} : {error_title} - See {stack_trace_path} file."
        with open(self.error_log_file, "a", encoding="utf-8") as file:
            file.write(error_content + "\n")

        self.clear_logs()

    def clear_logs(self):
        """
        Flushed stored INFO logs for the current thread.
        """
        if hasattr(self._thread_logs, "logs"):
            del self._thread_logs.logs
