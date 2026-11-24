(()=>{
const D=window.STARLINE||{cars:[],reviews:[],rating:4.9,total:46};
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const eur=n=>'€'+n.toLocaleString('en-IE');
const WA='353857553430', MAIL='starlinemotorssales@gmail.com';
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const avail=D.cars.filter(c=>!c.sold);
const Q=new URLSearchParams(location.search);

/* ---------- intro (home, once per visit) ---------- */
const intro=$('.intro');
if(intro){
  let seen=false;try{seen=sessionStorage.getItem('sl-intro')}catch(e){}
  if(seen||reduce){intro.remove()}
  else{
    document.body.classList.add('lock');
    const done=()=>{if(!intro.isConnected||intro.classList.contains('out'))return;intro.classList.add('out');document.body.classList.remove('lock');try{sessionStorage.setItem('sl-intro','1')}catch(e){}setTimeout(()=>intro.remove(),850)};
    setTimeout(done,2500);$('.sk',intro).onclick=done;
  }
}

/* ---------- nav ---------- */
const bg=$('.burger'),menu=$('#menu');
if(bg){bg.onclick=()=>{const o=menu.classList.toggle('open');bg.setAttribute('aria-expanded',o);document.body.classList.toggle('lock',o)}}
if(menu){menu.addEventListener('click',e=>{if(e.target.closest('a')){menu.classList.remove('open');document.body.classList.remove('lock');bg.setAttribute('aria-expanded',false)}});addEventListener('pageshow',()=>{menu.classList.remove('open');document.body.classList.remove('lock');bg.setAttribute('aria-expanded',false)})}
$$('[data-yr]').forEach(e=>e.textContent=new Date().getFullYear());
$$('[data-n=rating]').forEach(e=>e.textContent=D.rating.toFixed(1));
$$('[data-n=total]').forEach(e=>e.textContent=D.total);
$$('[data-n=stock]').forEach(e=>e.textContent=avail.length);

/* ---------- background videos: pick size, play when visible ---------- */
$$('video[data-src]').forEach(v=>{
  if(reduce||(navigator.connection&&navigator.connection.saveData))return;
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting){
      if(!v.src){v.src=v.dataset.src.replace('.mp4',innerWidth<800?'-m.mp4':'.mp4')}
      const p=v.play();if(p&&p.catch)p.catch(()=>{});
    }else if(v.src){v.pause()}
  }),{threshold:.1});
  io.observe(v);
});

/* ---------- reveal ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -6% 0px'});
const watch=r=>$$('.rvl',r).forEach(e=>io.observe(e));
watch(document);

/* ---------- cars ---------- */
const specs=c=>[c.year,c.fuel,c.trans,c.mileage].filter(Boolean).map(s=>`<span>${esc(s)}</span>`).join('');
const newest=avail.slice(0,3).map(c=>c.id);
const card=(c,i=0)=>`<a class="car rvl${c.sold?' sold':''}" style="--d:${Math.min(i,6)*.05}s" href="car?id=${c.id}">
  <div class="ph">${c.imgs[0]?`<img src="${c.imgs[0].replace('-0.webp','-t.webp')}" alt="${esc(c.title)}" loading="lazy" width="640" height="480">`:''}${c.sold?'<span class="badge">Sold</span>':newest.includes(c.id)?'<span class="badge new">Just in</span>':''}${!c.sold&&c.imgs.length>1?`<span class="pc">${c.imgs.length} photos</span>`:''}</div>
  <div class="bd"><h3>${esc(c.title)}</h3><div class="specs">${specs(c)}</div><div class="ft"><span class="price">${eur(c.price)}</span><span class="go" aria-hidden="true">→</span></div></div></a>`;

const dc=$('#door-car');if(dc&&avail[0]&&avail[0].imgs[0])dc.src=avail[0].imgs[0];
const feat=$('#featured');
if(feat){feat.innerHTML=avail.slice(0,3).map(card).join('');watch(feat)}

const grid=$('#grid');
if(grid){
  const st={q:'',make:Q.get('make')||'All',status:'avail',sort:'new'};
  const makes=['All',...[...new Set(D.cars.map(c=>c.make))].sort()];
  if(!makes.includes(st.make))st.make='All';
  $('#makes').innerHTML=makes.map(m=>`<button type="button" data-make="${esc(m)}" aria-pressed="${m===st.make}">${esc(m)}</button>`).join('');
  const draw=()=>{
    let L=D.cars.filter(c=>(st.status==='all'||(st.status==='sold')===c.sold)&&(st.make==='All'||c.make===st.make)&&(!st.q||(c.title+' '+c.head+' '+c.make).toLowerCase().includes(st.q)));
    const by={new:(a,b)=>b.added.localeCompare(a.added),lo:(a,b)=>a.price-b.price,hi:(a,b)=>b.price-a.price,yr:(a,b)=>(b.year||0)-(a.year||0)}[st.sort];
    L=[...L].sort((a,b)=>(a.sold-b.sold)||by(a,b));
    $('#count').textContent=L.length+(L.length===1?' vehicle':' vehicles')+(st.make!=='All'?' · '+st.make:'');
    grid.innerHTML=L.length?L.map(card).join(''):`<div class="empty">Nothing matches that just now. Stock changes every week, so <a href="contact?type=viewing">tell us what you’re after</a> and we’ll keep an eye out.</div>`;
    watch(grid);
  };
  $('#q').addEventListener('input',e=>{st.q=e.target.value.trim().toLowerCase();draw()});
  $('#sort').addEventListener('change',e=>{st.sort=e.target.value;draw()});
  $('#makes').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;st.make=b.dataset.make;$$('#makes button').forEach(x=>x.setAttribute('aria-pressed',x===b));draw()});
  $$('.seg button').forEach(b=>b.addEventListener('click',()=>{st.status=b.dataset.st;$$('.seg button').forEach(x=>x.setAttribute('aria-pressed',x===b));draw()}));
  draw();
}

/* ---------- single car page ---------- */
const det=$('#detail');
if(det){
  const c=D.cars.find(x=>x.id===Q.get('id'));
  if(!c){det.innerHTML=`<div class="empty">We couldn’t find that car. It may have been sold. <a href="cars">See everything in stock</a>.</div>`}
  else{
    document.title=`${c.title} · ${eur(c.price)} | Starline Motors`;
    let ix=0;
    const msg=encodeURIComponent(`Hi Starline Motors, I'm interested in the ${c.title} (${eur(c.price)}). Is it still available?`);
    const book='contact?type=viewing&car='+encodeURIComponent(c.title);
    det.innerHTML=`<p class="crumb"><a href="cars">← All cars</a> &nbsp;/&nbsp; ${esc(c.make)}</p>
    <div class="detail">
      <div class="gal">
        <div class="main"><img id="m-img" alt="" width="1200" height="900">${c.imgs.length>1?'<button class="arr p" aria-label="Previous photo">‹</button><button class="arr n" aria-label="Next photo">›</button><span class="n-of" id="n-of"></span>':''}${c.sold?'<span class="badge">Sold</span>':''}</div>
        ${c.imgs.length>1?`<div class="thumbs">${c.imgs.map((s,k)=>`<button type="button" data-k="${k}" aria-label="Photo ${k+1}"><img src="${s}" alt="" loading="lazy"></button>`).join('')}</div>`:''}
      </div>
      <div class="info">
        <div class="specs">${specs(c)}</div>
        <h1>${esc(c.title)}</h1><div class="sub">${esc(c.head)}</div>
        <span class="price"${c.sold?' style="color:#aaa;text-decoration:line-through"':''}>${eur(c.price)}</span>
        <div class="acts">${c.sold?`<a class="btn btn-red" href="contact?type=viewing">Find me one like it <span class="ar">→</span></a>`:`<a class="btn btn-red" href="${book}">Book a viewing <span class="ar">→</span></a><a class="btn btn-wa" href="https://wa.me/${WA}?text=${msg}" target="_blank" rel="noopener">WhatsApp</a><a class="btn btn-out" href="tel:+353852258335">Call sales</a>`}</div>
        ${c.sold?'<p><strong>This one has found a new home.</strong> Tell us what you liked about it and we’ll look out for the next one.</p>':''}
        ${c.intro.map(p=>`<p>${esc(p)}</p>`).join('')}
        <p class="note">Viewing by appointment on Greenhills Road, Dublin 12. Sales team available 9am to 7pm on 085 225 8335.</p>
      </div>
    </div>
    ${c.feats.length?`<h2 class="spec-h">Spec &amp; details</h2><ul class="feats">${c.feats.map(f=>`<li>${esc(f)}</li>`).join('')}</ul>`:''}`;
    const show=i=>{ix=(i+c.imgs.length)%c.imgs.length;const im=$('#m-img');im.src=c.imgs[ix];im.alt=c.title+' photo '+(ix+1);$$('.thumbs button').forEach((b,k)=>b.setAttribute('aria-current',k===ix));const n=$('#n-of');if(n)n.textContent=(ix+1)+' / '+c.imgs.length};
    if(c.imgs.length){show(0)}
    const th=$('.thumbs');if(th)th.addEventListener('click',e=>{const b=e.target.closest('button');if(b)show(+b.dataset.k)});
    const p=$('.arr.p'),n=$('.arr.n');if(p){p.onclick=()=>show(ix-1);n.onclick=()=>show(ix+1)}
    document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(ix-1);if(e.key==='ArrowRight')show(ix+1)});
    let tx=0;const m=$('.gal .main');
    m.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});
    m.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>40)show(ix+(d<0?1:-1))});
    const more=$('#more');
    if(more){more.innerHTML=avail.filter(x=>x.id!==c.id).sort((a,b)=>Math.abs(a.price-c.price)-Math.abs(b.price-c.price)).slice(0,3).map(card).join('');watch(more)}
  }
}

/* ---------- contact form ---------- */
const f=$('#form');
if(f){
  f.car.innerHTML='<option value="">Any / not sure yet</option>'+avail.map(c=>`<option value="${esc(c.title)}">${esc(c.title)} · ${eur(c.price)}</option>`).join('');
  f.day.min=new Date().toISOString().slice(0,10);
  const mode=()=>{const t=f.type.value;$('#l-svc').hidden=t!=='service';$('#l-reg').hidden=t!=='service';$('#l-car').hidden=t!=='viewing'};
  if(['service','viewing','general'].includes(Q.get('type')))f.type.value=Q.get('type');
  if(Q.get('service'))f.service.value=Q.get('service');
  if(Q.get('car'))f.car.value=Q.get('car');
  f.addEventListener('change',mode);mode();
  f.addEventListener('submit',e=>{
    e.preventDefault();
    const via=(e.submitter&&e.submitter.dataset.via)||'wa', t=f.type.value, hint=$('#hint');
    if(!f.name.value.trim()||!f.phone.value.trim()){hint.textContent='Please add your name and phone number so we can get back to you.';hint.style.color='var(--red)';(f.name.value.trim()?f.phone:f.name).focus();return}
    const head={service:'Service / repair booking',viewing:'Viewing / test drive request',general:'General enquiry'}[t];
    const L=[head,'','Name: '+f.name.value.trim(),'Phone: '+f.phone.value.trim()];
    if(f.email.value.trim())L.push('Email: '+f.email.value.trim());
    if(t==='service'){if(f.service.value)L.push('Service: '+f.service.value);if(f.vehicle.value.trim())L.push('Vehicle: '+f.vehicle.value.trim())}
    if(t==='viewing'&&f.car.value)L.push('Car: '+f.car.value);
    if(f.day.value)L.push('Preferred day: '+new Date(f.day.value+'T12:00').toLocaleDateString('en-IE',{weekday:'long',day:'numeric',month:'long'}));
    if(f.msg.value.trim())L.push('','Message: '+f.msg.value.trim());
    const body=L.join('\n');
    hint.style.color='';hint.textContent=via==='wa'?'Opening WhatsApp with your message. Just press send there.':'Opening your email app with your message. Just press send there.';
    const url=via==='wa'?`https://wa.me/${WA}?text=${encodeURIComponent(body)}`:`mailto:${MAIL}?subject=${encodeURIComponent(head+' from '+f.name.value.trim())}&body=${encodeURIComponent(body)}`;
    if(via==='wa')window.open(url,'_blank','noopener');else location.href=url;
  });
}
})();
