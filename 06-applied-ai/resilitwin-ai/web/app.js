const $ = s => document.querySelector(s);
const fmt = (n, digits = 0) => Number(n).toLocaleString('en-US', {maximumFractionDigits:digits});
const money = n => `${n >= 0 ? '+' : '−'}$${fmt(Math.abs(n))}`;
const signed = (n, suffix='') => `${n >= 0 ? '+' : '−'}${fmt(Math.abs(n), 2)}${suffix}`;
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let productInfo = {}, forecasts = [];
async function getJson(path, options={}) {
  const response = await fetch(path, options);
  if (!response.ok) throw new Error(`${response.status} ${await response.text()}`);
  return response.json();
}
function renderChart(items) {
  const w=900,h=232,left=48,right=22,top=20,bottom=39;
  const max=Math.ceil(Math.max(...items.map(d=>d.high))*1.08);const min=0;
  const X=i=>left+i/(items.length-1)*(w-left-right);
  const Y=v=>h-bottom-(v-min)/(max-min)*(h-bottom-top);
  const upper=items.map(x=>x.high),lower=items.map(x=>x.low),means=items.map(x=>x.mean);
  let grid='';for(let i=0;i<=4;i++){const y=Y(i*max/4);grid+=`<line x1="${left}" y1="${y}" x2="${w-right}" y2="${y}" stroke="#263d4d" stroke-dasharray="4 6"/><text x="${left-9}" y="${y+4}" text-anchor="end" fill="#8396a8" font-size="12">${Math.round(i*max/4)}</text>`;}
  const labels=[0,5,10,15,20].map(i=>`<text x="${X(i)}" y="${h-12}" text-anchor="middle" fill="#8396a8" font-size="12">${items[i].date.slice(5)}</text>`).join('');
  const area=upper.map((v,i)=>`${X(i)},${Y(v)}`).join(' ')+' '+lower.map((v,i)=>`${X(lower.length-1-i)},${Y(lower[lower.length-1-i])}`).join(' ');
  $('#forecast-plot').innerHTML=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Daily demand forecast with an illustrative uncertainty band" preserveAspectRatio="none">${grid}<polygon points="${area}" fill="#77cfa4" fill-opacity=".16"/><polyline points="${means.map((v,i)=>`${X(i)},${Y(v)}`).join(' ')}" fill="none" stroke="#c2f27b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>${means.map((v,i)=>i%4===0?`<circle cx="${X(i)}" cy="${Y(v)}" r="3.5" fill="#cff9a0"/>`:'').join('')}${labels}</svg>`;
}
function chooseSku(){const sku=$('#sku-select').value;const rows=forecasts.filter(r=>r.sku===sku);if(!rows.length)return;renderChart(rows);$('#sku-total').textContent=`${fmt(rows.reduce((s,r)=>s+r.mean,0))} units`;$('#sku-inventory').textContent=`${fmt(productInfo[sku].inventory)} units`;$('#sku-name').textContent=productInfo[sku].name;}
function syncSliders(){const settings=[['duration',n=>`${n} days`],['shock',n=>`${n>=0?'+':''}${n}%`],['carbon',n=>`$${fmt(n)} / tCO₂e`],['risk',n=>`${n}×`],['budget',n=>`$${fmt(n)}`]];for(const [id,fn] of settings){const el=$(`#${id}`);const refresh=()=>{$(`#${id}-value`).textContent=fn(Number(el.value))};el.addEventListener('input',refresh);refresh();}}
async function run(){const button=$('#run');button.disabled=true;button.textContent='Optimizing…';$('#run-state').textContent='RUNNING';try{
 const payload={outages:$('#outage').value?[$('#outage').value]:[],disruption_days:+$('#duration').value,demand_shock_pct:+$('#shock').value,carbon_price_per_ton:+$('#carbon').value,risk_aversion:+$('#risk').value,budget:+$('#budget').value,service_target:.9,trials:250};
 const data=await getJson('/api/scenarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
 $('#base-service').textContent=`${(data.baseline.stress_test.expected_service_rate*100).toFixed(1)}%`;
 $('#optimized-service').textContent=`${(data.optimized.stress_test.expected_service_rate*100).toFixed(1)}%`;
 $('#delta-service').textContent=signed(data.differences.expected_service_percentage_points,' pp');
 $('#delta-cost').textContent=money(data.differences.purchase_cost);
 $('#delta-carbon').textContent=signed(data.differences.emissions_kg,' kg');
 $('#reliability').textContent=`${(data.optimized.stress_test.probability_meeting_target*100).toFixed(1)}%`;
 $('#decision-note').textContent=data.decision_notes.length?data.decision_notes.join(' '):'Allocation solved. Review costs, supplier diversity and simulated downside risk before acting.';
 $('#allocation-list').innerHTML=data.optimized.allocations.map(a=>`<tr><td>${esc(a.sku)}</td><td>${esc(a.supplier)}</td><td>${fmt(a.units,1)}</td><td>${a.lead_days} days</td><td>${fmt(a.emissions_kg,1)} kg</td></tr>`).join('') || '<tr><td colspan="5">No feasible procurement within current constraints.</td></tr>';
 $('#run-state').textContent='SCENARIO READY';
 }catch(err){$('#run-state').textContent='ERROR';$('#decision-note').textContent=err.message;}finally{button.disabled=false;button.innerHTML='Simulate & optimize <span>→</span>';}}
async function query(){const q=$('#query').value.trim();if(!q)return;$('#evidence-list').innerHTML='<div class="loading-text">Searching indexed synthetic playbooks…</div>';try{const data=await getJson(`/api/evidence?query=${encodeURIComponent(q)}`);$('#evidence-list').innerHTML=data.documents.map(d=>`<article class="document"><div class="document-head"><strong>${esc(d.title)}</strong><span class="citation">${esc(d.citation)}</span></div><p>${esc(d.excerpt)}</p><small>Source: ${esc(d.source_path)} · relevance ${fmt(d.score*100,1)}%</small></article>`).join('')||'<div class="loading-text">No supporting document found for these terms. Try a different query.</div>';}catch(err){$('#evidence-list').textContent=err.message;}}
async function boot(){syncSliders();$('#run').addEventListener('click',run);$('#search').addEventListener('click',query);$('#query').addEventListener('keydown',e=>{if(e.key==='Enter')query()});$('#sku-select').addEventListener('change',chooseSku);try{const [overview,pred,card]=await Promise.all([getJson('/api/overview'),getJson('/api/forecasts'),getJson('/api/model-card')]);productInfo=Object.fromEntries(overview.products.map(p=>[p.sku,p]));forecasts=pred.forecasts;$('#kpi-products').textContent=overview.products.length;$('#kpi-suppliers').textContent=overview.suppliers.length;$('#kpi-wape').textContent=`${(card.wape_model*100).toFixed(1)}%`;$('#sku-select').innerHTML=overview.products.map(p=>`<option value="${esc(p.sku)}">${esc(p.sku)}</option>`).join('');$('#outage').innerHTML+=[...overview.suppliers].map(s=>`<option value="${esc(s.code)}">${esc(s.name)}</option>`).join('');chooseSku();$('#status').innerHTML='<i></i> Engine online';await Promise.all([run(),query()]);}catch(err){$('#status').textContent='Initialization error';$('#decision-note').textContent=`Could not load engine: ${err.message}`;}}
boot();
