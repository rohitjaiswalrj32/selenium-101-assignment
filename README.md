# Selenium 101 Assignment - TestMu AI

This repository contains the Selenium 101 coding assignment solution built with Python, Pytest, Selenium 4, and the TestMu AI Selenium Grid.

The suite runs in parallel across two browser and OS combinations and enables the required observability artifacts:

- Network logs
- Video recording
- Screenshots (`visual`)
- Console logs

## Scenarios Covered

1. Simple Form Demo
2. Drag and Drop Sliders
3. Input Form Submit

## Default Browser Matrix

- `Chrome` on `Windows 10`
- `Safari` on `macOS Catalina`

You can override the browser matrix with the `LT_BROWSER_MATRIX` environment variable.

## Project Structure

```text
.
|-- README.md
|-- pytest.ini
|-- requirements.txt
`-- tests
    |-- conftest.py
    `-- test_selenium_playground.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set TestMu AI credentials in PowerShell:

```powershell
$env:LT_USERNAME="your_testmu_username"
$env:LT_ACCESS_KEY="your_testmu_access_key"
```

Optional metadata:

```powershell
$env:LT_PROJECT="Selenium 101 Assignment"
$env:LT_BUILD="Selenium Playground Parallel Suite"
```

## Run The Suite

```bash
pytest -n 2
```

This executes all scenarios in parallel against the configured browser matrix.

## Optional Browser Matrix Override

```powershell
$env:LT_BROWSER_MATRIX='[
  {"browserName":"Chrome","browserVersion":"latest","platformName":"Windows 10"},
  {"browserName":"Safari","browserVersion":"latest","platformName":"macOS Catalina"}
]'
```

## Session IDs

Each test prints its TestMu AI session ID in the console output, for example:

```text
TestMu AI session for 'Scenario 1 - Simple Form Demo | Chrome on Windows 10': <session_id>
```

Use those session IDs when submitting the assignment.

## Local Screenshots

In addition to the TestMu AI cloud artifacts, the suite also saves local screenshots after each test run under:

```text
test-results/screenshots/
```

This makes it easier to include screenshot files directly in the repository when needed.

## Submission Notes

- Push the project to your GitHub repository.
- Share the repository privately with `admin@testmuaicertifications.com`.
- Submit the GitHub repository URL and the TestMu AI session IDs on the exam portal.
