

function checkboxChange(clickedBox){
    //function to ensure only one option can be selected at one time
    if(clickedBox.id == "Take-out" && clickedBox.checked){
        document.getElementById("Return").checked = false;
    } else if(clickedBox.id == "Return" && clickedBox.checked){
        document.getElementById("Take-out").checked = false;
    }

}

document.addEventListener("DOMContentLoaded", () => startScanner());

function qrBoxSize(viewfinderWidth, viewfinderHeight) {
  let minEdgePercentage = 0.7; // 70%
  let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
  let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
  return {
    width: qrboxSize,
    height: qrboxSize
  };
}

function startScanner() {
  const logDiv = document.getElementById('log'); // display messages to the user
  const html5QrCode = new Html5Qrcode("reader"); // create new QR reader area

  Html5Qrcode.getCameras().then(cameras => {
    if (cameras && cameras.length) {
      // use the first detected camera (change index for USB if needed)
      const cameraId = cameras[0].id;

      html5QrCode.start(
        cameraId,
        {
          fps: 10,
          qrbox: { width: 300, height: 300 }, // ✅ fix: was "qr box"
          videoConstraints: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: "environment" // good for external USB webcams
          }
        },
        qrCodeMessage => {
          // callback function - when QR is detected
          scanQrCode(qrCodeMessage);
        },
        errorMessage => {
          // optional: called for every scan failure
          console.warn("QR scan error:", errorMessage);
        }
      ).catch(err => {
        logDiv.textContent = "Failed to start scanner: " + err;
      });
    } else {
      logDiv.textContent = "No camera found.";
    }
  }).catch(err => {
    logDiv.textContent = "Camera access error: " + err;
  });
}

function scanQrCode(decodedText){
  //decodedText and result are the QR code!
  try{
    const data = JSON.parse(decodedText);
    document.getElementById('Book-title').value = data.title || '';
    document.getElementById('Book-author').value = data.author || '';

  } catch(e) {
    console.error("Ivalide QR code", e)
  }

}



