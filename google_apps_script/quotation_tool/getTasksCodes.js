function getTaskCodes() {
 
 var taskCodes = "";
  
  for (i = 2; i < 17; i++) {
    
    var cellCoords = "C" + i
    
    if (collectData("tasks_fields_code", cellCoords) != "") {
      taskCodes += collectData("tasks_fields_code", cellCoords) + "\n";
    }
    
  };
  
 return taskCodes
}
