function convertSpreadsheetToPdf(email, spreadsheetId, sheetName, pdfName, mailSubject, mailBody, folderId) {

  var spreadsheet = spreadsheetId ? SpreadsheetApp.openById(spreadsheetId) : SpreadsheetApp.getActiveSpreadsheet();
  spreadsheetId = spreadsheetId ? spreadsheetId : spreadsheet.getId()  
  var sheetId = sheetName ? spreadsheet.getSheetByName(sheetName).getSheetId() : null;  
  var pdfName = pdfName ? pdfName : spreadsheet.getName();
  var parents = DriveApp.getFileById(spreadsheetId).getParents();
  var folder = DriveApp.getFolderById(folderId)//parents.hasNext() ? parents.next() : DriveApp.getRootFolder();
  var url_base = spreadsheet.getUrl().replace(/edit$/,'');

  var url_ext = 'export?exportFormat=pdf&format=pdf'   //export as pdf

      // Print either the entire Spreadsheet or the specified sheet if optSheetId is provided
      + (sheetId ? ('&gid=' + sheetId) : ('&id=' + spreadsheetId)) 
      // following parameters are optional...
      + '&size=letter'      // paper size
      + '&portrait=true'    // orientation, false for landscape
      + '&fitw=true'        // fit to width, false for actual size
      + '&sheetnames=false&printtitle=false&pagenum=RIGHT'  //hide optional headers and footers
      + '&gridlines=false'  // hide gridlines
      + '&fzr=false';       // do not repeat row headers (frozen rows) on each page

  var options = {
    headers: {
      'Authorization': 'Bearer ' +  ScriptApp.getOAuthToken(),
    }
  }
  
  var response = UrlFetchApp.fetch(url_base + url_ext, options);
  var blob = response.getBlob().setName(pdfName + '.pdf');
  folder.createFile(blob);
  
  confirmWindow('Do you also want to send the quotation via email ?');
  
  if (email) {

    var mailOptions = {
      attachments:blob
    }

    MailApp.sendEmail(
      email, 
      mailSubject, 
      mailBody, 
      mailOptions);
  }
  
}