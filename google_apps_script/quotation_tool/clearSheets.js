function restartSheet() {
 
 confirmWindow("Are you sure that you want to clear this sheet ?")
  
 var thisSheet = SpreadsheetApp.getActiveSpreadsheet()
 var tasksFields = thisSheet.getSheetByName('tasks_fields_code');
 
 tasksFields.getRange("tasks_fields_code!A2:C16").clearContent();
 tasksFields.getRange("tasks_fields_code!G2:G16").clearContent();
 tasksFields.getRange("tasks_fields_code!I2:I16").clearContent();
 tasksFields.getRange("tasks_fields_code!L2:M16").clearContent();
 
 var invoiceFields = thisSheet.getSheetByName('quotation_fields');
 invoiceFields.getRange("quotation_fields!B9:B12").clearContent();
 invoiceFields.getRange("quotation_fields!B14:B17").clearContent();
  
 Logger.log("Sheet cleaned !")
 
}
