# Usage

The `rpa_logger` package is used to log tasks done by RPA or similar script. This is to communicate to the user what tasks are in progress and what tasks have been completed.

## Getting started

The logging is done via `rpa_logger.logger.Logger` class. It provides `rpa_logger.logger.Logger.start_task` and `rpa_logger.logger.Logger.finish_task` methods for starting and finishing tasks, respectively. An simple hello world case could be `examples/hello_world.py`:

```python
.. include:: ../examples/hello_world.py
```

When finishing the task, task must be assigned an status. The status can be any string. The status is used to determine the status indicator for the task, for example `✓` or `✗`. This is done, by default, by the `rpa_logger.defaults.get_indicator` function.

For short tasks, `rpa_logger.logger.Logger.start_task` can be omitted. In this case task description should be given as parameter to the `rpa_logger.logger.Logger.finish_task` method. Alternatively, `rpa_logger.logger.Logger.log_task`, an alias for finish_task, can be used in this case.

If task was started with `rpa_logger.logger.Logger.start_task`, it must be stopped with `rpa_logger.logger.Logger.finish_task` to stop printing the progress spinner.

The tasks are indentified with keys. Keys are either provided as parameter when starting the task or, if the `key` parameter is omitted, new `uuid` is automatically generated. In both cases, the key used to identify the started task is returned by the `rpa_logger.logger.Logger.start_task` method. A key can be anything that can be used as a dict `key`.

After all tasks to be logged have finished, `rpa_logger.logger.Logger.finish_suite` can be used to finish the `rpa_logger.task.TaskSuite` instance automatically created by the `rpa_logger.logger.Logger`. This sets the `rpa_logger.task.TaskSuite.finished` and `rpa_logger.task.TaskSuite.status` variables.

## Title and summary

In addition to logging tasks, the `rpa_logger.logger.Logger` provides `rpa_logger.logger.Logger.title` and `rpa_logger.logger.Logger.summary` methods for printing title and summary for the RPA process, respectively. Example usage of these methods is provided in `examples/title_and_summary.py`:

```python
.. include:: ../examples/title_and_summary.py
```
