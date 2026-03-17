from playwright.sync_api import Page, expect


def test_dashboard_loads(page: Page):
    page.goto("http://127.0.0.1:8050", wait_until="networkidle")
    expect(page.locator("text=НРИ-Помощник (офлайн)")).to_be_visible()
    expect(page.locator("text=Аналитический дашборд")).to_be_visible()
    expect(page.locator("text=Дашборд")).to_be_visible()
    expect(page.locator("text=Персонажи")).to_be_visible()
