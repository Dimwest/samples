function selectTCSheets() {
  var sheetsKept = ['quotation_document'];
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();

  for (var i = 1; i < sheets.length; i++) {
    sheetName = sheets[i].getName()
    isEmpty = collectData(sheetName, 'B15')
    
    if (sheetName.match('t&c_[0-9]?[0-9]') && isEmpty != '') {
      sheetsKept.push(sheetName);
    }
  
  }
  
  sheetsKept.push('t&c_signature');
  
  return sheetsKept;
}