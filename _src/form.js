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
