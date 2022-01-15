# rpa_logger

A simple python package for logging robotic process automation (RPA) progress.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle rpa_logger
autopep8 -aaar --in-place rpa_logger
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance rpa_logger
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source rpa_logger/ -m unittest discover -s tst/
coverage report -m
```
