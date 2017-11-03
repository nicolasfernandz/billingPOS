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


def getZETAReportDetailsByOpeningBoxNumber(idAperturaCaja):
    with connection.cursor() as cursor:   
        cursor.execute("SELECT ac.id as apertura, " + 
                              "ac." + '"' + "fecha_apertura_Caja" + '"' + " as fecha_apertura, " + 
                              "ac." + '"' + "fecha_cierre_Caja" + '"' + " as fecha_cierre, " +
                              "ac." + '"' + "Caja_id" + '"' + " as Caja, " +
                              "coalesce(sum(v.total_sin_iva),0) as total_sin_iva, " +
                              "coalesce(sum(monto_iva), 0) as monto_iva, " + 
                              "coalesce(sum(total), 0) as total, " +
                              "min(v.id) as ticket_desde, " +
                              "max(v.id) as ticket_hasta, " +
                              "count(lv.*) as productos_vendidos " +
                       "FROM gallery_aperturacaja ac, gallery_venta v, gallery_linea_venta lv " +
                       "WHERE ac.id = v." + '"' + "AperturaCaja_id" + '" ' +
                            "AND v.id = lv." + '"' + "Venta_id" + '" ' +
                            "AND ac.id = %s "
                        "Group by ac.id;", [idAperturaCaja])
        #row = cursor.fetchone()
        row = cursor.fetchall() 

    return row
    
def getSalesProductsCountsByOpeningBoxNumber(idAperturaCaja):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.nombre, count(p.id) " +
                       "FROM gallery_venta v, gallery_linea_venta lv, gallery_preciosproductofecha ppf, gallery_producto p " +
                       "WHERE v." + '"' + "AperturaCaja_id" + '"' + "=%s "
                            "AND v.id = lv." + '"' + "Venta_id" + '" ' +
                            "AND lv." + '"' + "ImpuestosProductoFecha_id" + '"' + "= ppf.id " +
                            "AND ppf." + '"' + "Producto_id" + '"' + "= p.id "
                       "Group by p.nombre;", [idAperturaCaja])
        #row = cursor.fetchone()
        row = cursor.fetchall() 

    return row

def getTicketsByOpeningBoxNumber(idAperturaCaja):
    with connection.cursor() as cursor:   
        cursor.execute("SELECT ac.id as apertura, " +
                              "min(v.id) as ticket_desde, " +
                              "max(v.id) as ticket_hasta, " +
                              "count(lv.*) as productos_vendidos " +
                       "FROM gallery_aperturacaja ac, gallery_venta v, gallery_linea_venta lv " +
                       "WHERE ac.id = v." + '"' + "AperturaCaja_id" + '" ' +
                            "AND v.id = lv." + '"' + "Venta_id" + '" ' +
                            "AND ac.id = %s "
                        "Group by ac.id;", [idAperturaCaja])
        #row = cursor.fetchone()
        row = cursor.fetchall() 

    return row


def getVentaPorProductoPorFechas(fromDate, endDate):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.nombre, " +
                                "p.aplica_impuesto, " + 
                                "ipf.porcentaje_impuesto, " + 
                                "count(p.id) as cantidad, " +
                                "coalesce(sum(v.total_sin_iva),0) as sub_total_ventas, " +
                                "coalesce(sum(v.monto_iva),0) as iva_venta, " + 
                                "coalesce(sum(v.total),0) as total_venta " +        
                        "FROM gallery_venta v, " + 
                                "gallery_linea_venta lv, " + 
                                "gallery_impuestosproductofecha ipf, " +
                                "gallery_preciosproductofecha ppf, " + 
                                "gallery_producto p " +
                        #"WHERE v.fecha between to_timestamp('2015-12-02 12:20:48', 'YYYY-MM-DD HH24:MI:SS') and to_timestamp('2018-12-02 12:20:48', 'YYYY-MM-DD HH24:MI:SS') " +
                        "WHERE v.fecha between date %s and date %s " +
                                "AND v.id = lv." + '"' + "Venta_id" + '" ' +
                                "AND lv." + '"' + "PreciosProductoFecha_id"  + '"' + "= ppf.id " +
                                "AND lv." + '"' + "ImpuestosProductoFecha_id"  + '"' + "= ipf.id " +
                                "AND ppf." + '"' + "Producto_id" + '"' + "= p.id " +
                        #"Group by(p.nombre, p.aplica_impuesto, ipf.porcentaje_impuesto);", ([fromDate],[endDate]))
                        "Group by(p.nombre, p.aplica_impuesto, ipf.porcentaje_impuesto);", [fromDate, endDate])
        row = cursor.fetchall()
    return row