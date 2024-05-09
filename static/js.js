// pythonCommand can be any code in python
function execPythonCommand(pythonCommand){
    $.ajax({ 
      url: '/'+pythonCommand, 
      type: 'GET', 
      contentType: 'application/json', 
      success: function(response) { 
          document.getElementById('output').innerHTML = response; 
      }, 
      error: function(error) { 
          console.log(error); 
      } 
  }); 
}


const clickAndHold = (btnEl) => {
    let timerId;
    const DURATION = 50;

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
    let camUp = document.getElementById("cupBtn");
    let camDwn = document.getElementById("cdownBtn");
    let camLeft = document.getElementById("cleftBtn");
    let camRight = document.getElementById("crightBtn");
    clickAndHold(camUp);
    clickAndHold(camDwn);
    clickAndHold(camLeft);
    clickAndHold(camRight);
  });