function collectData(sheetName, cell) {
  
  var originalSpreadsheet = SpreadsheetApp.getActive();
  var sheet = originalSpreadsheet.getSheetByName(sheetName);
  var cellValue = sheet.getRange(cell).getValue();
  return cellValue;
};