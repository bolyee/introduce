const puppeteer = require('/Users/leehyunjoong/.npm/_npx/e5f4bcd55d2c7c9f/node_modules/puppeteer-core');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,userDataDir:'/tmp/portfolio-browser-'+Date.now(),args:['--no-first-run']});
 try{
 const page=await browser.newPage(); const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const target='file://'+path.resolve(__dirname,'../site/index.html');
 for(const width of [1440,768,390,320]){
 await page.setViewport({width,height:1000});await page.goto(target);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'horizontal overflow '+width);
 assert.equal(await page.$$eval('details',a=>a.length),3);
 await page.focus('summary');await page.keyboard.press('Enter');
 assert(await page.$eval('details',d=>d.open));await page.keyboard.press('Enter');
 assert(!(await page.$eval('details',d=>d.open)));
 assert.equal(await page.$$eval('audio',a=>a.length),0);
 await page.screenshot({path:path.resolve(__dirname,`../private/preview-${width}.png`),fullPage:true});
 }
 await page.goto(target);await page.keyboard.press('Tab');
 assert(await page.evaluate(()=>document.activeElement.classList.contains('skip')));
 assert.deepEqual(errors,[]);console.log('PASS: mobile overflow, keyboard details, skip link, no empty players, no JS errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
