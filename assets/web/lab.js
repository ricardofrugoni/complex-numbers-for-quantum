/* Geometria calculada no navegador; o HTML exportado inclui o Plotly. */
const TAU = 2 * Math.PI;
const radians = degrees => degrees * Math.PI / 180;
const polar = (r, t) => [r * Math.cos(t), r * Math.sin(t)];
const multiply = ([a, b], [c, d]) => [a*c - b*d, a*d + b*c];
const samples = (end = TAU, n = 121) => Array.from({length:n}, (_, i) => end*i/(n-1));
const [BLUE, ORANGE, TEAL, GRAY] = LAB_THEME.colorway;
const format = (x, digits = 2) => (Math.abs(x) < 1e-10 ? 0 : x).toFixed(digits);
const complexText = ([a,b]) => `${format(a)} ${b < -1e-10 ? '−' : '+'} ${format(Math.abs(b))}i`;

function blochState(p, phi, chi) {
    if (![p, phi, chi].every(Number.isFinite) || p < 0 || p > 1) throw new RangeError('Estado inválido');
    const alpha = polar(Math.sqrt(p), chi), beta = polar(Math.sqrt(1-p), chi+phi);
    const transverse = 2*Math.sqrt(p*(1-p));
    return {alpha, beta, vector:[transverse*Math.cos(phi), transverse*Math.sin(phi), 2*p-1],
        relativePhase:p === 0 || p === 1 ? null : phi};
}

const lessons = {
    plano: {chapter:'01 / COORDENADAS', title:'Um ponto. Duas componentes.',
        description:'Mova as partes real e imaginária. O vetor muda de direção e de comprimento.',
        formula:String.raw`\(z=a+bi,\quad |z|=\sqrt{a^2+b^2}\)`,
        controls:[['a','Parte real · a',-3,3,1.5,.1,''],['b','Parte imaginária · b',-3,3,1,.1,'']],
        label:'Plano complexo & reflexão', animate:'b',
        challengeTitle:'O que acontece quando a parte imaginária troca de sinal?',
        challenge:'Compare b = 1 e b = −1. O ponto se reflete no eixo real, mas a distância até a origem é a mesma.',
        interpretation:'O vetor azul representa z. O laranja tracejado representa seu conjugado. O círculo reúne pontos de mesmo módulo.',
        observation:'Na origem, o módulo é zero e o argumento não está definido.'},
    multiplicacao: {chapter:'02 / TRANSFORMAÇÕES', title:'Multiplicar é transformar.',
        description:'Uma única multiplicação gira e redimensiona todos os pontos de uma grade.',
        formula:String.raw`\(w=\rho e^{i\theta},\quad z\mapsto wz\)`,
        controls:[['scale','Escala · ρ',0,2,1,.05,'×'],['angle','Rotação · θ',-180,180,45,1,'°']],
        label:'Grade original → grade transformada', animate:'angle',
        challengeTitle:'Transforme uma multiplicação por i em um movimento.',
        challenge:'Escolha escala 1 e rotação 90°. Depois experimente 180° e 360° (ou 0°). Observe a direção do vetor e as distâncias entre os pontos.',
        interpretation:'Os dois planos usam a mesma escala. O vetor de referência é z = 1 + i. A grade laranja mostra a ação de w sobre todo o plano.',
        observation:'Com escala 1, a rotação preserva distâncias. Com escala 0, a grade inteira colapsa na origem.'},
    euler: {chapter:'03 / MAGNITUDE & FASE', title:'Uma volta. Duas ondas.',
        description:'Acompanhe as projeções de um vetor que percorre o círculo no plano complexo.',
        formula:String.raw`\(re^{i\theta}=r\cos\theta+ir\sin\theta\)`,
        controls:[['radius','Módulo · r',0,2,1,.05,''],['angle','Fase · θ',0,360,60,1,'°']],
        label:'Círculo complexo & suas projeções', animate:'angle',
        challengeTitle:'Encontre os momentos em que uma componente desaparece.',
        challenge:'Use 0°, 90°, 180° e 270°. A parte real e a parte imaginária se alternam nos eixos. Depois anime uma volta completa.',
        interpretation:'O azul é a componente real; o laranja tracejado é a imaginária. O eixo horizontal do segundo painel é o ângulo, não uma nova componente complexa.',
        observation:'O módulo permanece constante durante a volta. Se r = 0, não existe uma fase definida para z.'},
    bloch: {chapter:'04 / UM QUBIT', title:'Esfera de Bloch.',
        description:'Arraste para explorar.',
        formula:String.raw`\(|\psi\rangle=\alpha|0\rangle+\beta|1\rangle\)`,
        controls:[['p','Probabilidade · P(0)',0,1,.75,.01,''],['phi','Fase relativa · φ',-180,180,60,1,'°'],['chi','Fase global · χ',-180,180,0,1,'°']],
        label:'Estado puro · vetor unitário', animate:'phi',
        challengeTitle:'Gire as amplitudes sem mover o estado quântico.',
        challenge:'Mude somente a fase global χ. As duas amplitudes giram juntas; o vetor de Bloch fica imóvel. Depois mude a fase relativa φ e compare.',
        interpretation:String.raw`\(\mathbf r=(2\Re(\alpha^*\beta),\,2\Im(\alpha^*\beta),\,|\alpha|^2-|\beta|^2)\). O vetor real representa um estado, não um número complexo isolado. Arraste a esfera para girar a câmera.`,
        observation:'‖r‖ = 1 · A fase global não move o estado. Nos polos, a fase relativa é indefinida.'}
};

function line(points, name, color=BLUE, axis='', dashed=false, markers=false) {
    return {type:'scatter', x:points.map(p=>p[0]), y:points.map(p=>p[1]), name,
        xaxis:'x'+axis,yaxis:'y'+axis,mode:markers?'lines+markers':'lines',
        line:{color,width:2.5,dash:dashed?'dash':'solid'},marker:{size:7,color},
        hovertemplate:'Re: %{x:.3f}<br>Im: %{y:.3f}<extra>%{fullData.name}</extra>'};
}
const vector = (z,name,color,axis='',dashed=false) => line([[0,0],z],name,color,axis,dashed,true);
function circle(r,axis='') {
    return {...line(samples().map(t=>polar(r,t)),'Mesmo módulo',GRAY,axis,true),
        line:{color:GRAY,width:1,dash:'dot'},showlegend:false,hoverinfo:'skip'};
}
function axis(title,range,domain) {
    return {title:{text:title,font:{size:11}},range,domain,gridcolor:'#18243a',zerolinecolor:'#425879',
        zerolinewidth:1,showline:false,tickfont:{size:10},fixedrange:true,constrain:'domain'};
}
function layout(mode) {
    const result=structuredClone(LAB_THEME);
    result.uirevision=mode;
    result.xaxis=axis('Parte real',[-3.2,3.2],[0,.44]);
    result.yaxis={...axis('Parte imaginária',[-3.2,3.2],[0,1]),scaleanchor:'x',scaleratio:1};
    result.xaxis2={...axis('Parte real',[-3.2,3.2],[.57,1]),anchor:'y2'};
    result.yaxis2={...axis('Parte imaginária',[-3.2,3.2],[0,1]),anchor:'x2',scaleanchor:'x2',scaleratio:1};
    return result;
}
function figure(mode,s) {
    const l=layout(mode); let data=[],metrics=[];
    if (mode==='plano') {
        const z=[s.a,s.b],r=Math.hypot(...z);
        l.xaxis.domain=[0,1];delete l.xaxis2;delete l.yaxis2;
        l.xaxis.range=l.yaxis.range=[-4.5,4.5];
        data=[circle(r),vector(z,'z',BLUE),vector([s.a,-s.b],'Conjugado',ORANGE,'',true),
            {...line([[s.a,0],z,[0,s.b]],'Projeções',GRAY,'',true),showlegend:false}];
        metrics=[['Número complexo',complexText(z)],['Módulo |z|',format(r)],['Argumento',r?format(Math.atan2(s.b,s.a)*180/Math.PI,1)+'°':'Indefinido']];
    } else if (mode==='multiplicacao') {
        const w=polar(s.scale,radians(s.angle)),z=[1,1],product=multiply(w,z);
        l.xaxis.range=l.yaxis.range=l.xaxis2.range=l.yaxis2.range=[-6,6];
        for(let k=-2;k<=2;k++) for(const points of [[[k,-2],[k,2]],[[-2,k],[2,k]]]) {
            data.push({...line(points,'Grade original',GRAY),line:{color:'#c9d3e1',width:1},showlegend:false,hoverinfo:'skip'});
            data.push({...line(points.map(p=>multiply(w,p)),'Grade transformada',ORANGE,'2'),line:{color:ORANGE,width:1},showlegend:false,hoverinfo:'skip'});
        }
        data.push(vector(z,'z = 1 + i',BLUE),vector(product,'wz',ORANGE,'2'));
        metrics=[['Multiplicador w',complexText(w)],['Resultado wz',complexText(product)],['Módulo |wz|',format(Math.hypot(...product))]];
    } else if(mode==='euler') {
        const t=radians(s.angle),z=polar(s.radius,t),angles=samples();
        l.xaxis.range=l.yaxis.range=[-2.4,2.4];
        l.xaxis2={...axis('θ (graus)',[0,360],[.57,1]),anchor:'y2'};
        l.yaxis2={...axis('Componente',[-2.4,2.4],[0,1]),anchor:'x2'};
        data=[circle(s.radius),vector(z,'z',TEAL),
            line(angles.map(a=>[a*180/Math.PI,s.radius*Math.cos(a)]),'Real · cos θ',BLUE,'2'),
            line(angles.map(a=>[a*180/Math.PI,s.radius*Math.sin(a)]),'Imaginária · sen θ',ORANGE,'2',true),
            {...line([[s.angle,-2.4],[s.angle,2.4]],'Fase atual',GRAY,'2',true),showlegend:false},
            {...line([[s.angle,z[0]]],'Real atual',BLUE,'2',false,true),showlegend:false},
            {...line([[s.angle,z[1]]],'Imaginária atual',ORANGE,'2',false,true),showlegend:false}];
        data.slice(2).forEach(trace=>trace.hovertemplate='θ: %{x:.1f}°<br>Componente: %{y:.3f}<extra>%{fullData.name}</extra>');
        metrics=[['Parte real',format(z[0])],['Parte imaginária',format(z[1])],['Módulo |z|',format(s.radius)]];
    } else {
        const state=blochState(s.p,radians(s.phi),radians(s.chi));
        metrics=[['Magnitudes |α| / |β|',`${format(Math.sqrt(s.p))} / ${format(Math.sqrt(1-s.p))}`],
            ['Probabilidades P(0) / P(1)',`${format(s.p)} / ${format(1-s.p)}`],['Fase relativa',state.relativePhase===null?'Indefinida':format(s.phi,0)+'°']];
    }
    return {data,layout:l,metrics,bloch:mode==='bloch'?blochState(s.p,radians(s.phi),radians(s.chi)):null};
}

const $ = id=>document.getElementById(id);
let mode='multiplicacao',state={},timer=null,rendering=false,dirty=false,generation=0,blochView=null;
function stop(){clearInterval(timer);timer=null;$('play').textContent='▶ Animar';$('play').setAttribute('aria-pressed','false');}
async function render(){
    dirty=true;if(rendering)return;rendering=true;
    try {while(dirty){dirty=false;const f=figure(mode,state);
        $('metrics').innerHTML=f.metrics.map(([label,value])=>`<div class="metric"><span>${label}</span><strong>${value}</strong></div>`).join('');
        document.querySelectorAll('#controls input').forEach(input=>{$('value-'+input.id).value=format(state[input.id],input.step<1?2:0)+input.dataset.unit;input.value=state[input.id];});
        $('plot').hidden=mode==='bloch';$('bloch-scene').hidden=mode!=='bloch';
        if(f.bloch){
            if(!blochView){const module=await import(BLOCH_MODULE);blochView=await module.createBloch($('bloch-scene'));}
            blochView.update(f.bloch.vector);
        }else await Plotly.react('plot',f.data,f.layout,{responsive:true,displaylogo:false,displayModeBar:false,scrollZoom:false});
    }} catch(error){stop();$('observation').textContent='Não foi possível desenhar o gráfico: '+error.message;console.error(error);}
    finally{rendering=false;}
}
async function select(){
    stop();const requested=location.hash.slice(1);mode=Object.hasOwn(lessons,requested)?requested:'multiplicacao';
    const lesson=lessons[mode];state=Object.fromEntries(lesson.controls.map(c=>[c[0],c[4]]));
    document.body.classList.toggle('bloch-mode',mode==='bloch');
    document.querySelectorAll('[data-mode]').forEach(a=>{if(a.dataset.mode===mode)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    for(const [id,key] of [['chapter','chapter'],['title','title'],['description','description'],['plot-label','label'],['challenge-title','challengeTitle'],['challenge','challenge'],['observation','observation']])$(id).textContent=lesson[key];
    if(window.MathJax?.typesetClear)MathJax.typesetClear([$('formula'),$('interpretation')]);
    $('formula').innerHTML=lesson.formula;$('interpretation').textContent=lesson.interpretation;
    $('hint').textContent=mode==='bloch'?'Arraste para girar · roda para zoom · Home restaura a câmera.':'Passe o cursor sobre os gráficos para ler as coordenadas.';
    $('plot').setAttribute('aria-label',lesson.label);
    $('controls').innerHTML=lesson.controls.map(([id,label,min,max,value,step,unit])=>`<div class="control"><label for="${id}">${label}<output id="value-${id}" for="${id}"></output></label><input type="range" id="${id}" min="${min}" max="${max}" value="${value}" step="${step}" data-unit="${unit}"></div>`).join('');
    const current=++generation;
    if(window.MathJax?.startup?.promise) await MathJax.startup.promise.then(()=>current===generation&&MathJax.typesetPromise([$('formula'),$('interpretation')]));
    if(current===generation) await render();
}
$('controls').addEventListener('input',event=>{stop();const input=event.target;const value=Number(input.value);if(!Number.isFinite(value))return;state[input.id]=Math.min(Number(input.max),Math.max(Number(input.min),value));render();});
$('play').addEventListener('click',()=>{if(timer){stop();return;}$('play').textContent='Ⅱ Pausar';$('play').setAttribute('aria-pressed','true');
    timer=setInterval(()=>{if(document.hidden||rendering)return;const id=lessons[mode].animate;const [, ,min,max,,step]=lessons[mode].controls.find(c=>c[0]===id);
        state[id]=state[id]+Math.max(step,(max-min)/180);if(state[id]>max)state[id]=min;render();},50);
});
$('reset').addEventListener('click',()=>{stop();if(mode==='bloch'&&blochView)blochView.reset();select();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
window.addEventListener('hashchange',select);
select();
