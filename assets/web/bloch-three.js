import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export async function createBloch(container) {
    await document.fonts.ready;
    const scene=new THREE.Scene();
    const camera=new THREE.PerspectiveCamera(38,1,.1,30);
    camera.up.set(0,0,1);
    camera.position.set(2.1,-2.9,1.7);
    const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
    renderer.setClearColor(0x000000,0);
    container.appendChild(renderer.domElement);
    const controls=new OrbitControls(camera,renderer.domElement);
    controls.enablePan=false;controls.minDistance=2.8;controls.maxDistance=7;
    controls.target.set(0,0,0);controls.update();controls.saveState();
    const draw=()=>{if(!container.hidden)renderer.render(scene,camera);};
    controls.addEventListener('change',draw);

    function curve(points,color,opacity=.3) {
        const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),
            new THREE.LineBasicMaterial({color,transparent:true,opacity}));
        scene.add(line);return line;
    }
    const pointsAt=(f,n=160)=>Array.from({length:n+1},(_,i)=>new THREE.Vector3(...f(i/n*2*Math.PI)));
    const surface=new THREE.Mesh(new THREE.SphereGeometry(.998,64,48),
        new THREE.MeshBasicMaterial({color:0x11214b,transparent:true,opacity:.17,depthWrite:false}));
    scene.add(surface);
    for(let j=1;j<8;j++) {
        const t=j*Math.PI/8;
        curve(pointsAt(a=>[Math.sin(t)*Math.cos(a),Math.sin(t)*Math.sin(a),Math.cos(t)]),0x6599ce,.14);
    }
    for(let j=0;j<8;j++) {
        const p=j*Math.PI/8;
        curve(pointsAt(t=>[Math.sin(t)*Math.cos(p),Math.sin(t)*Math.sin(p),Math.cos(t)]),0x6599ce,.14);
    }
    curve(pointsAt(a=>[Math.cos(a),Math.sin(a),0]),0x7acddd,.55);
    for(const d of [[1,0,0],[0,1,0],[0,0,1]]) curve([
        new THREE.Vector3(...d).multiplyScalar(-1.12),new THREE.Vector3(...d).multiplyScalar(1.12)],0x6b829e,.35);

    // Pontos uniformes na superfície: textura discreta, sem dados fictícios.
    const positions=[];
    for(let i=0;i<1800;i++) {
        const z=1-2*(i+.5)/1800,r=Math.sqrt(1-z*z),a=i*Math.PI*(3-Math.sqrt(5));
        positions.push(r*Math.cos(a),r*Math.sin(a),z);
    }
    const dots=new THREE.BufferGeometry();dots.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    scene.add(new THREE.Points(dots,new THREE.PointsMaterial({color:0xaacdf2,size:.009,transparent:true,opacity:.38,depthWrite:false})));

    function label(text,position,color='#afc5df') {
        const canvas=document.createElement('canvas');canvas.width=256;canvas.height=80;
        const ctx=canvas.getContext('2d');ctx.font='500 40px Montserrat';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=color;ctx.fillText(text,128,40);
        const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(canvas),transparent:true,depthTest:false}));
        sprite.position.set(...position);sprite.scale.set(.64,.2,1);scene.add(sprite);
    }
    label('|0⟩',[0,0,1.2]);label('|1⟩',[0,0,-1.2]);
    label('x',[1.22,0,0]);label('y',[0,1.22,0]);
    const arrow=new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(),1,0xf393cd,.12,.055);
    scene.add(arrow);
    const tip=new THREE.Mesh(new THREE.SphereGeometry(.024,16,12),new THREE.MeshBasicMaterial({color:0xffe8f7}));
    scene.add(tip);
    const glowCanvas=document.createElement('canvas');glowCanvas.width=glowCanvas.height=128;
    const ctx=glowCanvas.getContext('2d'),gradient=ctx.createRadialGradient(64,64,0,64,64,64);
    gradient.addColorStop(0,'rgba(255,158,218,.7)');gradient.addColorStop(.18,'rgba(245,117,193,.35)');gradient.addColorStop(1,'rgba(245,117,193,0)');
    ctx.fillStyle=gradient;ctx.fillRect(0,0,128,128);
    const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(glowCanvas),transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));
    glow.scale.set(.26,.26,1);scene.add(glow);
    const latitude=curve(pointsAt(a=>[Math.cos(a),Math.sin(a),0]),0xd583bb,.5);
    function resize(){const w=container.clientWidth,h=container.clientHeight;if(!w||!h)return;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();draw();}
    const observer=new ResizeObserver(resize);observer.observe(container);resize();
    container.addEventListener('keydown',event=>{
        if(event.key==='Home'){controls.reset();event.preventDefault();}
    });
    renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();container.dataset.error='Contexto 3D interrompido. Recarregue a página.';});
    return {
        update(vector){const direction=new THREE.Vector3(...vector);arrow.setDirection(direction.clone().normalize());tip.position.copy(direction);glow.position.copy(direction);
            const radius=Math.hypot(vector[0],vector[1]);latitude.scale.set(radius,radius,1);latitude.position.z=vector[2];latitude.visible=radius>1e-8;resize();},
        reset(){controls.reset();draw();},
    };
}
