<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="UTF-8">
<title>AES - ABEL ENGINEERING SOLUTIONS - Offline</title>
<style>
body{background:#0B0E14;color:white;font-family:Arial,sans-serif;padding:12px;margin:0}
.hero{background:linear-gradient(105deg,#FF6A00,#FF2E63,#8A2BE2);border-radius:20px;padding:22px;text-align:center;color:white}
.hero h1{margin:5px 0;font-size:26px;font-weight:900}
.glass{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);border-radius:16px;padding:16px;margin-top:14px}
input,select,textarea{width:100%;padding:12px;margin:6px 0;border-radius:10px;border:0;background:#1A1E2A;color:white;box-sizing:border-box;font-size:14px}
button{background:linear-gradient(90deg,#FF6A00,#FF2E63);color:white;border:0;border-radius:12px;padding:14px;width:100%;font-weight:900;font-size:15px;margin-top:8px;cursor:pointer}
.metric{background:#1A1E2A;border-radius:12px;padding:10px;text-align:center;margin:4px;flex:1}
table{width:100%;margin-top:10px;border-collapse:collapse}
td,th{padding:8px;border-bottom:1px solid #333;font-size:12px;text-align:left}
canvas{width:100%;background:#12151E;border-radius:10px;margin-top:10px}
.receipt-box{background:white;color:black;border-radius:12px;padding:16px;margin-top:12px}
</style>
</head>
<body>
<div class="hero">
<div style="font-size:10px;letter-spacing:3px">WINDHOEK NAMIBIA • OFFLINE MODE</div>
<h1>ABEL ENGINEERING SOLUTIONS</h1>
<p style="font-weight:800">Built for Chaos. Designed to Deliver.</p>
<p style="font-size:12px">AI Job Shop • Gantt • Receipt • Delivery</p>
</div>

<div class="glass">
<h3>📝 New Customer Order</h3>
<input id="cname" placeholder="Customer Name *">
<input id="cphone" placeholder="Phone / WhatsApp *">
<input id="job" placeholder="Job Title * - Steel Gate 2.5m">
<select id="cat"><option>Fabrication</option><option>Welding</option><option>Cutting</option><option>Grinding</option><option>Assembly</option><option>Custom</option></select>
<div style="display:flex;gap:8px">
<input id="qty" type="number" value="1" min="1" style="flex:1">
<input id="hrs" type="number" value="3.5" step="0.5" style="flex:1">
<select id="prio" style="flex:1"><option value="3">Priority 3</option><option value="5">Priority 5</option><option value="1">Priority 1</option></select>
</div>
<label style="display:flex;align-items:center;gap:8px;margin-top:8px"><input id="rush" type="checkbox" style="width:auto"> 🔥 RUSH ORDER - Extra 50%</label>
<textarea id="notes" placeholder="Notes"></textarea>
<button onclick="addOrder()">✅ ADD ORDER & CALCULATE</button>
<div id="msg"></div>
</div>

<div class="glass">
<h3>📊 AES Live Board</h3>
<div style="display:flex"><div class="metric">Revenue<br><b id="rev">N$ 0</b></div><div class="metric">Orders<br><b id="cnt">0</b></div><div class="metric">Makespan<br><b id="span">0h</b></div></div>
<div id="list"><p style="opacity:0.6">No orders yet.</p></div>
<canvas id="gantt" width="800" height="300"></canvas>
<button onclick="clearAll()" style="background:#333;margin-top:10px">🗑️ Clear All Orders</button>
</div>

<div id="receiptWrap"></div>

<script>
let orders = JSON.parse(localStorage.getItem('aes_orders')||'[]');
let rate=350, rushpct=50;
function save(){ localStorage.setItem('aes_orders', JSON.stringify(orders)); }
function addOrder(){
 let cname=document.getElementById('cname').value.trim();
 let job=document.getElementById('job').value.trim();
 let qty=parseFloat(document.getElementById('qty').value)||1;
 let hrs=parseFloat(document.getElementById('hrs').value)||3.5;
 let rush=document.getElementById('rush').checked;
 if(!cname||!job){document.getElementById('msg').innerHTML='<p style=color:#FF3B30>Fill Name & Job!</p>';return;}
 let base=hrs*rate*qty;
 let extra=rush?base*rushpct/100:0;
 let buff=(base+extra)*0.10;
 let tot=base+extra+buff;
 let dh=qty*hrs*1.1;
 let id='AES-'+new Date().toTimeString().slice(0,8).replace(/:/g,'');
 let o={id,cname,job,qty,hrs,base,extra,buff,tot,dh,rush,time:new Date().toLocaleString(),notes:document.getElementById('notes').value};
 orders.push(o); save();
 document.getElementById('msg').innerHTML='<p style=color:#00FF88>✅ Added '+id+' - N$ '+tot.toFixed(0)+'</p>';
 draw(); receipt(o);
}
function draw(){
 let sum=orders.reduce((a,b)=>a+b.tot,0);
 let span=orders.reduce((a,b)=>a+b.dh,0);
 document.getElementById('rev').innerText='N$ '+sum.toFixed(0);
 document.getElementById('cnt').innerText=orders.length;
 document.getElementById('span').innerText=span.toFixed(1)+'h';
 if(orders.length==0){document.getElementById('list').innerHTML='<p style=opacity:0.6>No orders yet.</p>';}
 else{
  let html='<table><tr><th>ID</th><th>Job</th><th>Total</th></tr>';
  orders.slice().reverse().forEach(o=>{html+='<tr onclick=receiptById("'+o.id+'")><td>'+o.id+'</td><td>'+o.job.substring(0,18)+(o.rush?' 🔥':'')+'</td><td>N$ '+o.tot.toFixed(0)+'</td></tr>';});
  html+='</table>'; document.getElementById('list').innerHTML=html;
 }
 let c=document.getElementById('gantt'), ctx=c.getContext('2d');
 ctx.clearRect(0,0,c.width,c.height); ctx.fillStyle='#12151E'; ctx.fillRect(0,0,c.width,c.height);
 let x=10;
 orders.forEach((o,i)=>{
  let w=Math.max(o.dh*12, 40);
  ctx.fillStyle=o.rush?'#FF3B30':'#FF6A00'; ctx.fillRect(x, i*32+10, w, 22);
  ctx.fillStyle='white'; ctx.font='11px Arial'; ctx.fillText(o.id+' '+o.dh.toFixed(1)+'h', x+4, i*32+24);
  x+=w+8; if(x>c.width-80){x=10;}
 });
}
function receipt(o){
 let wrap=document.getElementById('receiptWrap');
 wrap.innerHTML='<div class="glass"><div class="receipt-box"><b>'+o.id+'</b> - '+o.time+'<br><br>Customer: '+o.cname+'<br>Job: '+o.job+' x'+o.qty+'<br><br>Total: <b>N$ '+o.tot.toFixed(2)+'</b><br>Base N$ '+o.base.toFixed(0)+' + Rush N$ '+o.extra.toFixed(0)+' + Buffer N$ '+o.buff.toFixed(0)+'<br><br><button onclick=window.print()>📥 Print / Save PDF</button></div></div>';
}
function receiptById(id){ let o=orders.find(x=>x.id==id); if(o) receipt(o); }
function clearAll(){ if(confirm('Clear all?')){ orders=[]; save(); draw(); document.getElementById('receiptWrap').innerHTML=''; } }
draw();
</script>
</body>
</html>