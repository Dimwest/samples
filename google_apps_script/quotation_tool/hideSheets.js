function hideSheets(visibleSheets) {

var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();

var visible = visibleSheets; //sheet names

sheets.forEach(function(sheet) {

if (visible.indexOf(sheet.getName()) == -1) {

sheet.hideSheet();

}

})

};