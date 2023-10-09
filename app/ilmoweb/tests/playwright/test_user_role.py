from playwright.sync_api import Page, expect
import pytest
"""
def test_admin_login_view(page: Page):
    page.goto('/')    
    page.get_by_role("button", name="Kirjaudu sisään").click()
    page.get_by_role("textbox", name="username").fill('admin')
    page.get_by_role("textbox", name="password").fill('admin')
    page.get_by_role("button", name="Log In").click()
    assert page.inner_text('h6') == 'Olet admin roolissa'
"""
def test_student_login_view(page: Page):
    page.goto('/')
    page.get_by_role("button", name="Kirjaudu sisään").click()
    page.get_by_role("textbox", name="username").fill('kemianope')
    page.get_by_role("textbox", name="password").fill('atomi123')
    page.get_by_role("button", name="Log In").click()
    assert page.inner_text('h6') == 'Olet käyttäjäroolissa'
