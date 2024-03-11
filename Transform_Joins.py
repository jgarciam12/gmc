# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 08:55:56 2022

@author: jcgarciam
"""

import pandas as pd

#%%

#Esta funcion mezcla los reportes SIRUP y los codigos.
def CreacionNuevasTablas(CCM, CCH, DCM, DDL, BLA, Medicamentos, Codigos_Procedimiento, Codigos_Servicio, Codigos_Diagnostico):

    HyC_total_acum_CCH = InnerJoin1(CCM, CCH)
    HyC_total_acum_CCH = LeftJoin1(HyC_total_acum_CCH,Codigos_Servicio)
    HyC_total_acum_CCH = LeftJoin2(HyC_total_acum_CCH, Codigos_Diagnostico, Codigos_Procedimiento)
    
    HyC_total_acum_DCM = RightJoin(CCM, DCM)
    HyC_total_acum_DCM = LeftJoin2(HyC_total_acum_DCM, Codigos_Diagnostico, Codigos_Procedimiento)
    
    HyC_total_acum_DDL = InnerJoin1(CCM, DDL)
    HyC_total_acum_DDL = InnerJoin2(HyC_total_acum_DDL, BLA)
    HyC_total_acum_DDL = pd.merge(HyC_total_acum_DDL, Codigos_Procedimiento, how = 'left', on = 'Procedimiento')
    
    MPP_total_acum_DCM = InnerJoin1(CCM, DCM)
    MPP_total_acum_DCM = LeftJoin2(MPP_total_acum_DCM, Codigos_Diagnostico, Codigos_Procedimiento)
    
    MPP_total_acum_DDL = RightJoin(CCM, DDL)
    MPP_total_acum_DDL = pd.merge(MPP_total_acum_DDL, BLA, how = 'inner', on = ['Fecha_Contabilizacion', 'Tipo_Documento', 
                                                                                'Folio', 'Sucursal', 'Consecutivo', 'Correlativo'])
    MPP_total_acum_DDL = pd.merge(MPP_total_acum_DDL, Codigos_Procedimiento, how = 'left', on = 'Procedimiento')
    
    MPP_total_acum_MED = pd.merge(CCM, Medicamentos, how = 'inner', left_on = ['Fecha_Contabilizacion','Folio'],
                                  right_on = ['FechaCon', 'Folio'])
    MPP_total_acum_MED = pd.merge(MPP_total_acum_MED, Codigos_Procedimiento, how = 'left', left_on = 'CodMedicamento',
                                  right_on = 'Procedimiento')
    
    return HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED

#Se crean los Joins de interseccion

def InnerJoin1(df1,df2):
    
    df = pd.merge(df1,df2, how = 'inner', on = ['Fecha_Contabilizacion', 'Tipo_Documento', 'Folio', 'Sucursal'])
    
    return df

def InnerJoin2(df1,df2):
    
    df = pd.merge(df1,df2, how = 'inner', on = ['Fecha_Contabilizacion', 'Tipo_Documento', 'Folio', 'Sucursal','Consecutivo',
                                                'Correlativo'])
    return df

#Se crean los joins left
def LeftJoin1(df1,df2):  
    
    df = pd.merge(df1, df2, how = 'left', on = ['Tipo_Servicio', 'Tipo_Atencion', 'Clase_Atencion'])
    
    return df

def LeftJoin2(df1,df2,df3):
    
    df = pd.merge(df1, df2, how = 'left', left_on = 'Diagnostico_Ingreso', right_on = 'CODIGO')
    df = pd.merge(df, df3, how = 'left', on = 'Procedimiento')
    return df

#Se crea el join right
def RightJoin(df1,df2):
    
    df = pd.merge(df1,df2, how = 'right', on = ['Fecha_Contabilizacion','Tipo_Documento','Folio','Sucursal'])
    return df
