const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const formats = JSON.parse(fs.readFileSync('formats.json'));
  const b = await chromium.launch();
  for (const [name, [w, h]] of Object.entries(formats)) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(name + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    await p.screenshot({ path: `out/${name}.jpg`, type: 'jpeg', quality: 92 });
    await p.close(); console.log('rendered', name);
  }
  await b.close();
})();
