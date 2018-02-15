function execScript(){
  
  var thisSheetId = SpreadsheetApp.getActiveSpreadsheet().getId()
  var folderId = collectData('settings', 'C2');
  var exportSheetId = collectData('settings', 'C3');
  var date = (new Date()).toISOString().slice(0,16).replace(/-/g,"").replace("T","").replace(":","");
  var dateString = (new Date()).toISOString().slice(0,16).replace("T"," ");
  var sheetsKept = selectTCSheets();
  var sheetsStart = ['quotation_document', 'quotation_fields', 'tasks_fields_code', 't&c_fields', 'settings']

  var clientCompany = collectData('quotation_fields', 'B9');
  var clientAddress = collectData('quotation_fields', 'B10');  
  var email = collectData('quotation_fields', 'B11');
  var receiverName = collectData('quotation_fields', 'B12');
  var senderName = collectData('quotation_fields', 'B13');
  var language = collectData('quotation_fields', 'B16');
  var invoiceTaxCase = collectData('quotation_fields', 'B17');
  var invoiceTaxRate = collectData('quotation_document', 'H32').toFixed(2);
  var invoiceAmountPreTax = collectData('quotation_document', 'H31').toFixed(2);
  var invoiceAmountTaxInc = collectData('quotation_document', 'H33').toFixed(2);
  var invoiceCurrency = collectData('quotation_document', 'I33');
  var validUntil = collectData('quotation_document', 'F11');
  var taskCodes = getTaskCodes();
  
  var quoteName = collectData('quotation_document', 'B8').replace('Quotation ID: ', '');
  
  var confirmBody = 'Are you sure you want to create the following invoice as .pdf ?\n\n'+
    'Sender: ' + senderName + '\n' +
    'Receiver: ' + receiverName + ' - ' + email + '\n' +
    'Total amount before tax: ' + invoiceAmountPreTax + ' ' + invoiceCurrency + '\n' +
    'Tax case: ' + invoiceTaxCase + '\n' +
    'Tax rate: ' + (invoiceTaxRate*100) + '%' + '\n' +
    'Total amount tax inc.: ' + invoiceAmountTaxInc + ' ' + invoiceCurrency + '\n' +
    'Valid until: ' + validUntil + '\n' +
    'T&Cs language: ' + language + '\n' +
    'Quote name: ' + quoteName;
  
  confirmWindow(confirmBody);

  exportInvoiceData(exportSheetId, quoteName, dateString, clientCompany, clientAddress, email, receiverName,
                    validUntil, taskCodes, invoiceCurrency, language, invoiceTaxCase, invoiceAmountPreTax, 
                    invoiceAmountTaxInc, senderName);
  
  var body = collectData('quotation_fields', 'B18');
  
  hideSheets(sheetsKept);
  convertSpreadsheetToPdf(email, thisSheetId, undefined, quoteName, quoteName, body, folderId);
  showSheets();

}