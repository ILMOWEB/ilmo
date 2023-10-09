from playwright.sync_api import Page, expect
import pytest

def test_welcome_message(page: Page):
    page.goto('/')
    assert page.inner_text('h1') == 'Fysikaalisen kemian laboratorio - Labra'

def test_login_link(page: Page):
    page.goto('/')
    page.get_by_role("button", name="Kirjaudu sisään").click()
    expect(page.get_by_role("heading", name="Log In")).to_be_visible()

def test_logging_in(page: Page):
    page.goto('/')
    page.get_by_role("button", name="Kirjaudu sisään").click()
    page.get_by_role("textbox", name="username").fill('kemianope')
    page.get_by_role("textbox", name="password").fill('atomi123')
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("heading", name="Tervetuloa laboratoriotöiden ilmoittautumis- ja palautusjärjestelmään kemianope!")).to_be_visible()

