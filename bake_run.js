/* Frame-step the bake page and write PNG-with-alpha frames per person.
   One exact loop: fps=30, frames = loopLen*fps = 3.9*30 = 117. */
const { chromium } = require('/Users/marcoopertti/lf-next/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const OUTDIR = '/private/tmp/claude-501/-Users-marcoopertti-LF-Website/0ac44c05-f439-478e-b304-1a5f5adbdd4d/scratchpad/bake';
const FPS = 30, FRAMES = 117;

(async () => {
  const browser = await chromium.launch({ headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const ctx = await browser.newContext({ viewport: { width: 700, height: 600 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  page.on('pageerror', e => { console.error('pageerror', e); process.exit(1); });
  await page.goto('file:///Users/marcoopertti/LF-Website/.tmp/people-ascii-mockup/bake.html');
  const n = await page.evaluate(() => window.__bake.ready());
  const stems = await page.evaluate(() => window.STEMS || null) ||
    ['Sarah','Marco','Nate','Ruben','Sheelagh','Isaiah','Ryan','Morgan','Shelley'];
  for (const s of stems) fs.mkdirSync(path.join(OUTDIR, s), { recursive: true });
  console.log('tiles ready:', n);
  for (let k = 0; k < FRAMES; k++) {
    await page.evaluate(([k, fps]) => window.__bake.setPhase(k, fps), [k, FPS]);
    for (let i = 0; i < n; i++) {
      const url = await page.evaluate((i) => window.__bake.grab(i), i);
      const b = Buffer.from(url.slice('data:image/png;base64,'.length), 'base64');
      fs.writeFileSync(path.join(OUTDIR, stems[i], `f_${String(k).padStart(3,'0')}.png`), b);
    }
    if (k % 20 === 0) console.log('frame', k, '/', FRAMES);
  }
  console.log('done');
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
