# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:40:30 2022

@author: jcgarciam
"""
import pandas as pd
import numpy as np
from Extract import ExtraccionBases
from Transform_Joins import CreacionNuevasTablas

#Esta funcion filtra las nuevas tablas creadas por los joins y ademas crea nuevos campos
def NuevosCampos(HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED):
    MPP_total_acum_CCH = HyC_total_acum_CCH[HyC_total_acum_CCH['Tipo_Documento'].astype(int).isin([2,3])]
    
    HyC_total_acum_CCH = HyC_total_acum_CCH[HyC_total_acum_CCH['Tipo_Documento'].astype(int) == 4]
    
    HyC_total_acum_DCM = HyC_total_acum_DCM[HyC_total_acum_DCM['Tipo_Documento'].astype(int) == 4]
    
    HyC_total_acum_DDL = HyC_total_acum_DDL[HyC_total_acum_DDL['Tipo_Documento'].astype(int) == 4]
    
    MPP_total_acum_DCM = MPP_total_acum_DCM[MPP_total_acum_DCM['Tipo_Documento'].astype(int).isin([2,3])]
    
    MPP_total_acum_DDL = MPP_total_acum_DDL[MPP_total_acum_DDL['Tipo_Documento'].astype(int).isin([2,3])]
    
    MPP_total_acum_MED = MPP_total_acum_MED[MPP_total_acum_MED['Tipo_Documento'].astype(int).isin([2,3])]
    
    
    HyC_total_acum_CCH = Campos_Plan_Y_TipoContrato1(HyC_total_acum_CCH)
    
    HyC_total_acum_DCM = Campos_Plan_Y_TipoContrato1(HyC_total_acum_DCM)
    HyC_total_acum_DCM = DescuentoValorConsulta(HyC_total_acum_DCM)
    HyC_total_acum_DCM['Expr1'] = 'Consulta medica'
    
    
    HyC_total_acum_DDL = Campos_Plan_Y_TipoContrato1(HyC_total_acum_DDL) 
    HyC_total_acum_DDL = DescuentoTotalServicio(HyC_total_acum_DDL) 
    HyC_total_acum_DDL['Vales'] = HyC_total_acum_DDL['Valor_Cheque_Diagnostico']* HyC_total_acum_DDL['Total_Servicio']/ HyC_total_acum_DDL['Valor_Diagnostico']
    HyC_total_acum_DDL = HyC_total_acum_DDL.rename(columns = {'Total_Servicio':'Suma_Total_Servicio'})
    HyC_total_acum_DDL = dx_y_dias(HyC_total_acum_DDL)
    
    HyC_total_acum_DCM['dias'] = 0

    MPP_total_acum_CCH = Campos_Plan_Y_TipoContrato2(MPP_total_acum_CCH)
    
    MPP_total_acum_DCM = Campos_Plan_Y_TipoContrato2(MPP_total_acum_DCM)
    MPP_total_acum_DCM = DescuentoValorConsulta(MPP_total_acum_DCM)
    MPP_total_acum_DCM['Nombre'] = np.nan
    MPP_total_acum_DCM['dias'] = np.nan
    MPP_total_acum_DCM = MPP_total_acum_DCM.rename(columns = {'Valor_Consulta':'Suma_Valor_Consulta','Valor_cheque_consulta':'Suma_Valor_Cheque_Consulta'})
    

    MPP_total_acum_DDL = Campos_Plan_Y_TipoContrato2(MPP_total_acum_DDL)
    MPP_total_acum_DDL = DescuentoTotalServicio(MPP_total_acum_DDL)
    MPP_total_acum_DDL = dx_y_dias(MPP_total_acum_DDL)
    MPP_total_acum_DDL['Vales'] = MPP_total_acum_DDL['Valor_Cheque_Diagnostico']* MPP_total_acum_DDL['Total_Servicio']/MPP_total_acum_DDL['Valor_Diagnostico']
    MPP_total_acum_DDL = MPP_total_acum_DDL.rename(columns = {'Total_Servicio':'Suma_Total_Servicio'})
    MPP_total_acum_DDL['Nombre'] = MPP_total_acum_DDL['DESCRIPCION SERVICIO']
    
    
    MPP_total_acum_MED['CarneUsuario'] = pd.Categorical(MPP_total_acum_MED['CarneUsuario'].apply(str))
    MPP_total_acum_MED['Plan'] = MPP_total_acum_MED['CarneUsuario'].str[0:2]
    MPP_total_acum_MED['Tipo Contrato'] = MPP_total_acum_MED['CarneUsuario'].str[2:3]
    #MPP_total_acum_MED['Val cheques'] = 0
    MPP_total_acum_MED['Val descuento'] = 0
    MPP_total_acum_MED['dx'] = np.nan
    MPP_total_acum_MED['descripcion dx'] = np.nan
    MPP_total_acum_MED['Nombre'] = MPP_total_acum_MED['DESCRIPCION SERVICIO']
    MPP_total_acum_MED = MPP_total_acum_MED.rename(columns = {'VlrTotMedica':'Suma_Vlr_Tot_Medica','Valor_Cheques':'Val cheques'})
    
    MPP_total_acum_DCM['Tabla'] = 'DCM'
    MPP_total_acum_DDL['Tabla'] = 'DDL'
    MPP_total_acum_MED['Tabla'] = 'MED'
    MPP_total_acum_CCH['Tabla'] = 'CCH'
    HyC_total_acum_CCH['Tabla'] = 'CCH'
    HyC_total_acum_DCM['Tabla'] = 'DCM'
    HyC_total_acum_DDL['Tabla'] = 'DDL'
    
    
    return HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED, MPP_total_acum_CCH


def Campos_Plan_Y_TipoContrato1(df):
    df['Numero_Carne'] = pd.Categorical(df['Numero_Carne'].apply(str))
    df['Plan'] = df['Numero_Carne'].str[0:3]
    df['Tipo_Contrato'] = df['Numero_Carne'].str[3:4]
    return df
    
def Campos_Plan_Y_TipoContrato2(df):
    df['Numero_Carne'] = pd.Categorical(df['Numero_Carne'].apply(str))
    df['Plan'] = df['Numero_Carne'].str[0:2]
    df['Tipo_Contrato'] = df['Numero_Carne'].str[2:3]
    return df

def DescuentoValorConsulta(df):
    df['Descuento'] = df['Descuento_General']*(df['Valor_Consulta']/(df['Valor'] + df['Descuento_General']))
    return df
   
def DescuentoTotalServicio(df):    
    df['Descuento'] = df['Descuento_General']*(df['Total_Servicio']/(df['Valor'] + df['Descuento_General'])) 
    return df

def dx_y_dias(df):
    df['dx'] = np.nan
    df['descripcion dx'] = np.nan
    df['dias'] = 0
    return df 

#Esta funcion se crea para realizar unos groupby que estaban programados en el access que erea el programa que creaba
#los informes de gasto medico
def GroupByValores(df,Nombres_Finales):  
    df['Concatenacion'] = (df['Tipo_Negocio'].astype(str) + df['Folio'].astype(str) + df['Fecha_Contabilizacion'].astype(str) +
                    df['Sucursal'].astype(str) + df['Plan'].astype(str) + df['Tipo_Contrato'].astype(str) +
                    df['Carne'].astype(str) + df['Tipo_Identificacion_Usuario'].astype(str) + df['Nro_Identificacion'].astype(str) + 
                    df['Descuento_General'].astype(str) + df['Nombre'].astype(str) + df['Descripcion_Servicio'].astype(str) +
                    df['Descripcion_Agrupacion'].astype(str) + df['Diagnostico_2'].astype(str) + df['Codigos_Diagnostico_Descripcion'].astype(str) + 
                    df['Procedimiento'].astype(str) + df['Codigos_Procedimiento_Descripcion'].astype(str) + 
                    df['Dias'].astype(str) + df['Fecha_Servicio'].astype(str) + df['Tipo_Identificacion_Institucion'].astype(str) +
                    df['NIT'].astype(str) + df['Fecha_Radicacion'].astype(str) + df['Numero_Factura'].astype(str) + df['Tabla'].astype(str))

    
    df2 = df[['Concatenacion','Valor_Hospital','Valor_Cheques_Hospital']]
    df2 = df2.groupby(['Concatenacion'])['Valor_Hospital','Valor_Cheques_Hospital'].sum().reset_index()
    
    
    
    df = df.drop_duplicates('Concatenacion')
    df = df.drop(columns = ['Valor_Hospital','Valor_Cheques_Hospital'])
    
    
    
    df = df.merge(df2, how = 'left', on = 'Concatenacion') 
    df = df.drop(columns = ['Concatenacion'])
    
    df = df[Nombres_Finales]
    
    return df

