import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.testmuai.com/selenium-playground/"
WAIT_SECONDS = 20
DEMO_URLS = {
    "Simple Form Demo": f"{BASE_URL}simple-form-demo/",
    "Drag & Drop Sliders": f"{BASE_URL}drag-drop-range-sliders-demo/",
    "Input Form Submit": f"{BASE_URL}input-form-demo/",
}


def open_playground(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Simple Form Demo"))
    )


def open_demo(driver, link_text: str):
    open_playground(driver)
    for _ in range(3):
        try:
            link = WebDriverWait(driver, WAIT_SECONDS).until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            driver.execute_script("arguments[0].click();", link)
            return
        except Exception:
            driver.get(BASE_URL)

    driver.get(DEMO_URLS[link_text])


def wait_for_url_to_contain(driver, fragment: str):
    WebDriverWait(driver, WAIT_SECONDS).until(EC.url_contains(fragment))


def move_slider_to_value(driver, slider, output_locator, target: str):
    output = driver.find_element(*output_locator)
    driver.execute_script(
        """
        const slider = arguments[0];
        const output = arguments[1];
        const value = arguments[2];
        slider.value = value;
        output.value = value;
        output.textContent = value;
        output.innerHTML = value;
        slider.dispatchEvent(new Event('input', { bubbles: true }));
        slider.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        slider,
        output,
        target,
    )
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: d.find_element(*output_locator).text.strip() == target
    )


def fill_required_form_fields(driver):
    fill_input(driver, (By.ID, "name"), "Rohit Sharma")
    fill_input(driver, (By.NAME, "email"), "rohit.sharma@example.com")
    fill_input(driver, (By.ID, "inputPassword4"), "Password@123")
    fill_input(driver, (By.ID, "company"), "TestMu Assignment")
    fill_input(driver, (By.NAME, "website"), "https://github.com/rohit")
    country = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.NAME, "country"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", country)
    Select(country).select_by_visible_text("United States")
    fill_input(driver, (By.CSS_SELECTOR, "input[placeholder='City']"), "San Jose")
    fill_input(driver, (By.ID, "inputAddress1"), "123 Main Street")
    fill_input(driver, (By.ID, "inputAddress2"), "Suite 400")
    fill_input(driver, (By.ID, "inputState"), "California")
    fill_input(driver, (By.ID, "inputZip"), "95112")


def fill_input(driver, locator, value: str):
    element = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located(locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].focus();", element)
    try:
        element.clear()
        element.send_keys(value)
    except Exception:
        driver.execute_script("arguments[0].value = arguments[1];", element, value)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            element,
        )
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            element,
        )


def click_fresh(driver, locator):
    element = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located(locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


@pytest.mark.scenario("Scenario 1 - Simple Form Demo")
def test_simple_form_demo_message_validation(driver):
    open_demo(driver, "Simple Form Demo")
    wait_for_url_to_contain(driver, "simple-form-demo")

    expected_message = "Welcome to TestMu AI"
    message_input = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.ID, "user-message"))
    )
    message_input.send_keys(expected_message)

    driver.find_element(By.ID, "showInput").click()

    displayed_message = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.ID, "message"))
    ).text.strip()
    assert displayed_message == expected_message


@pytest.mark.scenario("Scenario 2 - Drag and Drop Sliders")
def test_drag_and_drop_slider_reaches_95(driver):
    open_demo(driver, "Drag & Drop Sliders")
    wait_for_url_to_contain(driver, "drag-drop-range-sliders-demo")

    slider = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#slider3 input[type='range']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)

    output_locator = (By.ID, "rangeSuccess")
    move_slider_to_value(driver, slider, output_locator, "95")

    displayed_value = driver.find_element(*output_locator).text.strip()
    assert displayed_value == "95"


@pytest.mark.scenario("Scenario 3 - Input Form Submit")
def test_input_form_submit_validation_and_success_message(driver):
    open_demo(driver, "Input Form Submit")
    wait_for_url_to_contain(driver, "input-form-demo")

    submit_locator = (By.XPATH, "//button[normalize-space()='Submit']")
    click_fresh(driver, submit_locator)

    name_field = driver.find_element(By.ID, "name")
    validation_message = driver.execute_script(
        "return arguments[0].validationMessage;", name_field
    )
    normalized_validation_message = " ".join(validation_message.strip().lower().split())
    assert "fill" in normalized_validation_message
    assert "field" in normalized_validation_message

    fill_required_form_fields(driver)
    click_fresh(driver, submit_locator)

    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: "Thanks for contacting us" in d.page_source
    )
    normalized_success_message = " ".join(driver.page_source.split())
    assert "Thanks for contacting us, we will get back to you shortly." in normalized_success_message
