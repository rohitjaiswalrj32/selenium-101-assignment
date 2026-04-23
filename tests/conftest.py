import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import pytest
from selenium import webdriver


GRID_HOST = "hub.lambdatest.com/wd/hub"
DEFAULT_PROJECT = "Selenium 101 Assignment"
DEFAULT_BUILD = "Selenium Playground Parallel Suite"
SESSION_LOG = Path("test-results/session_ids.txt")


@dataclass(frozen=True)
class BrowserConfig:
    browser_name: str
    browser_version: str
    platform_name: str

    @property
    def id(self) -> str:
        platform_slug = self.platform_name.lower().replace(" ", "-")
        return f"{self.browser_name.lower()}-{platform_slug}"


def _default_browser_matrix() -> list[BrowserConfig]:
    return [
        BrowserConfig(
            browser_name="Chrome",
            browser_version="latest",
            platform_name="Windows 10",
        ),
        BrowserConfig(
            browser_name="Safari",
            browser_version="latest",
            platform_name="macOS Catalina",
        ),
    ]


def _load_browser_matrix() -> Iterable[BrowserConfig]:
    raw_matrix = os.getenv("LT_BROWSER_MATRIX")
    if not raw_matrix:
        return _default_browser_matrix()

    matrix = json.loads(raw_matrix)
    return [
        BrowserConfig(
            browser_name=entry["browserName"],
            browser_version=entry.get("browserVersion", "latest"),
            platform_name=entry["platformName"],
        )
        for entry in matrix
    ]


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "browser_config" not in metafunc.fixturenames:
        return

    configs = list(_load_browser_matrix())
    metafunc.parametrize("browser_config", configs, ids=[cfg.id for cfg in configs])


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "scenario(name): human readable scenario label for TestMu AI session naming",
    )
    SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
    SESSION_LOG.write_text("", encoding="utf-8")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _build_lt_options(test_name: str, browser_config: BrowserConfig) -> dict:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")

    return {
        "user": username,
        "username": username,
        "accessKey": access_key,
        "project": os.getenv("LT_PROJECT", DEFAULT_PROJECT),
        "build": os.getenv("LT_BUILD", DEFAULT_BUILD),
        "name": test_name,
        "platformName": browser_config.platform_name,
        "network": True,
        "video": True,
        "visual": True,
        "console": True,
        "w3c": True,
    }


def _remote_url() -> str:
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")

    if not username or not access_key:
        raise RuntimeError(
            "LT_USERNAME and LT_ACCESS_KEY must be set before running these tests."
        )

    return f"https://{GRID_HOST}"


@pytest.fixture
def driver(request: pytest.FixtureRequest, browser_config: BrowserConfig):
    marker = request.node.get_closest_marker("scenario")
    scenario_name = marker.args[0] if marker and marker.args else request.node.name
    test_name = f"{scenario_name} | {browser_config.browser_name} on {browser_config.platform_name}"

    options = webdriver.ChromeOptions()
    if browser_config.browser_name.lower() == "safari":
        options = webdriver.SafariOptions()

    options.set_capability("browserName", browser_config.browser_name)
    options.set_capability("browserVersion", browser_config.browser_version)
    options.set_capability("LT:Options", _build_lt_options(test_name, browser_config))

    web_driver = webdriver.Remote(command_executor=_remote_url(), options=options)
    web_driver.maximize_window()

    try:
        yield web_driver
        test_passed = getattr(request.node, "rep_call", None) and request.node.rep_call.passed
        web_driver.execute_script(
            "lambda-status=passed" if test_passed else "lambda-status=failed"
        )
    finally:
        session_id = web_driver.session_id
        with SESSION_LOG.open("a", encoding="utf-8") as log_file:
            log_file.write(f"{test_name}: {session_id}\n")
        print(
            f"TestMu AI session for '{test_name}': {session_id}",
            flush=True,
        )
        web_driver.quit()
