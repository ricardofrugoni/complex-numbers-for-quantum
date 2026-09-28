// Run with: node tests/check_web_lab.cjs (Node.js 18+).
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/web/lab.js'), 'utf8').split('const $ =')[0];
const checks = String.raw`
function assert(condition, message) { if (!condition) throw new Error(message); }
function near(a,b) { return Math.abs(a-b)<1e-10; }
assert(multiply([1,1],[0,1]).every((x,i)=>near(x,[-1,1][i])), 'Multiplication by i');
for (const [p,phi,expected] of [[1,0,[0,0,1]],[0,0,[0,0,-1]],[.5,0,[1,0,0]],[.5,90,[0,1,0]],[.5,180,[-1,0,0]],[.5,-90,[0,-1,0]]]) {
    const state=blochState(p,radians(phi),0);
    assert(state.vector.every((v,i)=>near(v,expected[i])), 'Bloch axis '+phi);
    assert((state.relativePhase===null)===(p===0||p===1), 'Pole phase');
}
for (const p of [0,.01,.25,.5,.73,.99,1]) {
    const before=blochState(p,.37,0),after=blochState(p,.37,.91);
    assert(near(Math.hypot(...before.vector),1), 'Unit Bloch vector');
    assert(near(Math.hypot(...before.alpha)**2+Math.hypot(...before.beta)**2,1), 'Normalized amplitudes');
    assert(before.vector.every((v,i)=>near(v,after.vector[i])), 'Global phase invariance');
}
let rejected=0;
for (const args of [[-1,0,0],[2,0,0],[.5,NaN,0],[.5,0,Infinity]]) {
    try { blochState(...args); } catch(error) { rejected++; }
}
assert(rejected===4, 'Invalid state validation');
for(const [mode,lesson] of Object.entries(lessons)) for(const edge of [2,3,4]) {
    const state=Object.fromEntries(lesson.controls.map(c=>[c[0],c[edge]]));
    const f=figure(mode,state);
    assert((mode==='bloch'?f.data.length===0&&near(Math.hypot(...f.bloch.vector),1):f.data.length>0) && f.metrics.length===3, 'Figure '+mode);
    for(const trace of f.data) {
        assert(trace.x.length===trace.y.length, 'Coordinate lengths '+mode);
        assert([...trace.x,...trace.y,...(trace.z||[])].every(Number.isFinite), 'Finite coordinates '+mode);
    }
}
const f=figure('multiplicacao',{scale:0,angle:37});
assert(f.data.at(-1).x.every(x=>near(x,0)) && f.data.at(-1).y.every(y=>near(y,0)), 'Zero scale');
`;
vm.runInNewContext(source + '\n' + checks, {
    LAB_THEME:{colorway:['#365ddd','#c15d2c','#087e8b','#a7b4c8']}, structuredClone,
});
console.log('Web lab: all math and figure checks passed.');
