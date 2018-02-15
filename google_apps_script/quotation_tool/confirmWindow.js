function confirmWindow(body) {
 var ui = SpreadsheetApp.getUi();
 var response = ui.alert('Confirmation', body, ui.ButtonSet.YES_NO);

 // Process the user's response.
 if (response == ui.Button.YES) {
   Logger.log('Clicked yes, execution continues.');
 } else {
   Logger.log('Did not click yes, execution cancelled.');
   showSheets();
   throw new Error("User cancelled execution");
 }
  
}