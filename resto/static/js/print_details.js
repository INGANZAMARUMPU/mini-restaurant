function templateFacture(id, date, serveur, table, total, caissier, facture_body){
 	str_lignes_facture=`
<tr>
<td>
Facture no. ${id+" "+date}<br>
Serveur: <b>${serveur}</b><br><br/>
RC .......................<br/>
NIF .......................<br/>
Tel: 79 991 419 / 75 790 436<br/>
FIDODIDO BAR-RESTAURANT<br/>
Chaussée PL Rwagasore<br/>
Rohero 1 Quartier INSS<br/><br/>
</td>
</tr>
<tr>
<td><b>${table}</b></td>
</tr>
<tr>
<td>
<table style="width:100%;">
<tbody>
<tr>
<th style="border-bottom: 1px solid #aaa;text-align: left;">Article</th>
<th style="border-bottom: 1px solid #aaa;text-align: left;">P.U.</th>
<th style="border-bottom: 1px solid #aaa;text-align: left;">Qt.</th>
<th style="border-bottom: 1px solid #aaa;text-align: right;">Total</th>
</tr>
${facture_body}
<tr>
<th style="border-top: 1px solid #aaa;text-align: left;">Total</th>
<th style="border-top: 1px solid #aaa;text-align: left;">&nbsp;</th>
<th style="border-top: 1px solid #aaa;text-align: left;">&nbsp;</th>
<th style="border-top: 1px solid #aaa;text-align: right;"><b>${total}</b></th>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td>Caissier ${caissier}</td>
</tr>
<tr>
<br>
<td style="text-align: center;"><strong>Merci à biento!</strong></td>
</tr>
<tr>
<td style="text-align: center;"><strong>Thank you see you soon!</strong></td>
</tr>
`;
	return str_lignes_facture;
}

function printDiv(id, date, serveur, table, total, caissier, object_facture) { 
	str_facture = templateFacture(id, date, serveur, table, total, caissier, object_facture);
	$("#printable-body").html(str_facture);

	var a = window.open('', '', 'height=500, width=1000'); 
	a.document.write($("#printable").html()); 
	a.document.close(); 
	a.print();
    a.close();
}