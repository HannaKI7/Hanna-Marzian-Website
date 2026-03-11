const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Load the HTML file
  const filePath = path.resolve('product-3d.html');
  await page.goto('file:///' + filePath.replace(/\\/g, '/'));

  // Set viewport large enough
  await page.setViewport({ width: 800, height: 700, deviceScaleFactor: 2 });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 500));

  // Make body background transparent for screenshot
  await page.evaluate(() => {
    document.body.style.background = 'transparent';
    document.body.style.overflow = 'visible';
    const before = document.querySelector('body::before');
  });

  // Get bounding box of the scene element
  const scene = await page.$('.scene');
  const box = await scene.boundingBox();

  // Add some padding
  const padding = 60;
  const clip = {
    x: Math.max(0, box.x - padding),
    y: Math.max(0, box.y - padding),
    width: box.width + padding * 2,
    height: box.height + padding * 2.5
  };

  await page.screenshot({
    path: 'product-3d.png',
    omitBackground: true,
    clip: clip
  });

  console.log('PNG gespeichert: product-3d.png');
  console.log('Clip:', JSON.stringify(clip));
  await browser.close();
})();
