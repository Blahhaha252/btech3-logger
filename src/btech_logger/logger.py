import os
import traceback
from datetime import datetime

class Logger:
    def __init__(self, log_level=None, date_format=None, do_print=False, show_stack_trace=False):
        self.levels = ["fatal", "error", "warn", "log", "verbose"]
        self.date = datetime.now().date()
        self.home_path = os.getcwd()
        self.log_dir = os.path.join(self.home_path, "./logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.show_stack = show_stack_trace
        self.logging_level = "log"
        self.date_format = "%d/%m/%Y - %H:%M:%S"
        self.do_print = do_print

        if log_level:
            lvl = log_level.lower()
            if lvl in self.levels:
                self.logging_level = lvl
            else:
                self.__log(
                    f"[INTERNAL] passed in logging level not found in {self.levels}. Defaulting to 'log'.",
                    "error",
                    special_print=True,
                )

        if date_format:
            self.date_format = date_format

          # date object is fine

    # shorthand
    def v(self, message, exc_type=None, *, show_stack=False):
        return self.verbose(message, exc_type, show_stack=show_stack)

    def l(self, message, exc_type=None, *, show_stack=False):
        return self.log(message, exc_type, show_stack=show_stack)

    def w(self, message, exc_type=None, *, show_stack=False):
        return self.warn(message, exc_type, show_stack=show_stack)

    def e(self, message, exc_type=None, *, show_stack=False):
        return self.error(message, exc_type, show_stack=show_stack)

    def f(self, message, exc_type=None, *, show_stack=True):
        return self.fatal(message, exc_type, show_stack=show_stack)

    def verbose(self, message, exc_type=None, *, show_stack=False):
        if show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "verbose")
        if self.show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "verbose")
        if exc_type is None:
            self.__log(message, "verbose")
            return
        self.__raise_with_log(message, exc_type, level="verbose")

    def log(self, message, exc_type=None, *, show_stack=False):
        if show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "log")
        if self.show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "log")
        if exc_type is None:
            self.__log(message, "log")
            return
        self.__raise_with_log(message, exc_type, level="log")

    def warn(self, message, exc_type=None, *, show_stack=False):
        if show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "warn")
        if self.show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "warn")
        if exc_type is None:
            self.__log(message, "warn")
            return
        self.__raise_with_log(message, exc_type, level="warn")

    def error(self, message, exc_type=None, *, show_stack=False, exc=None):
        if show_stack or self.show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "error")

        if exc is not None:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            self.__log(tb, "error")

        if exc_type is None:
            self.__log(message, "error")
            return

        self.__raise_with_log(message, exc_type, level="error")

    def fatal(self, message, exc_type=None, *, show_stack=True, exc=None):
        # Call-site stack (who called fatal)
        if show_stack or self.show_stack:
            self.__log("".join(traceback.format_stack()[:-1]), "fatal")

        # Exception traceback (only if provided, or if we're currently in an except)
        if exc is not None:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            self.__log(tb, "fatal")
        else:
            active = traceback.format_exc()
            if active.strip() != "NoneType: None":
                self.__log(active, "fatal")

        # Log the message itself
        self.__log(message, "fatal")

        # Raise if requested
        if exc_type is None:
            return
        self.__raise_with_log(message, exc_type, level="fatal")

    def __raise_with_log(self, message, exc_type, *, level):
        if not isinstance(exc_type, type) or not issubclass(exc_type, BaseException):
            self.__log(
                f"[INTERNAL] exc_type must be an exception class (e.g., ValueError). Got: {exc_type!r}",
                "fatal",
                special_print=True,
            )
            raise TypeError("exc_type must be an exception class")
        self.__log(message, level)
        raise exc_type(message)

    def __log(self, message, level, special_print=False):
        index = self.levels.index(level)
        log_index = self.levels.index(self.logging_level)

        # Your current comparison means: only log messages that are <= configured level
        # With levels ordered ["fatal","error","warn","log","verbose"], this acts like:
        # logging_level="log" logs fatal/error/warn/log but not verbose. (reasonable)
        if index <= log_index:
            filename = os.path.join(self.log_dir, f"{self.date}-log.txt")
            ts = datetime.now().strftime(self.date_format)

            with open(filename, "a", encoding="utf-8") as f:
                for line in str(message).splitlines():
                    msg = f"{ts} | [{level.upper()}] {line}"
                    f.write(msg + "\n")

                    if self.do_print or special_print:
                        print(msg)
