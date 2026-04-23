# Selenium 101 Assignment - TestMu AI

This repository is my Selenium 101 coding assignment submission. The solution is implemented with Python, Pytest, Selenium 4, and the TestMu AI Selenium Grid.

The suite is designed to run in parallel across two browser and OS combinations and enables the required observability artifacts:

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

These are the two browser and OS combinations used for the assignment execution.

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

## Run The Suite In Parallel

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

The following TestMu AI session IDs were generated for the successful assignment run:

- Scenario 1, Chrome on Windows 10: `e3d95e25048442a0ec56b984beba7756`
- Scenario 1, Safari on macOS Catalina: `D152A444-6F6E-4AEB-98A0-EA3FDC0D1B6E`
- Scenario 2, Chrome on Windows 10: `f7b0e2aed27ef38a46b1b99a2f20c194`
- Scenario 2, Safari on macOS Catalina: `59005CED-8B1E-48B4-AEE5-1DA7D2855146`
- Scenario 3, Chrome on Windows 10: `f908a57ab7a216c039c023568e473a8a`
- Scenario 3, Safari on macOS Catalina: `C6E6C312-5F5B-4F05-B6EC-B0E094405AD9`

## Local Screenshots

In addition to the TestMu AI cloud artifacts, local screenshots are also available in this repository under:

```text
test-results/screenshots/
```

Included screenshot files:

- `scenario-1-simple-form-demo__chrome-windows-10__5f5bbb755513f7dfa1cf40716b823152.png`
- `scenario-1-simple-form-demo__safari-macos-catalina__B7C272A2-A703-4742-9165-E583F00285B0.png`
- `scenario-2-drag-and-drop-sliders__chrome-windows-10__f2640d8ad11bf9ec2b6ed5a6b4210942.png`
- `scenario-2-drag-and-drop-sliders__safari-macos-catalina__170B1515-E9DE-4355-B83C-7C7C5C50B828.png`
- `scenario-3-input-form-submit__chrome-windows-10__18e8d499cbe3176a489160fd0f58f007.png`
- `scenario-3-input-form-submit__safari-macos-catalina__A4A6A547-00B2-47A6-89D4-4791B61D4B5B.png`

## Submission Notes

- GitHub repository: `https://github.com/rohitjaiswalrj32/selenium-101-assignment`
- The repository should be shared privately with `admin@testmuaicertifications.com` as required.
- The final submission on the exam portal should include the GitHub repository URL and the TestMu AI session IDs listed above.
