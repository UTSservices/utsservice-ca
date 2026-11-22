
(()=>{
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const smooth=(p,e0,e1)=>{const t=clamp((p-e0)/(e1-e0),0,1);return t*t*(3-2*t)};
const RM=matchMedia('(prefers-reduced-motion: reduce)');

/* clients marquee */
const L=[['tim-hortons','Tim Hortons'],['amazon','Amazon'],['rbc','RBC Royal Bank'],['opp','Ontario Provincial Police'],['city-of-toronto','City of Toronto'],['eaton-centre','CF Toronto Eaton Centre'],['louis-vuitton','Louis Vuitton'],['mercedes-benz','Mercedes-Benz'],['canada-post','Canada Post'],['ups','UPS'],['wework','WeWork'],['smartcentres','SmartCentres'],['dominos',"Domino's Pizza"],['pizza-pizza','Pizza Pizza'],['fred-victor','Fred Victor']];
const cell=([f,n],hide)=>`<div class="logo-cell"${hide?' aria-hidden="true"':''}><img src="assets/clients/${f}.png" alt="${hide?'':n}" loading="lazy" width="360" height="140"></div>`;
const half=a=>a.map(x=>cell(x)).join('')+a.map(x=>cell(x,1)).join('');
$('#trackA').innerHTML=half(L.slice(0,8).concat(L.slice(0,8)));
$('#trackB').innerHTML=half(L.slice(8).concat(L.slice(8)));

/* split text */
function rng(seed){let s=seed>>>0;return()=>(s=(s*1664525+1013904223)>>>0)/4294967296}
$$('.split').forEach((el,ei)=>{
  const txt=el.textContent.trim(), r=rng(7+ei*31), fx=el.dataset.fx;
  const words=txt.split(' ');
  const vis=words.map((w,i)=>{
    const th=(i/words.length)*0.5+r()*0.04;
    const jx=fx==='part'?(i%2?1:-1)*(24+r()*30):0;
    return `<span class="w" style="--th:${th.toFixed(3)};--jx:${jx.toFixed(1)}px">${w}</span>`;
  }).join(' ');
  el.innerHTML=`<span class="visually-hidden">${txt}</span><span aria-hidden="true">${vis}</span>`;
});

/* reveals + doors */
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;
  const t=e.target; t.classList.add('in');
  if(t.classList.contains('doorway')||t.classList.contains('box')){
    const host=t.classList.contains('box')?t:t;
    host.classList.add('open');
    const d=host.querySelector(':scope > .doors');
    if(d){d.querySelector('.pane').addEventListener('transitionend',()=>d.classList.add('gone'),{once:true});setTimeout(()=>d.classList.add('gone'),2200)}
  }
  io.unobserve(t);
}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
$$('section.sec, .reveal, .box').forEach(el=>io.observe(el));

/* nav state */
const nav=$('.nav');let navSolid=null;
const sticky=$('.sticky-call');let stickyOn=null,reqIn=false;
new IntersectionObserver(es=>{reqIn=es[0].isIntersecting;navCheck()},{rootMargin:'0px 0px -15% 0px'}).observe($('#request'));
function navCheck(){const s=scrollY>innerHeight*0.6;if(s!==navSolid){navSolid=s;nav.classList.toggle('solid',s)}const o=scrollY>hero.offsetHeight-innerHeight*0.35&&!reqIn;if(o!==stickyOn){stickyOn=o;sticky.classList.toggle('show',o)}}

/* pause loops off-screen / hidden */
document.addEventListener('visibilitychange',()=>document.body.classList.toggle('paused',document.hidden));
const mio=new IntersectionObserver(es=>es.forEach(e=>e.target.classList.toggle('anim-off',!e.isIntersecting)));
mio.observe($('#clients'));

/* ---------- hero scrub ---------- */
const hero=$('#hero'), stage=$('#stage'), video=$('#hero-video'), poster=$('#poster'), ringFill=$('#ring-fill');
const chip=$('#chip'), chipTxt=$('#chip-txt');
const PORTRAIT=matchMedia('(max-width: 720px),(orientation: portrait) and (max-width: 1024px)').matches, TOUCH=matchMedia('(pointer: coarse)').matches;
const VIDEO_URL=PORTRAIT?'assets/hero-scrub-m.mp4':'assets/hero-scrub.mp4', VIDEO_BYTES=PORTRAIT?1061192:5634505, POSTER_URL=PORTRAIT?'assets/hero-poster-m.jpg':'assets/hero-poster.jpg';
const railEl=$('#rail');let railP=-1;
const bands=$$('.band').map(el=>({el,a:+el.dataset.a,b:+el.dataset.b,op:-1,k:-1,live:null}));
const GATES=['(orientation: landscape) and (pointer: coarse) and (max-height: 560px)','(prefers-reduced-motion: reduce)'];
let forceStatic=!!(navigator.connection&&navigator.connection.saveData);
const MQLS=GATES.map(q=>matchMedia(q));
let scrubOn=false, inited=false, heroOnScreen=true, target=0, shown=0, rafId=null, lastTick=0, loadK=0, loadStart=0, chipOn=null;
let seekBusy=false, pendingTime=null;

function heroProgress(){const r=hero.getBoundingClientRect();const span=hero.offsetHeight-stage.offsetHeight;return span>0?clamp(-r.top/span,0,1):0}
function requestSeek(t){if(!video.duration||!isFinite(t))return;if(seekBusy){pendingTime=t;return}seekBusy=true;video.currentTime=Math.min(t,video.duration-0.04)}
video.addEventListener('seeked',()=>{seekBusy=false;if(pendingTime!==null){const t=pendingTime;pendingTime=null;requestSeek(t)}});
video.addEventListener('error',()=>{seekBusy=false;pendingTime=null;failVideo()});

function updateCaptions(p){
  bands.forEach((B,i)=>{
    const f=0.045, last=i===bands.length-1, first=i===0;
    let op=(first?1:smooth(p,B.a,B.a+f))*(last?1:1-smooth(p,B.b-f,B.b));
    if(p<B.a-0.001&&!first)op=0;
    let k=clamp((p-B.a)/0.07,0,1);
    if(first)k=Math.max(k,loadK);
    op=Math.round(op*1000)/1000;
    if(Math.abs(op-B.op)>0.004||(op===0)!==(B.op===0)){B.op=op;B.el.style.opacity=op}
    if(Math.abs(k-B.k)>0.008||(k===1&&B.k!==1)){B.k=k;B.el.style.setProperty('--k',k.toFixed(3))}
    const live=op>0.5;if(live!==B.live){B.live=live;B.el.classList.toggle('live',live)}
  });
  if(Math.abs(p-railP)>0.002){railP=p;railEl.style.transform='scaleX('+p.toFixed(3)+')'}
  const on=p>0.43;
  if(on!==chipOn){chipOn=on;chip.classList.toggle('on',on);chipTxt.textContent=on?'Entrance 01 · Access granted':'Entrance 01 · Standby'}
}
function tick(now){
  const dt=Math.min(100,now-(lastTick||now));lastTick=now;
  shown+=(target-shown)*(1-Math.pow(1-0.16,dt/16.667));
  let busy=Math.abs(target-shown)>=0.0005;
  if(!busy)shown=target;
  if(loadK<1){loadK=clamp((now-loadStart)/1300,0,1);loadK=1-Math.pow(1-loadK,3);busy=true}
  requestSeek(shown*(video.duration||0));
  updateCaptions(shown);
  if(busy&&scrubOn)rafId=requestAnimationFrame(tick);else{rafId=null;lastTick=0}
}
function kick(){if(rafId===null&&heroOnScreen&&scrubOn)rafId=requestAnimationFrame(tick)}
function onScroll(){target=heroProgress();kick()}

let started=false;
function initHeroOnce(){
  if(inited)return;inited=true;
  poster.style.backgroundImage="url('"+POSTER_URL+"')";
  const img=new Image();img.onload=startBlobFetch;img.onerror=startBlobFetch;img.src=POSTER_URL;
  setTimeout(startBlobFetch,4000);
}
function startBlobFetch(){if(started)return;started=true;loadHeroBlob().catch(failVideo)}
async function loadHeroBlob(){
  const ctrl=new AbortController();let wd=setTimeout(()=>ctrl.abort(),20000);
  const res=await fetch(VIDEO_URL,{priority:'low',signal:ctrl.signal});
  if(!res.ok||!res.body)throw new Error('video');
  const total=Number(res.headers.get('Content-Length'))||VIDEO_BYTES;
  const reader=res.body.getReader();const chunks=[];let got=0,last=0;
  for(;;){
    const {done,value}=await reader.read();if(done)break;
    clearTimeout(wd);wd=setTimeout(()=>ctrl.abort(),20000);
    chunks.push(value);got+=value.length;
    const fr=Math.min(1,got/total),now=performance.now();
    if(now-last>100||fr===1){last=now;ringFill.style.setProperty('--ld',Math.round(126*(1-fr)))}
  }
  clearTimeout(wd);ringFill.style.setProperty('--ld',0);
  video.preload='auto';video.src=URL.createObjectURL(new Blob(chunks,{type:'video/mp4'}));video.load();
  const go=()=>{requestSeek(heroProgress()*video.duration);stage.classList.add('video-ready');kick()};
  if(!TOUCH){video.addEventListener('canplay',go,{once:true});return}
  /* phones only paint video frames once playback has started: start muted, pause, then scrub. If the phone refuses (Low Power Mode), fall back to the still hero. */
  video.muted=true;let done=false;
  const ok=()=>{if(done)return;done=true;clearTimeout(bail);video.pause();go()};
  const no=()=>{if(done)return;done=true;clearTimeout(bail);forceStatic=true;applyHeroMode()};
  const bail=setTimeout(no,7000);
  const pr=video.play();
  if(pr&&pr.then)pr.then(ok).catch(no);else video.addEventListener('canplay',ok,{once:true});
}
function failVideo(){stage.classList.add('video-failed')}

function enableScrub(){
  if(scrubOn)return;scrubOn=true;
  initHeroOnce();
  addEventListener('scroll',onScroll,{passive:true});
  bands.forEach(b=>{b.op=-1;b.k=-1;b.live=null});chipOn=null;
  if(!loadStart)loadStart=performance.now();
  target=shown=heroProgress();updateCaptions(shown);onScroll();
}
function disableScrub(){
  if(!scrubOn)return;scrubOn=false;
  removeEventListener('scroll',onScroll);
  if(rafId!==null){cancelAnimationFrame(rafId);rafId=null}
}
function applyHeroMode(){const st=forceStatic||MQLS.some(m=>m.matches);document.documentElement.classList.toggle('hs',st);if(st)disableScrub();else enableScrub()}
MQLS.forEach(m=>m.addEventListener('change',applyHeroMode));
new IntersectionObserver(es=>{heroOnScreen=es[0].isIntersecting;if(heroOnScreen)kick()}).observe(hero);
applyHeroMode();
addEventListener('scroll',navCheck,{passive:true});navCheck();

/* ---------- fob hold interaction ---------- */
const zone=$('#fobzone'), rd=$('#reader'), lbl=$('#hold-label');
let h=0, holding=false, granted=false, hraf=null, hlast=0;
function setH(v){h=v;zone.style.setProperty('--h',v.toFixed(3))}
function hstep(now){
  const dt=Math.min(64,now-(hlast||now));hlast=now;
  if(holding)setH(Math.min(1,h+dt/1400));else setH(Math.max(0,h-dt/700*(0.4+h)));
  if(h>=1&&!granted){grant();return}
  if(holding||h>0)hraf=requestAnimationFrame(hstep);else{hraf=null;hlast=0}
}
function grant(){granted=true;holding=false;hraf=null;setH(1);zone.classList.add('granted');lbl.textContent='Access granted';rd.setAttribute('aria-label','Access granted')}
function start(e){if(granted)return;if(e)e.preventDefault();holding=true;if(!hraf)hraf=requestAnimationFrame(hstep)}
function stop(){holding=false}
rd.addEventListener('pointerdown',e=>{rd.setPointerCapture?.(e.pointerId);start(e)});
['pointerup','pointercancel','lostpointercapture'].forEach(t=>rd.addEventListener(t,stop));
rd.addEventListener('keydown',e=>{if((e.key===' '||e.key==='Enter')&&!e.repeat)start(e)});
rd.addEventListener('keyup',e=>{if(e.key===' '||e.key==='Enter')stop()});
rd.addEventListener('contextmenu',e=>e.preventDefault());

/* ---------- menu + active nav ---------- */
const mbtn=$('#menu-btn'), mnav=$('#mnav');
function setMenu(o){mnav.classList.toggle('open',o);mbtn.setAttribute('aria-expanded',o?'true':'false')}
mbtn.addEventListener('click',()=>setMenu(!mnav.classList.contains('open')));
mnav.addEventListener('click',e=>{if(e.target.tagName==='A')setMenu(false)});
addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
const links=new Map($$('.nav ul a').map(a=>[a.getAttribute('href').slice(1),a]));
const aio=new IntersectionObserver(es=>es.forEach(e=>{const a=links.get(e.target.id);if(a)a.classList.toggle('on',e.isIntersecting)}),{rootMargin:'-45% 0px -50% 0px'});
links.forEach((a,id)=>{const el=document.getElementById(id);if(el)aio.observe(el)});

/* reduced motion, live both ways */
function pinToFinalStates(){if(!granted)grant();$$('.doorway,.box').forEach(d=>{d.classList.add('open','in')});$$('.reveal').forEach(r=>r.classList.add('in'))}
function unpinFinalStates(){/* content stays revealed; scroll-driven hero re-arms through applyHeroMode */}
if(RM.matches)pinToFinalStates();
RM.addEventListener('change',e=>{if(e.matches)pinToFinalStates();else{unpinFinalStates();applyHeroMode()}});
})();

/* service request form (Web3Forms) */
(()=>{const f=document.getElementById('reqform');if(!f)return;const st=f.querySelector('[data-status]'),btn=f.querySelector('button[type=submit]'),orig=st.innerHTML;
f.addEventListener('submit',async e=>{e.preventDefault();if(f.botcheck.checked)return;
  const d=new FormData(f);const svc=d.getAll('service');d.delete('service');d.set('services',svc.join(', ')||'Not specified');d.delete('botcheck');
  const n=new Date(),pad=x=>String(x).padStart(2,'0'),ref='UTS-'+pad(n.getMonth()+1)+pad(n.getDate())+'-'+pad(n.getHours())+pad(n.getMinutes())+'-'+Math.random().toString(36).slice(2,4).toUpperCase();
  const who=[d.get('name'),d.get('company')].filter(Boolean).join(', ');
  d.set('subject','Service request '+ref+': '+who+(d.get('urgency')?' ('+d.get('urgency')+')':''));d.set('reference',ref);
  if(!d.get('access_key')){const body=['Name: '+d.get('name'),'Company: '+(d.get('company')||''),'Email: '+d.get('email'),'Phone: '+d.get('phone'),'Address: '+(d.get('address')||''),'Property: '+d.get('property_type'),'Urgency: '+d.get('urgency'),'Services: '+d.get('services'),'','Details:',d.get('message')||''].join('\n');location.href='mailto:Admin@utsservice.ca?subject='+encodeURIComponent(d.get('subject'))+'&body='+encodeURIComponent(body);st.innerHTML='Your email app should open with everything filled in. Press send there. Reference <strong>'+ref+'</strong>.';return}
  btn.disabled=true;btn.textContent='Sending...';f.classList.remove('err');
  try{const r=await fetch(f.action,{method:'POST',headers:{Accept:'application/json'},body:d});const j=await r.json();if(!j.success)throw 0;
    f.classList.add('sent');f.innerHTML='<p class="mono ptitle">Request sent</p><h3 class="sent-h">Thanks, we have it.</h3><p class="pnote">Your reference is <strong>'+ref+'</strong>. We will get back to you the same business day. If it cannot wait, call <a href="tel:+16477777411">647-777-7411</a>.</p>';
  }catch(_){f.classList.add('err');st.innerHTML='That did not go through. Please call <a href="tel:+16477777411">647-777-7411</a> or email <a href="mailto:Admin@utsservice.ca">Admin@utsservice.ca</a>.';btn.disabled=false;btn.textContent='Send request'}
});})();
