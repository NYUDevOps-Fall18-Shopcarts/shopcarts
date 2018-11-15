"""
Shopcart Steps

Steps file for Shopcart.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS=30

BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@given('data for shopcart entries')
def step_impl(context):
    """ Delete all Shopcart entries and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/shopcarts/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/shopcarts'
    for row in context.table:
        data = {
            "product_id": row['product_id'],
            "user_id": row['user_id'],
            "quantity": row['quantity'],
            "price": row['price']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@when('I set the "{element_name}" to {text_string}')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower()
    element_id = element_id.replace(" ","_")
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)
