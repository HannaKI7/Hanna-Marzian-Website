from playwright.sync_api import sync_playwright
import os

html_path = r"G:\Meine Ablage\Claudes Playground\scale²\Client Projects\Hanna KI\Stories\story_website_workshop.html"
out_dir = r"G:\Meine Ablage\Claudes Playground\scale²\Client Projects\Hanna KI\Stories"
file_url = "file:///" + html_path.replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 900})
    page.goto(file_url)
    page.wait_for_timeout(800)

    cards = page.query_selector_all(".story-card")
    print(f"Found {len(cards)} cards")
    for i, card in enumerate(cards):
        out_path = os.path.join(out_dir, f"story_{i+1:02d}.jpg")
        card.screenshot(path=out_path, type="jpeg", quality=95)
        print(f"Saved: {out_path}")

    browser.close()
    print("Done.")
