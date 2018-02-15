function exportInvoiceData(exportSheetId, quoteId, quoteDate, clientCompany, clientAddress, clientEmail, clientName, 
                           validUntil, taskCodes, currency, tcLang, taxCase, totalNoTax, totalTaxInc, senderName)
{
 
 var destinationSpreadSheet = SpreadsheetApp.openById(exportSheetId);
 var destinationTab = destinationSpreadSheet.getSheetByName('export_sheet');
 var targetRow = destinationTab.getLastRow()+1

 destinationTab.getRange(targetRow, 1).setValue(targetRow - 1); 
 destinationTab.getRange(targetRow, 2).setValue(quoteId);
 destinationTab.getRange(targetRow, 3).setValue(quoteDate);
 destinationTab.getRange(targetRow, 4).setValue(clientCompany);
 destinationTab.getRange(targetRow, 5).setValue(clientAddress);
 destinationTab.getRange(targetRow, 6).setValue(clientEmail);
 destinationTab.getRange(targetRow, 7).setValue(clientName);
 destinationTab.getRange(targetRow, 8).setValue(validUntil);
 destinationTab.getRange(targetRow, 9).setValue(taskCodes);
 destinationTab.getRange(targetRow, 10).setValue(currency);
 destinationTab.getRange(targetRow, 11).setValue(tcLang);
 destinationTab.getRange(targetRow, 12).setValue(taxCase);
 destinationTab.getRange(targetRow, 13).setValue(totalNoTax);
 destinationTab.getRange(targetRow, 14).setValue(totalTaxInc);
 destinationTab.getRange(targetRow, 15).setValue(senderName);
 Logger.log("Invoice exported !")
 
}