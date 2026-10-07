const toggle=document.querySelector('.menu-toggle');
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));document.querySelector('nav').classList.toggle('open',open);});
const search=document.querySelector('#paper-search');
if(search){const topic=document.querySelector('#topic-filter'),year=document.querySelector('#year-filter'),papers=[...document.querySelectorAll('.paper')];const filter=()=>{let count=0;for(const p of papers){const show=p.textContent.toLowerCase().includes(search.value.trim().toLowerCase())&&(!topic.value||p.dataset.topics.split('|').includes(topic.value))&&(!year.value||p.dataset.year===year.value);p.hidden=!show;if(show)count++;}document.querySelector('#result-count').textContent=`${count} publication${count===1?'':'s'}`;document.querySelector('.empty').hidden=count!==0;};[search,topic,year].forEach(el=>el.addEventListener('input',filter));filter();}
// Omitted illustration files have a calm placeholder until local assets are restored.
document.querySelectorAll('.prose img').forEach(img=>{img.addEventListener('error',()=>{const placeholder=document.createElement('div');placeholder.className='image-placeholder';placeholder.textContent=img.alt||'Research illustration';img.replaceWith(placeholder);});});

document.querySelectorAll('.paper-illustration').forEach(img=>img.addEventListener('error',()=>img.hidden=true));
