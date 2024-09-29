const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

canvas.style = "position: absolute; top: 0px; left: 0px; right: 0px; bottom: 0px; margin: auto; border:2px solid black";

const size = 50

var img = document.getElementById("red");

            ctx.drawImage(img, x * size, y * size);

for (let x = 0; x < 9; x++){
    for (let y = 0; y < 9; y++){
        if (((x + y) % 2) == 0){
            ctx.fillStyle = "black";
        }else{
            ctx.fillStyle = "red";
        }
        ctx.fillRect(x * size, y * size, size, size);
    }
}

function getMousePosition(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    let a = parseInt(x/ 50) + 1
    let b = parseInt(y / 50) + 1

    console.log(a + "," + b)

}

let canvasElem = document.querySelector("canvas");

canvasElem.addEventListener("mousedown", function (e) {
    getMousePosition(canvasElem, e);
}); 