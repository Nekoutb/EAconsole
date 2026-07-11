from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.goto("http://127.0.0.1:4173", wait_until="networkidle")
    assert page.locator("h1").inner_text() == "Good morning, IT Team"
    assert page.locator("tbody tr").count() == 4
    page.locator("header input").fill("Insights")
    assert page.locator("tbody tr:visible").count() == 1
    page.locator("header input").fill("")
    page.locator("#runCheck").click()
    page.wait_for_timeout(2100)
    assert "just now" in page.locator(".statusbar span").inner_text()
    page.screenshot(path=str(ROOT / "dashboard-preview.png"), full_page=True)
    assert not errors, errors
    browser.close()
