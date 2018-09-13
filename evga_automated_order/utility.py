from selenium.webdriver.support.ui import Select


def update_text_field(input_box, text):
    input_box.clear()
    input_box.send_keys(text)


def update_text_field_by_id(driver, dom_id, value):
    input_box = driver.find_element_by_id(dom_id)
    update_text_field(input_box, str(value))


def update_text_field_by_name(driver, name, value):
    input_box = driver.find_element_by_name(name)
    update_text_field(input_box, str(value))


def update_select_field(driver, dom_id, value):
    element = driver.find_element_by_id(dom_id)
    select_box = Select(element)
    select_box.select_by_visible_text(str(value))


def remove_element_by_class(driver, class_name):
    driver.execute_script("""
            var className = arguments[0];
            var element = document.querySelector("." + className);
            if (element)
                element.parentNode.removeChild(element);
        """, class_name)


# noinspection PyBroadException
def try_parse_float(string):
    try:
        return float(string)
    except:
        return None
