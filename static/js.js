// pythonCommand can be any code in python
function execPythonCommand(pythonCommand){
    var request = new XMLHttpRequest()
    request.open("GET", "/" + pythonCommand, true)
    request.send()
}


const clickAndHold = (btnEl) => {
    let timerId;
    const DURATION = 20;

    //handle when clicking down
    const onMouseDown = () => {
      timerId = setInterval(() => {
        btnEl && btnEl.click();
      }, DURATION);
    };

    //stop or clear interval
    const clearTimer = () => {
      timerId && clearInterval(timerId);
    };

    //handle when mouse is clicked
    btnEl.addEventListener("mousedown", onMouseDown);
    //handle when mouse is raised
    btnEl.addEventListener("mouseup", clearTimer);
    //handle mouse leaving the clicked button
    btnEl.addEventListener("mouseout", clearTimer);

    // a callback function to remove listeners useful in libs like react
    // when component or element is unmounted
    return () => {
      btnEl.removeEventListener("mousedown", onMouseDown);
      btnEl.removeEventListener("mouseup", clearTimer);
      btnEl.removeEventListener("mouseout", clearTimer);
    };
  };

  //onMount
  document.addEventListener("DOMContentLoaded", function () {
    let camUp = document.getElementById("up");
    let camDwn = document.getElementById("down");
    let camLeft = document.getElementById("left");
    let camRight = document.getElementById("right");
    clickAndHold(camUp);
    clickAndHold(camDwn);
    clickAndHold(camLeft);
    clickAndHold(camRight);
  });