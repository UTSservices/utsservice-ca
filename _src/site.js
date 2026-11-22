(()=>{
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1,rootMargin:'0px 0px -5% 0px'});
$$('.reveal').forEach(el=>io.observe(el));
if(matchMedia('(prefers-reduced-motion: reduce)').matches)$$('.reveal').forEach(el=>el.classList.add('in'));
/* menu */
const mbtn=$('#menu-btn'),mnav=$('#mnav');
const setMenu=o=>{mnav.classList.toggle('open',o);mbtn.setAttribute('aria-expanded',o?'true':'false')};
mbtn.addEventListener('click',()=>setMenu(!mnav.classList.contains('open')));
mnav.addEventListener('click',e=>{if(e.target.tagName==='A')setMenu(false)});
addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
/* sticky call bar hides while the request block is on screen */
const sticky=$('.sticky-call'),req=$('#request');
if(sticky&&req)new IntersectionObserver(es=>sticky.classList.toggle('hide',es[0].isIntersecting),{rootMargin:'0px 0px -15% 0px'}).observe(req);
document.addEventListener('visibilitychange',()=>document.body.classList.toggle('paused',document.hidden));
})();
