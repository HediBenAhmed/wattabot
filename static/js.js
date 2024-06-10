// pythonCommand can be any code in python
function execPythonCommand(feature, command){
    $.ajax({ 
      url: '/command/'+feature+'/'+command, 
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

function featureStartStop(cb){
  execPythonCommand(cb.id, cb.checked ? "START": "STOP")
}



var socket = io();


const joyCamera = new JoyStick('joyCamera', {"title": "Camera", "width": 300, "height": 300});
setInterval(function(){
	if(joyCamera.GetDir() !== 'C'){
		console.log("CAM", joyCamera.GetDir())
    execPythonCommand("cameraControl","CAM_" + joyCamera.GetDir())
	}
}, 100);

let motorDirection = 'C';
const joyMotor = new JoyStick('joyMotor', {"title": "Motor", "width": 300, "height": 300}, function(stickData) {
	if(motorDirection !== stickData.cardinalDirection){
		console.log("MOTOR_", stickData.cardinalDirection)
		motorDirection = stickData.cardinalDirection;
    execPythonCommand("motorsControl","MOTOR_" + motorDirection)
	}
});