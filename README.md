# BTech Logger

A lightweight, dependency-free Python logging utility with configurable
logging levels, automatic log files, stack traces, and exception handling.

BTech Logger uses only Python's standard library.

## Features

- Zero third-party dependencies
- Five logging levels: fatal, error, warn, log, and verbose
- Configurable logging verbosity
- Timestamped log messages
- Automatic log directory creation
- Date-based log filenames
- Optional console output
- Optional call-stack logging
- Exception traceback support
- Built-in exception raising
- Shorthand logging methods

## Installation

Install using pip:

```bash
pip install btech-logger
```

## Quick Start

```python
from btech_logger import Logger

logger = Logger()

logger.log("Application started")
logger.warn("This is a warning")
logger.error("An error occurred")
logger.fatal("A fatal condition occurred")
```

By default, Logger writes messages to a log file.

## Configuration

```python
logger = Logger(
    log_level="log",
    date_format="%d/%m/%Y - %H:%M:%S",
    do_print=True,
    show_stack_trace=False
)
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `log_level` | `"log"` | Minimum logging severity |
| `date_format` | `"%d/%m/%Y - %H:%M:%S"` | Timestamp format |
| `do_print` | `False` | Print logged messages to the console |
| `show_stack_trace` | `False` | Include call stacks in log messages |

## Logging Levels

Logger supports five levels, ordered from highest to lowest severity:

| Level | Method | Shorthand |
|-------|--------|-----------|
| Fatal | `fatal()` | `f()` |
| Error | `error()` | `e()` |
| Warning | `warn()` | `w()` |
| Log | `log()` | `l()` |
| Verbose | `verbose()` | `v()` |

The configured logging level determines which messages are recorded.

For example:

```python
logger = Logger(log_level="warn")
```

This records only:

- Fatal messages
- Error messages
- Warning messages

Log and verbose messages are ignored.

## Exception Handling

Logger can log a message and raise an exception.

```python
logger.error(
    "Invalid configuration",
    ValueError
)
```

This writes the error message and raises:

```python
ValueError("Invalid configuration")
```

The exception class must inherit from `BaseException`.

### Logging Existing Exceptions

```python
try:
    result = 10 / 0
except ZeroDivisionError as exc:
    logger.error(
        "Division failed",
        exc=exc
    )
```

This records the exception traceback alongside the error message.

## Stack Traces

Stack traces can be enabled for individual messages:

```python
logger.error(
    "Something unexpected happened",
    show_stack=True
)
```

Or globally:

```python
logger = Logger(show_stack_trace=True)
```

Stack traces help identify where logging calls originated.

## Log Files

Logger automatically creates a `logs` directory.

Log filenames use the date on which the Logger instance was created.

Example:

```text
logs/
└── 2026-10-20-log.txt
```

Example log contents:

```text
20/10/2026 - 14:32:01 | [LOG] Application started
20/10/2026 - 14:32:05 | [WARN] This is a warning
20/10/2026 - 14:32:07 | [ERROR] An error occurred
```

Note: The current implementation does not automatically switch
log files at midnight.

## Dependencies

BTech Logger has no third-party runtime dependencies.

It uses only:

- `os`
- `traceback`
- `datetime`

All three are included in Python's standard library.

## License

Distributed under the MIT License.

See [LICENSE](LICENSE) for details.
