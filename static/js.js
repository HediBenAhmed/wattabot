// pythonCommand can be any code in python
function execPythonCommand(pythonCommand){
    var request = new XMLHttpRequest()
    request.open("GET", "/" + pythonCommand, true)
    request.send()
}