function showSheets() {

var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();

sheets.forEach(function(sheet) {

sheet.showSheet()

})
};