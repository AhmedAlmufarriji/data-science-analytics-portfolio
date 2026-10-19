const API = async (path, options={}) => { const res = await fetch(`/api/${path}`, options); const data = await res.json(); if(!res.ok) throw new Error(data.detail || `HTTP ${res.status}`); return data; };
const $ = (id) => document.getElementById(id);
const svgNs = 'http://www.w3.org/2000/svg';
let state = {network:null, analysis:null, forecast:null};

function svgEl(tag, attrs={}, text='') { const e=document.createElementNS(svgNs,tag); Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v)); if(text) e.textContent=text; return e; }
function renderGraph(network,analysis) {
  const target=$('graph'); target.replaceChildren(); const svg=svgEl('svg',{viewBox:'0 0 1080 480',preserveAspectRatio:'xMidYMid meet'}); const byId=Object.fromEntries(network.nodes.map(n=>[n.id,n]));
  const ranking=(analysis?.candidates||[]).map(x=>x.pipe_id);
  for(const pipe of network.pipes) {
    const a=byId[pipe.source],b=byId[pipe.target]; const x1=a.x*10.4+19,y1=a.y*4.3+15,x2=b.x*10.4+19,y2=b.y*4.3+15;
    const line=svgEl('line',{x1,y1,x2,y2,class:`pipe ${ranking[0]===pipe.id?'hot':ranking[1]===pipe.id?'second':''}`});
    line.addEventListener('click',()=>{ $('pipeSelect').value=pipe.id; $('scenarios').scrollIntoView({behavior:'smooth'}); });
    const title=svgEl('title',{},`${pipe.id} · ${pipe.length_m} meters. Click to simulate closure.`); line.appendChild(title);svg.appendChild(line);
    if(ranking.slice(0,2).includes(pipe.id))svg.appendChild(svgEl('text',{x:(x1+x2)/2+4,y:(y1+y2)/2-8,class:'pipe-label'},pipe.id));
  }
  for(const node of network.nodes) { const x=node.x*10.4+19,y=node.y*4.3+15;
    svg.appendChild(svgEl('circle',{cx:x,cy:y,r:node.id==='RES'?11:9,class:`node ${node.id==='RES'?'supply':''}`}));
    svg.appendChild(svgEl('text',{x:x+15,y:y-1,class:'node-label'},node.id));
    svg.appendChild(svgEl('text',{x:x+15,y:y+13,class:'node-name'},node.name));
  } target.appendChild(svg);
}
function renderRankings(data){const candidates=data.candidates||[];const max=Math.max(0.1,...candidates.map(c=>c.evidence_score));$('rankings').replaceChildren();
  for(const [i,c] of candidates.entries()){
    const row=document.createElement('div');row.className='rank';
    const num=document.createElement('span');num.className='rank-number';num.textContent=String(i+1).padStart(2,'0');
    const main=document.createElement('div');main.className='rank-main';const name=document.createElement('div');name.className='rank-name';
    const title=document.createElement('strong');title.textContent=`Pipe ${c.pipe_id}`;const region=document.createElement('span');region.textContent=c.district+' District';name.append(title,region);
    const bar=document.createElement('div');bar.className='rank-bar';const inner=document.createElement('span');inner.style.width=`${Math.round(100*c.evidence_score/max)}%`;bar.appendChild(inner);main.append(name,bar);
    const score=document.createElement('span');score.className='rank-score';score.textContent=c.evidence_score.toFixed(2);row.append(num,main,score);$('rankings').appendChild(row);
  }
}
function renderChart(forecast){const el=$('chart');el.replaceChildren();const points=forecast.points;const W=650,H=258,pad=33;
  const svg=svgEl('svg',{viewBox:`0 0 ${W} ${H}`,preserveAspectRatio:'none'});
  const values=points.map(x=>x.total_lps_proxy),min=Math.min(...values)*.93,max=Math.max(...values)*1.04;
  const px=i=>pad+(W-2*pad)*i/Math.max(points.length-1,1),py=v=>H-pad-(H-2*pad)*(v-min)/Math.max(.01,max-min);
  for(let j=0;j<=3;j++){let y=pad+(H-2*pad)*j/3;svg.appendChild(svgEl('line',{x1:pad,y1:y,x2:W-pad,y2:y,stroke:'#345060','stroke-dasharray':'4 8'}));svg.appendChild(svgEl('text',{x:1,y:y+4,fill:'#87a4b0','font-size':'11'},String(Math.round(max-(max-min)*j/3))));}
  const line=points.map((p,i)=>`${i?'L':'M'}${px(i).toFixed(1)},${py(p.total_lps_proxy).toFixed(1)}`).join(' ');
  const area=`${line} L ${px(points.length-1)},${H-pad} L ${pad},${H-pad} Z`;
  const defs=svgEl('defs'),grad=svgEl('linearGradient',{id:'areaFill',x1:'0',x2:'0',y1:'0',y2:'1'});
  grad.append(svgEl('stop',{offset:'0%','stop-color':'#42cbb9','stop-opacity':'.29'}),svgEl('stop',{offset:'100%','stop-color':'#42cbb9','stop-opacity':'.005'}));defs.appendChild(grad);svg.appendChild(defs);
  svg.appendChild(svgEl('path',{d:area,fill:'url(#areaFill)'}));svg.appendChild(svgEl('path',{d:line,stroke:'#55d6c6','stroke-width':'3.2',fill:'none','stroke-linecap':'round','stroke-linejoin':'round'}));
  points.forEach((p,i)=>{if(i===0||i===points.length-1||i%3===0)svg.appendChild(svgEl('text',{x:px(i),y:H-8,fill:'#8dabb8','font-size':'11','text-anchor':'middle'},`+${p.hour_ahead}h`));});
  el.appendChild(svg);$('forecastError').textContent=`Holdout MAE: ${forecast.holdout_mae_lps_per_node} per node`;
}
function renderScenario(data){const result=$('scenarioResult');result.replaceChildren();const row=document.createElement('div');row.className='scenario-kpis';
  for(const [value,label] of [[data.reachable_nodes,'REACHABLE NODES'],[data.unreachable_nodes.length,'DISCONNECTED'],[data.risk_index+'/100','RISK INDEX']]){
    const box=document.createElement('div'),v=document.createElement('strong'),l=document.createElement('small');v.textContent=value;l.textContent=label;box.append(v,l);row.appendChild(box);
  }result.appendChild(row);const p=document.createElement('p');p.style.marginTop='15px';p.textContent=`Affected paths: ${data.affected_nodes.length}; outage-hours proxy: ${data.customer_outage_hours_proxy}. This is a topology-only simulation.`;result.appendChild(p);
}
function addBubble(kind,text){const el=document.createElement('div');el.className=`bubble ${kind}`;el.textContent=text;$('chatHistory').appendChild(el);$('chatHistory').scrollTop=$('chatHistory').scrollHeight;}
async function askAgent(message){addBubble('user',message);$('chatInput').value='';try{const data=await API('agent',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,session_id:'browser-demo'})});
  const cited=data.evidence?.map(e=>e.source_id).join(', ')||'No matching local document';addBubble('tool',`${data.answer}\n\nReferences: ${cited}`);$('toolLog').textContent=`Tools: ${data.tools_used.join(' · ')||'none'}`;
}catch(e){addBubble('tool',`Request failed: ${e.message}`);}}
async function load(){try{
  const [network,analysis,forecast]=await Promise.all([API('network'),API('analyze'),API('forecast?horizon=12')]);state={network,analysis,forecast};
  $('nodeCount').textContent=network.nodes.length-1;$('anomalyCount').textContent=analysis.flagged_nodes.length;$('topPipe').textContent=analysis.candidates[0]?.pipe_id||'—';
  $('peakDemand').textContent=Math.round(Math.max(...forecast.points.map(p=>p.total_lps_proxy))).toLocaleString();
  renderGraph(network,analysis);renderRankings(analysis);renderChart(forecast);
  const sel=$('pipeSelect');const old=sel.value;sel.replaceChildren();for(const p of network.pipes){const opt=document.createElement('option');opt.value=p.id;opt.textContent=`${p.id} · ${p.source} → ${p.target}`;sel.appendChild(opt);}sel.value=old||analysis.candidates[0]?.pipe_id||'P10';
}catch(e){$('rankings').textContent=`Could not load demo: ${e.message}`;}}
$('scenarioForm').addEventListener('submit',async e=>{e.preventDefault();try{const data=await API('scenarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pipe_id:$('pipeSelect').value,repair_hours:Number($('repairHours').value)})});renderScenario(data);}catch(err){$('scenarioResult').textContent=err.message;}});
$('chatForm').addEventListener('submit',e=>{e.preventDefault();const q=$('chatInput').value.trim();if(q)askAgent(q);});
document.querySelectorAll('[data-query]').forEach(x=>x.addEventListener('click',()=>askAgent(x.dataset.query)));
$('refreshBtn').addEventListener('click',load);$('clearChat').addEventListener('click',async()=>{await API('sessions/browser-demo',{method:'DELETE'});$('chatHistory').replaceChildren();addBubble('system','Session memory cleared.');$('toolLog').textContent='Tools: waiting';});
load();
