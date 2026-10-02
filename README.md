# Website Status Monitor

A small Python command-line project for checking website availability and response time.

This first version reads URLs from a text file, checks them one by one, and prints a clear status summary.

## Features

- Read multiple URLs from a text file
- Check HTTP/HTTPS availability
- Measure response time
- Show HTTP status code
- Detect connection and timeout errors
- Clean command-line output
- Uses only the Python standard library
- Includes unit tests

## Project Structure

```text
website-status-monitor/
├── src/
│   └── website_status_monitor/
│       ├── __init__.py
│       ├── checker.py
│       └── cli.py
├── tests/
│   └── test_checker.py
├── samples/
│   └── urls.txt
├── .gitignore
├── pyproject.toml
└── README.md
```

## Run

From the project folder:

```bash
python -m website_status_monitor.cli samples/urls.txt
```

Example output:

```text
[UP]   https://example.com       200   184 ms
[DOWN] https://example.invalid     -   connection error
```

## Planned Improvements

This repository will be developed in small Git commits. Planned features include:

- Concurrent URL checks
- JSON reports
- Retry support
- Summary statistics
- Configurable timeout

## Author

Farid Farahani

Python Developer | Web Developer

Website: https://faridfarahani.ir
