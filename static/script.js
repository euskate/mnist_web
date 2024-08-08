const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    draw(e);
});

canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath();
});

canvas.addEventListener('mouseout', () => {
    drawing = false;
    ctx.beginPath();
});

function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 20;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function uploadImage() {
    const scaledCanvas = document.createElement('canvas');
    const scaledCtx = scaledCanvas.getContext('2d');
    scaledCanvas.width = 28;
    scaledCanvas.height = 28;
    scaledCtx.drawImage(canvas, 0, 0, 28, 28);
    const dataURL = scaledCanvas.toDataURL('image/png');
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataURL }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.digit !== undefined) {
            document.getElementById('result').innerText = `Predicted Digit: ${data.digit}`;
        } else {
            document.getElementById('result').innerText = 'Prediction failed.';
        }
    });
}
