var tools = new function() {
    this.loadStats = function() {
        var stats = new Stats();
        stats.domElement.style.cssText = 'position:fixed;right:0;top:0;z-index:10000';
        document.body.appendChild(stats.domElement);
        requestAnimationFrame( function loop() {
            stats.update();
            requestAnimationFrame(loop)
        });
    };
};
