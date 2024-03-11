# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:53:52 2022

@author: jcgarciam
"""

import pandas as pd
import numpy as np

def CambioFormato(df, a = 'a'):
    df[a] = df[a].astype(str).str.strip().str.strip('\x02').str.strip('')
    df[a] = np.where(df[a].str[-2::] == '.0', df[a].str[0:-2], df[a])
    df[a] = np.where(df[a] == 'nan', np.nan, df[a])
    
    return df[a]

def ExtraccionBases(path_input1,path_salida):
    file_codigos = path_input1 + '\Codigos/Codigos.xlsx'
    
    #Extracción de archivos MPP
    dir_db = path_salida.format('DB_MOD_MPP.xlsx')
    xls = pd.ExcelFile(dir_db)
    sheets = xls.sheet_names
    Data = {}
    for sheet in sheets:
        Data[sheet] = xls.parse(sheet)
            
    xls.close()
    
    
    BLA = Data['BLA']    
    CCM = Data['CCM']
    CCH = Data['CCH']
    DCM = Data['DCM']
    DDL = Data['DDL']
    Medicamentos = Data['Medicamentos']
    
    #Cambiamos el formato de las columnas que tienen una fecha, ya que aparecen AAAA/MM/DD
    #y se necesitan en formato DD/MM/AAAA
        
    #Primero los pasamos a tipo fecha
    
    CCM['Fecha_Contabilizacion'] = pd.to_datetime(CCM['Fecha_Contabilizacion'], format = '%d/%m/%Y')
    CCM['Fecha_Factura'] = pd.to_datetime(CCM['Fecha_Factura'], format = '%d/%m/%Y')
    CCM['Fecha_Folio'] = pd.to_datetime(CCM['Fecha_Folio'], format = '%d/%m/%Y')
    CCH['Fecha_Contabilizacion'] = pd.to_datetime(CCH['Fecha_Contabilizacion'], format = '%d/%m/%Y')
    CCH['Fecha_Servicio'] = pd.to_datetime(CCH['Fecha_Servicio'], format = '%d/%m/%Y')
    DCM['Fecha_Contabilizacion'] = pd.to_datetime(DCM['Fecha_Contabilizacion'], format = '%d/%m/%Y')
    DCM['Fecha_Servicio'] = pd.to_datetime(DCM['Fecha_Servicio'], format = '%d/%m/%Y')
    DDL['Fecha_Contabilizacion'] = pd.to_datetime(DDL['Fecha_Contabilizacion'], format = '%d/%m/%Y')
    DDL['Fecha_Servicio'] = pd.to_datetime(DDL['Fecha_Servicio'], format = '%d/%m/%Y')
    BLA['Fecha_Contabilizacion'] = pd.to_datetime(BLA['Fecha_Contabilizacion'], format = '%d/%m/%Y')
    Medicamentos['FechaCon'] = pd.to_datetime(Medicamentos['FechaCon'], format = '%d/%m/%Y')
    
    #Ahora cambiamos el orden de la fecha a DD/MM/AAAA
    CCM['Fecha_Contabilizacion'] = CCM['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
    CCM['Fecha_Factura'] = CCM['Fecha_Factura'].dt.strftime('%d/%m/%Y')
    CCM['Fecha_Folio'] = CCM['Fecha_Folio'].dt.strftime('%d/%m/%Y')
    CCH['Fecha_Contabilizacion'] = CCH['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
    CCH['Fecha_Servicio'] = CCH['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
    DCM['Fecha_Contabilizacion'] = DCM['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
    DCM['Fecha_Servicio'] = DCM['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
    DDL['Fecha_Contabilizacion'] = DDL['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
    DDL['Fecha_Servicio'] = DDL['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
    BLA['Fecha_Contabilizacion'] = BLA['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
    Medicamentos['FechaCon'] = Medicamentos['FechaCon'].dt.strftime('%d/%m/%Y')
    
    Medicamentos['CantiMedica'] = Medicamentos['CantiMedica'].astype(str).str.replace(',','.').astype(int)

    #Estandarizamos formato tipo Ids
    lista = ['NunIdUsuario','CarneUsuario','Folio']
    
    for i in lista:
        Medicamentos[i] = CambioFormato(Medicamentos, a = i)
    
    lista = ['Sucursal','Tipo_Documento','Consecutivo','Correlativo',
             'Folio','Procedimiento','Consecutivos']
    
    for i in lista:
        BLA[i] = CambioFormato(BLA, a = i)

    lista = ['Folio','Numero_Identificacion','Numero_Carne','Correlativo',
             'Consecutivo','Sucursal','Tipo_Documento','Servicio',
             'Tipo_Contingencia','Clase_Atencion']
             
    for i in lista:
        DDL[i] = CambioFormato(DDL, a = i)

    lista = ['Folio','Numero_Identificacion','Numero_Carne','Procedimiento',
             'Numero_Ident_Medico','Correlativo','Consecutivo','Tipo_Documento',
             'Servicio','Clase_Atencion','Tipo_Contigencia','Sucursal']
    
    for i in lista:
        DCM[i] = CambioFormato(DCM, a = i)
    
    lista = ['Folio','Numero_Identificacion','Numero_Carne','Procedimiento',
             'Sucursal','Tipo_Documento','Correlativo','servicio',
             'Tipo_Contingencia','Clase_Atencion','Tipo_Atencion',
             'Tipo_Servicio']
    
    for i in lista:
        CCH[i] = CambioFormato(CCH, a = i)

    lista = ['Folio','NIT','Sucursal','Tipo_Documento','Tipo_Cuenta',
             'Tipo_Iden_Inst'] 
    
    for i in lista:
        CCM[i] = CambioFormato(CCM, a = i)

    #Extraccion Codigos de procedimientos
    xls = pd.ExcelFile(file_codigos)
    sheets = xls.sheet_names
    Codigos = {}
    for sheet in sheets:
        Codigos[sheet] = xls.parse(sheet)
        xls.close()
    
    Codigos_Procedimiento = Codigos['Codigos_Procedimiento']
    
    lista = ['BEN_NCODE','Procedimiento','CODIGO SERVICIO','CODIGO AGRUPACION']
    
    for i in lista:
        Codigos_Procedimiento[i] = CambioFormato(Codigos_Procedimiento, a = i)
        
    Codigos_Servicio = Codigos['Codigos_Servicio']
    
    lista = ['Clase_Atencion','Tipo_Atencion','Tipo_Servicio']
    
    for i in lista:
        Codigos_Servicio[i] = CambioFormato(Codigos_Servicio, a = i)
        
    Codigos_Diagnostico = Codigos['Codigos_Diagnostico']
    
    Codigos_Diagnostico['CONSECUTIVO'] = CambioFormato(Codigos_Diagnostico, a = 'CONSECUTIVO')
    
    return CCM, CCH, DCM, DDL, BLA, Medicamentos, Codigos_Procedimiento, Codigos_Servicio, Codigos_Diagnostico



    
