'''
Created on 16 oct. 2017

@author: Nicolas F
'''

from django.db import connection

def getTotalsToCloseBox(idAperturaCaja):
    with connection.cursor() as cursor:
        #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT coalesce(sum(total_sin_iva),0) as total_sin_iva, " + 
                            "coalesce(sum(monto_iva), 0) as monto_iva, " + 
                            "coalesce(sum(total), 0) as total " + 
                       "FROM gallery_venta " + 
                       "WHERE " + '"' + "AperturaCaja_id" + '"' + "=%s;", [idAperturaCaja])
        #row = cursor.fetchone()
        row = cursor.fetchall() 

    return row


