# Selenium 101 Assignment - TestMu AI

This project covers all three assignment scenarios from the provided PDF using:

- Python
- Pytest
- Selenium 4
- TestMu AI Selenium Grid

The suite is designed to run in parallel on at least two browser and OS combinations, with TestMu AI capabilities enabled for:

- Network logs
- Video recording
- Screenshots (`visual`)
- Console logs

## Covered Scenarios

1. Simple Form Demo
2. Drag and Drop Sliders
3. Input Form Submit

## Browser Matrix

By default, the suite runs on:

- `Chrome` on `Windows 10`
- `Safari` on `macOS Catalina`

You can override this matrix with the `LT_BROWSER_MATRIX` environment variable.

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

3. Set TestMu AI credentials.

Windows PowerShell:

```powershell
$env:LT_USERNAME="your_testmu_username"
$env:LT_ACCESS_KEY="your_testmu_access_key"
```

Optional metadata:

```powershell
$env:LT_PROJECT="Selenium 101 Assignment"
$env:LT_BUILD="Selenium Playground Parallel Suite"
```

## Run The Suite In Parallel

```bash
pytest -n 2
```

This will execute all tests in parallel across the configured browser matrix.

## Optional Browser Matrix Override

Example:

```powershell
$env:LT_BROWSER_MATRIX='[
  {"browserName":"Chrome","browserVersion":"latest","platformName":"Windows 10"},
  {"browserName":"Safari","browserVersion":"latest","platformName":"macOS Catalina"}
]'
```

## Session IDs

Each test prints its TestMu AI session ID to the console in this format:

```text
TestMu AI session for 'Scenario 1 - Simple Form Demo | Chrome on Windows 10': <session_id>
```

Use these session IDs when submitting the assignment on the exam portal.

## Notes For Submission

- Push this project to your GitHub repository.
- Share the repository privately with `admin@testmuaicertifications.com`.
- Run the suite on your TestMu AI account and collect the generated session IDs.
- Submit both the GitHub repository URL and the TestMu AI session IDs on the exam portal.
