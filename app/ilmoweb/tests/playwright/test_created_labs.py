import re
from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_created_labs(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    expect(page).to_have_title(re.compile('Created labs'))

def test_create_lab_and_check_that_it_is_created(page: Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.locator('[data-testid="1"]').click()
    page.get_by_test_id('lab_name').fill('Testilabra')
    page.get_by_test_id('description').fill('Kuvaus testilabrasta.')
    page.get_by_test_id('max_students').fill('3')
    page.get_by_role('button', name='Luo labra').click()
    page.goto('/created_labs')
    expect(page.get_by_role("cell", name="Testilabra"))

def test_delete_lab_group_and_check_it_is_deleted(page:Page):
    page.goto('/')
    login(page, 'kemianope', 'atomi123')
    page.locator('[data-testid="lab_group_12"]').click()
    page.locator('[data-testid="delete_lab_group_12"]').click()
    expect(page.get_by_role("cell", name="31.10.2025 klo 12 - 16")).to_be_hidden()
    expect(page.get_by_text('D210 (Phy)')).to_be_hidden()
    