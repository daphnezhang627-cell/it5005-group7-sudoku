const {chromium}=require(process.argv[2]);
const fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
 const project=path.resolve(__dirname,'..'),out=path.join(project,'validation_outputs');
 const url=process.argv[3]||'http://127.0.0.1:8502/';const remote=url.startsWith('https:');
 const pool=JSON.parse(fs.readFileSync(path.join(project,'puzzles.json'),'utf8'));
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1050}});page.setDefaultTimeout(90000);
 const errors=[],checks=[],runs=[];page.on('pageerror',e=>errors.push(String(e)));
 let ui=page;
 try{
  await page.goto(url,{timeout:90000});
  if(remote)ui=page.frameLocator('iframe[title="streamlitApp"]');
  await ui.getByRole('heading',{name:'Sudoku Logic Tutor',exact:true}).waitFor();
  const settled=()=>ui.locator('[data-testid="stApp"][data-test-script-state="notRunning"]').waitFor({timeout:240000});
  await ui.getByRole('button',{name:'Solve selected puzzle',exact:true}).waitFor();await settled();
  for(let i=0;i<5;i++){
   const entry=pool.puzzles[i],count=Object.keys(entry.givens).length;
   if(i){await ui.getByRole('combobox').click();await ui.getByRole('combobox').press('ArrowDown');await ui.getByRole('option',{name:`Puzzle ${i+1} — ${count} givens`,exact:true}).click();await ui.getByRole('grid').nth(1).waitFor({state:'hidden'});await settled();}
   for(let tries=0;tries<100;tries++){if(await ui.getByRole('grid').count()===1 && await ui.getByRole('gridcell',{name:/^given cell/}).count()===count)break;await page.waitForTimeout(100);}
   assert.equal(await ui.getByRole('grid').count(),1);
   assert.equal(await ui.getByRole('gridcell',{name:/^given cell/}).count(),count);
   for(const method of ['Backward chaining','Forward chaining']){
    await ui.getByText(method,{exact:true}).click();await settled();
    await ui.getByRole('button',{name:'Solve selected puzzle',exact:true}).click();
    await ui.getByText(new RegExp(`^${method} solved the grid in`)).waitFor({timeout:240000});await settled();
    const values=await ui.getByRole('grid').nth(1).getByRole('gridcell').allTextContents();assert.equal(values.length,81);
    for(let k=0;k<81;k++)assert.equal(Number(values[k]),entry.solution[`${Math.floor(k/9)+1}_${k%9+1}`]);
    runs.push({puzzle:i+1,method,result:await ui.getByText(new RegExp(`^${method} solved the grid in`)).innerText()});
   }
   const cell=Object.keys(entry.solution).find(k=>!(k in entry.givens));const [r,c]=cell.split('_').map(Number),v=entry.solution[cell];
   for(const value of [v,v%9+1]){
    for(const [label,num] of [['Row',r],['Column',c],['Value',value]]){const input=ui.getByRole('spinbutton',{name:label,exact:true});await input.fill(String(num));await input.press('Tab');await settled();}
    await ui.getByRole('button',{name:'Check entailment',exact:true}).click();
    await ui.getByText(value==v?`True — cell (${r}, ${c}) must contain ${value}.`:`False — value ${value} is eliminated from cell (${r}, ${c}).`,{exact:true}).waitFor();await settled();
    const exp=ui.locator('[data-testid="stExpander"]');assert.match(await exp.innerText(),/Reasoning trace \([1-9]\d* steps\)/);
    if(await exp.locator('details').getAttribute('open')===null)await exp.locator('summary').click();
    assert.match(await exp.innerText(),/this is a given|remaining candidate|eliminated/);
   }
   checks.push(`Puzzle ${i+1}: FC/BC exact grids, givens, queries and proof text PASS`);console.log(checks.at(-1));
  }
  await ui.getByRole('combobox').click();await ui.getByRole('combobox').press('ArrowDown');await ui.getByRole('option',{name:'Puzzle 1 — 30 givens',exact:true}).click();await ui.getByRole('grid').nth(1).waitFor({state:'hidden'});await settled();for(let tries=0;tries<100 && await ui.getByRole('grid').count()!==1;tries++)await page.waitForTimeout(100);assert.equal(await ui.getByRole('grid').count(),1);assert.equal(await ui.locator('[data-testid="stExpander"]').count(),0);
  await page.screenshot({path:path.join(out,remote?'public_desktop.png':'local_desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});const bounds=await ui.getByRole('grid').first().boundingBox();assert(bounds.x>=0&&bounds.x+bounds.width<=391);
  await page.screenshot({path:path.join(out,remote?'public_mobile.png':'local_mobile.png'),fullPage:true});assert.equal(errors.length,0);
  const report={status:'PASS',url,checked_at:new Date().toISOString(),checks,runs,page_errors:errors};fs.writeFileSync(path.join(out,remote?'public_deployment.json':'browser_tests.json'),JSON.stringify(report,null,2));
 }catch(e){await page.screenshot({path:path.join(out,'browser_failure.png'),fullPage:true}).catch(()=>{});console.log((await ui.locator('body').innerText()).slice(-2500));throw e;}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
