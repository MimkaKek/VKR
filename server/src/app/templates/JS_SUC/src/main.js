let x = "0px";
let y = "0px";
let wd = 500;
let hg = 500;
let king = document.getElementById("king");

let sh = document.getElementById("shadow");
king.onmousemove = () => {
    sh.style.opacity = "20%";
};
king.onmouseout = () => {
    sh.style.opacity = "0";
};
var rect = sh.getBoundingClientRect();
sh.style.width = wd + "px";
sh.style.height = hg + "px";
document.onmousemove = (e) => {
    x = e.clientX - rect.left - wd / 2 + "px";
    y = e.clientY - rect.top - hg / 2 + "px";
};
function loop() {
    sh.style.left = x;
    sh.style.top = y;
    requestAnimationFrame(loop);
}
loop();
