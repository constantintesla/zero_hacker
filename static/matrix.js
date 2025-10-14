(function(){
	const canvas = document.getElementById('rain');
	const ctx = canvas.getContext('2d');
	let w, h, columns, drops;

	function resize(){
		w = canvas.width = window.innerWidth;
		h = canvas.height = window.innerHeight;
		columns = Math.floor(w / 16);
		drops = new Array(columns).fill(0).map(()=> Math.random()*h);
	}
	window.addEventListener('resize', resize);
	resize();

	const glyphs = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポ0123456789';
	function tick(){
		ctx.fillStyle = 'rgba(0,0,0,0.08)';
		ctx.fillRect(0,0,w,h);
		ctx.fillStyle = '#00ff95';
		ctx.font = '16px Share Tech Mono, monospace';
		for(let i=0;i<columns;i++){
			const text = glyphs[Math.floor(Math.random()*glyphs.length)];
			ctx.fillText(text, i*16, drops[i]);
			drops[i] += 16 + Math.random()*8;
			if(drops[i] > h){
				drops[i] = Math.random()*-200;
			}
		}
		requestAnimationFrame(tick);
	}
	tick();
})();
