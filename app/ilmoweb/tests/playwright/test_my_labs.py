from playwright.sync_api import Page, expect
from helper_functions import login

def test_login_and_navigate_to_my_labs(page: Page):
    page.goto('/')
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_role('heading', name='Omat ilmoittautumiset')).to_be_visible()

def test_enrolled_group_is_visible_in_my_labs(page: Page):
    login(page, 'kemianopiskelija', 'salasana123')
    page.get_by_role('link', name='Laboratoriotyöt').click()
    page.locator('[data-testid="1"]').click()
    page.get_by_role('link', name='Omat labrat').click()
    expect(page.get_by_text('labra 1')).to_be_visible()