import asyncio
from playwright.async_api import async_playwright

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { background: transparent; }
  .wrap {
    display: inline-flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 40px 48px 36px;
  }
  .title {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 96px;
    font-weight: 700;
    line-height: 1;
    letter-spacing: 8px;
    text-transform: uppercase;
    color: #2A1608;
    white-space: nowrap;
  }
  .title em {
    font-style: italic;
    color: #E8894E;
  }
  .line {
    margin-top: 14px;
    width: 100%;
    height: 3px;
    background: linear-gradient(to right, #D8622A, #E8894E, transparent 85%);
    border-radius: 2px;
  }
</style>
</head>
<body>
<div class="wrap" id="logo">
  <div class="title">Fake it <em>Real</em></div>
  <div class="line"></div>
</div>
</body>
</html>"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Seite laden (inline HTML)
        await page.set_content(HTML, wait_until="networkidle")

        # Auf Font warten
        await page.wait_for_timeout(1200)

        # Bounding Box des Logo-Elements holen
        el = await page.query_selector("#logo")
        box = await el.bounding_box()

        # Screenshot: nur das Element, transparent
        clip = {
            "x": box["x"],
            "y": box["y"],
            "width": box["width"],
            "height": box["height"],
        }

        output = r"G:\Meine Ablage\Claudes Playground\scale²\Hanna KI\fake-it-real-logo-dark.png"
        await page.screenshot(
            path=output,
            clip=clip,
            omit_background=True,  # transparenter Hintergrund
            scale="device",
        )

        print(f"Gespeichert: {output}")
        print(f"Groesse: {round(box['width'])}x{round(box['height'])}px")
        await browser.close()

asyncio.run(main())
