

function checkboxChange(clickedBox){
    //function to ensure only one option can be selected at one time
    if(clickedBox.id == "Take-out" && clickedBox.checked){
        document.getElementById("Return").checked = false;
    } else if(clickedBox.id == "Return" && clickedBox.checked){
        document.getElementById("Take-out").checked = false;
    }

}

document.addEventListener("DOMContentLoaded", () => startScanner());

function qrBoxSize(){
    let minEdgePercentage = 0.7; // 70%
    let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
    let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
    return {
        width: qrboxSize,
        height: qrboxSize
    };

}

function startScanner() {
  const logDiv = document.getElementById('log'); //display messages to the user
  //setup the qr scanner and display video feed
  const html5QrCode = new Html5Qrcode("reader"); //will create a new object where the qr reader will appear

  //ask the browser for a list of available cameras
  //.then --> when the cameras are found run the following function...
  // cameras{} is working as an array {id:label}
  Html5Qrcode.getCameras().then(cameras => {
    //ensure cameras are working... if true
    if (cameras && cameras.length) {
        //using the first camera in the list setup with these specs
      html5QrCode.start(
        cameras[0].id,
        { fps: 10, qrbox: qrBoxSize },
        qrCodeMessage => {
            //callback function - when qr detected
          scanQrCode(qrCodeMessage)
          //logDiv.textContent = "Scanned: " + qrCodeMessage; //TESTING ONLY
        }
      );
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



