import logging
from contextlib import closing
from re import sub

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from yaml import load

from utility import try_parse_float, remove_element_by_class, update_text_field_by_id, update_select_field, \
    update_text_field_by_name

WAIT_TIMEOUT = 120


def continue_checkout(driver):
    continue_button = driver.find_element_by_xpath('.//input[@class="btnCheckoutContinue"]')
    continue_button.click()


def is_suitable_product(configuration, link):
    for product in configuration['products']:
        if product['terms'] in link.text:
            container_element = link.find_element_by_xpath('./ancestor::div[@class="list-item"]')
            price_element = container_element.find_element_by_xpath('.//p[@class="pl-list-price"]')
            price = try_parse_float(sub(r'[^\d.]', '', price_element.text))
            if price is None or price < product['maximumPrice']:
                return True
    return False


def main():
    configuration = load(open('configuration.yml'))
    with closing(webdriver.Firefox()) as driver:
        logging.info('Login')
        driver.get('https://secure.evga.com/us/login.asp')
        update_text_field_by_name(driver, 'evga_login', configuration['username'])
        update_text_field_by_name(driver, 'password', configuration['password'])
        login_button = driver.find_element_by_name('login_button')
        login_button.click()

        logging.info('Wait until we are redirected to the home page')
        expected_text = 'Hello, {}'.format(configuration['username'])
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'login-text'), expected_text))

        logging.info('Keep refreshing the page until we find a suitable deal')
        product_link = None
        while product_link is None:
            logging.info('Navigate to the feature page')
            driver.get('https://www.evga.com/products/feature.aspx')

            logging.info('Find all products')
            product_links = driver.find_elements_by_xpath('//a[@class="pl-list-pname"]')

            logging.info('Look for a suitable product')
            for link in product_links:
                if is_suitable_product(configuration, link):
                    product_link = link
                    break

        logging.info('Add the product to the cart')
        container_element = product_link.find_element_by_xpath('./ancestor::div[@class="list-item"]')
        add_to_cart_element = container_element.find_element_by_xpath('.//input[@class="btnAddCart"]')
        add_to_cart_element.click()

        logging.info('Wait until we are redirected to the cart')
        continue_text = input('Good to proceed?')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'btn-checkout')))

        logging.info('Click checkout')
        checkout_button = driver.find_element_by_xpath('.//input[@class="btn-checkout"]')
        checkout_button.click()

        logging.info('Wait until the shipping address screen has loaded')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'btnCheckoutContinue')))

        logging.info('Click continue')
        continue_checkout(driver)

        logging.info('Wait until the shipping options screen has loaded')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'checkoutHeading'),
                                                              'Choose Your Shipping Options'))

        logging.info('Check the agree button')
        agree_checkbox = driver.find_element_by_xpath('.//input[@id="cbAgree"]')
        agree_checkbox.click()

        logging.info('Click continue')
        continue_checkout(driver)

        logging.info('Wait until the billing address screen has loaded')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'checkoutHeading'), 'Enter a Billing Address'))

        logging.info('Click continue')
        continue_checkout(driver)

        logging.info('Wait until the payment selection screen has loaded')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'checkoutHeading'),
                                                              'Enter your Credit Information'))

        logging.info('Remove this damn ajax BG element')
        remove_element_by_class(driver, 'ajax-bg')

        logging.info('Ensure that we are paying with credit card')
        credit_checkbox = driver.find_element_by_xpath('.//input[@value="Credit Card"]')
        credit_checkbox.click()

        logging.info('Wait until the credit card name field is present')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.presence_of_element_located((By.ID, 'ctl00_LFrame_txtNameOnCard')))

        logging.info('Populate credit card fields')
        credit_card = configuration['creditCard']
        update_text_field_by_id(driver, 'ctl00_LFrame_txtNameOnCard', credit_card['name'])
        update_text_field_by_id(driver, 'ctl00_LFrame_txtCardNumber', credit_card['number'])
        update_select_field(driver, 'ctl00_LFrame_ddlMonth', credit_card['month'])
        update_select_field(driver, 'ctl00_LFrame_ddlYear', credit_card['year'])
        update_text_field_by_id(driver, 'ctl00_LFrame_txtCvv', credit_card['cvv'])

        logging.info('Click continue')
        continue_checkout(driver)

        logging.info('Wait until the review screen has been shown')
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'checkoutHeading'), 'Review Your Order'))

        logging.info('Check the agree button')
        agree_checkbox = driver.find_element_by_xpath('.//input[@id="cbAgree"]')
        agree_checkbox.click()

        logging.info('Wait for the user to confirm that they are happy with the order')
        confirmation_text = input('Does this look good?')
        if confirmation_text == 'yes':
            logging.info('Place the order!')
            place_order_button = driver.find_element_by_xpath('.//input[@class="btnPlaceOrder"]')
            place_order_button.click()
            finish_text = input('Did it finish?')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except:
        input('aaaaaaa')
