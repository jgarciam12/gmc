# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:16:22 2021

@author: rfpinedab
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

#%%
Tiempo_Total = datetime.now()

path_entrada = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\12. Gasto Medico\Entradas\Consolidado'#r'D:\DATOS\Users\yardilap\OneDrive - AXA Colpatria Seguros\Ysk\BI\ARL Y Salud\Gasto Medico Contable\Input\Consolidado GM Activa'
path_salida = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\12. Gasto Medico\Salidas'
#%%
mes = input('Ingrese el nombre del mes a trabajar: ejemplo: Enero: ')
anio = input('Ingrese el año a trabajar: ')
path_entrada_archivo = r'\\dc1pvfnas1\Autos\Soat_Y_ARL\Pagos_Arl_Salud\Cierre'
path_entrada_archivo = path_entrada_archivo + '/' + str(anio) + '/' + mes.title() + '/Salud/GM Actuaría'
#%%
## 1. PREPARA ARCHIVOS DE CONSOLIDADO
Tiempo_Parcial = datetime.now() #PERMITE CONOCER EL TIEMPO PARCIAL DE CADA UNO  DE LOS PROCESOS.
print('''
Cargando archivos de Consolidado del Gasto Medico descargados desde ACTIVA, cargar en formato csv.
''')

consolidado = []
for archivos in glob.glob(path_entrada+'\*.xlsx'):
    print(archivos[len(path_entrada) + 1::])
    dfconsolidado = pd.read_excel(archivos,
                            #sep=";",
                            header = 0,
                            usecols = ['FOLIO','NRO_CONTRATO','NRO_IDENTIFICACION_BENEF','FECHA_RAD_FACT','COD_PROCEDIMIENTO','COD_DIAGNOSTICO','NOMBRE_PROCEDIMIENTO','CUPS_PRINCIPAL','CONCEPTO_HOSPITALARIO','TIPO_CUENTA','Dx_Egreso','Dx_Nombre','NIT_PRESTADOR','NOMBRE_PRESTADOR'],
                            #encoding=('latin-1'),
                            #low_memory=False,
                            index_col= False)
    consolidado.append(dfconsolidado)
    
#%%


dfconsolidado = pd.concat(consolidado).reset_index(drop = True)
print("Tiempo de carga Consolidado: " , datetime.now()-Tiempo_Parcial)
print("Cantidad de Registros Cargados: ", len(dfconsolidado))

Nombre_Nits = dfconsolidado[['NIT_PRESTADOR','NOMBRE_PRESTADOR']].copy()
Nombre_Nits = Nombre_Nits.rename(columns = {'NIT_PRESTADOR':'NIT','NOMBRE_PRESTADOR':'Razon_Social'})
Nombre_Nits = Nombre_Nits[Nombre_Nits['Razon_Social'].isnull() == False]
Nombre_Nits = Nombre_Nits.drop_duplicates('NIT', keep = 'last')

dfconsolidado = dfconsolidado.drop(columns = ['NIT_PRESTADOR','NOMBRE_PRESTADOR'])

#%%
## 2.PREPARA
Tiempo_Parcial = datetime.now()



#%%
gasto = {}
columnas = ['Tipo Negocio','Folio','Fecha Contabilizacion','Sucursal','Plan','Tipo Contrato',
            'Carne','Tipo Identificacion Usuario','Nro. Identificacion','Valor Hospital',
            'Valor Cheques Hospital','Descuento General','Nombre','DESCRIPCION SERVICIO',
            'DESCRIPCION AGRUPACION','Diagnostico 2','Codigos_Diagnostico.Descripcion',
            'Procedimiento','Codigos_Procedimiento.Descripcion','Dias','Fecha Servicio',
            'Tipo Identificacion Institucion','NIT','Fecha Radicacion','Numero Factura',
            'TABLA','valor neto','Contrato final','Sucursal del contrato']

for archivo in glob.glob(path_entrada_archivo + '/*' + mes.title() + ' ' + anio + '.xlsx'):
    print('\n Cargando archivo: ',archivo[-20-len(mes)::])
    if 'HYC' in archivo:
        sheet = 'HYC'     
        a = 'HYC'
    else:
        sheet = 'Gasto médico'
        a = 'MPP'
    formatos = {'Tipo Negocio':str,'Folio':str,'Sucursal':str,'Plan':str,'Tipo Contrato':str,
                'Carne':str,'Nro. Identificacion':str,'Procedimiento':str,'Dias':str,
                'NIT':str,'Contrato final':str,'Sucursal del contrato':str}
    df = pd.read_excel(archivo, header = 0, sheet_name = sheet, usecols = columnas, dtype = formatos)
    df = df.dropna(subset = ['Tipo Negocio','Folio','Fecha Contabilizacion','Fecha Servicio'])
    df['archivo'] = a
    gasto[archivo] = df
    print('Archivo ', archivo[-20-len(mes)::], ' cargado \n')
    
dfgasto = pd.concat(gasto).reset_index(drop = True)
print("Tiempo de carga Gasto Medico: " , datetime.now()-Tiempo_Parcial)
print("Cantidad de Registros Cargados: ", len(dfgasto))


#%%

def CambioFormato(df, a = 'a'):
    df[a] = df[a].astype(str).str.strip()
    df[a] = np.where(df[a].str[-2::] == '.0', df[a].str[0:-2], df[a])
    df.loc[(df[a].str.contains('nan') == True),a] = np.nan
    return df[a]

dfsalida1 = dfgasto.copy()

dfsalida1['Folio'] = CambioFormato(dfsalida1, a = 'Folio')
dfsalida1['Carne'] = CambioFormato(dfsalida1, a = 'Carne')
dfsalida1['Nro. Identificacion'] = CambioFormato(dfsalida1, a = 'Nro. Identificacion')
dfsalida1['Procedimiento'] = CambioFormato(dfsalida1, a = 'Procedimiento')

#%%
def FormatoFecha(df, a = 'a'):
    if True in df[a].astype(str).str.contains('-'):
        df_a = df[df[a].astype(str).str.contains('-') == True].copy()
        df_a[a] = pd.to_datetime(df_a[a], format = '%Y-%m-%d')
        df_b = df[df[a].astype(str).str.contains('-') == False].copy()
        df_b[a] = pd.to_datetime(df_b[a], dayfirst = True, format = '%d/%m/%Y')
        df = pd.concat([df_a, df_b])
    else:
        df[a] =pd.to_datetime(df[a], dayfirst = True, format = '%d/%m/%Y')
        
    return df[a]

fechas = ['Fecha Radicacion','Fecha Contabilizacion','Fecha Servicio']

for i in fechas:
    print(i)
    dfsalida1[i] = FormatoFecha(dfsalida1, a = i)
#dfsalida1 = df1.loc[df1.apply(lambda x : int(str(x['Folio'])[0]) in [8] , axis= 1)]

dfsalida1['llave'] = (dfsalida1['Folio'].astype(str) +'-'+ dfsalida1['Carne'].astype(str)+'-' + dfsalida1['Nro. Identificacion'].astype(str) + '-' + dfsalida1['Fecha Radicacion'].astype(str))
dfproc1 = dfsalida1.copy()
dfproc1 = dfproc1.groupby(['llave'])['Procedimiento'].nunique().reset_index()
dfproc1.rename(columns = {'Procedimiento':'Cantidad_Proc_1'}, inplace = True)

dfsalida1['llave_cod'] = (dfsalida1['Folio'].astype(str) +'-'+ dfsalida1['Carne'].astype(str)+'-' + dfsalida1['Nro. Identificacion'].astype(str) + '-' + dfsalida1['Fecha Radicacion'].astype(str) +'-'+ dfsalida1['Procedimiento'].astype(str))
#dfsalida1 = dfsalida1.drop_duplicates(subset=(['llave']),keep='last')
#%%
## 4. PROCESO AL HISTORICO
dfsalida2 = dfconsolidado#.loc[dfconsolidado.apply(lambda x : int(str(x['FOLIO'])[0]) in [8] , axis= 1)]

dfsalida2['FECHA_RAD_FACT'] = pd.to_datetime(dfsalida2['FECHA_RAD_FACT'], dayfirst = True, format = '%Y-%m-%d')
dfsalida2 = dfsalida2.loc[:,['FOLIO','NRO_CONTRATO','NRO_IDENTIFICACION_BENEF','FECHA_RAD_FACT','COD_DIAGNOSTICO','COD_PROCEDIMIENTO','NOMBRE_PROCEDIMIENTO','CUPS_PRINCIPAL','CONCEPTO_HOSPITALARIO','TIPO_CUENTA','Dx_Egreso','Dx_Nombre']]
dfsalida2['NRO_CONTRATO'] = dfsalida2['NRO_CONTRATO'].fillna(0.0).astype('int64')

dfsalida2['FOLIO'] = CambioFormato(dfsalida2, a = 'FOLIO')
dfsalida2['NRO_CONTRATO'] = CambioFormato(dfsalida2, a = 'NRO_CONTRATO')
dfsalida2['NRO_IDENTIFICACION_BENEF'] = CambioFormato(dfsalida2, a = 'NRO_IDENTIFICACION_BENEF')
dfsalida2['COD_PROCEDIMIENTO'] = CambioFormato(dfsalida2, a = 'COD_PROCEDIMIENTO')

#%%
dfproc2 = dfsalida2.copy()
dfproc2['llave'] = (dfproc2['FOLIO'].astype(str) +'-'+dfproc2['NRO_CONTRATO'].astype(str)+'-' + dfproc2['NRO_IDENTIFICACION_BENEF'].astype(str) + '-' + dfproc2['FECHA_RAD_FACT'].astype(str))
dfproc2 = dfproc2.groupby(['llave'])['COD_PROCEDIMIENTO'].nunique().reset_index()
dfproc2.rename(columns = {'COD_PROCEDIMIENTO':'Cantidad_Proc_2'}, inplace = True)

dfsalida4 = dfsalida2.copy()
dfsalida4['llave_valida'] = (dfsalida4['FOLIO'].astype(str) +'-'+dfsalida4['NRO_CONTRATO'].astype(str)+'-' + dfsalida4['NRO_IDENTIFICACION_BENEF'].astype(str) + '-' + dfsalida4['FECHA_RAD_FACT'].astype(str))
dfsalida4 = dfsalida4.drop_duplicates(subset=(['llave_valida']),keep='last')
dfsalida4 = dfsalida4.loc[:,['llave_valida']]
dfsalida2['llave_cod'] = (dfsalida2['FOLIO'].astype(str) +'-'+dfsalida2['NRO_CONTRATO'].astype(str)+'-' + dfsalida2['NRO_IDENTIFICACION_BENEF'].astype(str) + '-' + dfsalida2['FECHA_RAD_FACT'].astype(str)+'-'+dfsalida2['COD_PROCEDIMIENTO'].astype(str))
dfsalida2 = dfsalida2.drop_duplicates(subset=(['llave_cod']),keep='last')

#%%
## 5. UNIÓN DEL CONSOLIDADO Y GASTO MEDICO
dfsalida3 = dfsalida1.merge(dfsalida2, on = 'llave_cod', how = 'left', validate = 'many_to_one')
dfsalida3 = dfsalida3.merge(dfsalida4, left_on = 'llave', right_on = 'llave_valida', how = 'left', validate = 'many_to_one')
dfsalida3 = dfsalida3.merge(dfproc1, on = 'llave', how = 'left', validate = 'many_to_one')
dfsalida3 = dfsalida3.merge(dfproc2, on = 'llave', how = 'left', validate = 'many_to_one')

#%%
dfsalida3['Folio'] = dfsalida3['Folio'].fillna(0.0)
dfsalida3['Folio'] = dfsalida3['Folio'].replace('nan',0.0)
dfsalida3['digito'] = dfsalida3.apply(lambda x : int(str(x['Folio'])[0]), axis = 1)


dfsalida3['Dx_Nombre'] = np.where(dfsalida3['Dx_Nombre'].isnull() == True,dfsalida3['Codigos_Diagnostico.Descripcion'],dfsalida3['Dx_Nombre'])
dfsalida3['Dx_Egreso'] = np.where(dfsalida3['Dx_Egreso'].isnull() == True,dfsalida3['Diagnostico 2'],dfsalida3['Dx_Egreso'])
dfsalida3['COD_DIAGNOSTICO'] = np.where(dfsalida3['COD_DIAGNOSTICO'].isnull() == True,dfsalida3['Diagnostico 2'],dfsalida3['COD_DIAGNOSTICO'])


## 6. CAMPOS DE VALIDACIÓN 
dfsalida3.loc[dfsalida3['digito'] != 8,'tipo_error'] = 'FOLIO DE OTRO TIPO'
dfsalida3.loc[(dfsalida3['tipo_error'].isnull() == True) & (dfsalida3['llave_valida'].isnull() == True),'tipo_error'] = 'FOLIO PERDIDO'
dfsalida3.loc[(dfsalida3['tipo_error'].isnull() == True) & (dfsalida3['FOLIO'].isnull() == True),'tipo_error'] = 'COD_PROCEDIMIENTO ERRONEO'
dfsalida3.loc[(dfsalida3['tipo_error'].isnull() == True),'tipo_error'] = 'SIN ERROR'

dfsalida3.loc[dfsalida3['Diagnostico 2'] == dfsalida3['COD_DIAGNOSTICO'],'COMPARA_DIAGNOSTICO'] = 'IGUALES'
dfsalida3.loc[dfsalida3['Diagnostico 2'] != dfsalida3['COD_DIAGNOSTICO'],'COMPARA_DIAGNOSTICO'] = 'DIFERENTES'
dfsalida3.loc[dfsalida3['COD_DIAGNOSTICO'].isnull() == True,'COMPARA_DIAGNOSTICO'] = 'ERROR'

dfsalida3.loc[dfsalida3['Procedimiento'] == dfsalida3['COD_PROCEDIMIENTO'],'COMPARA_PROCEDIMIENTO'] = 'IGUALES'
dfsalida3.loc[dfsalida3['Procedimiento'] != dfsalida3['COD_PROCEDIMIENTO'],'COMPARA_PROCEDIMIENTO'] = 'DIFERENTES'
dfsalida3.loc[dfsalida3['COD_PROCEDIMIENTO'].isnull() == True,'COMPARA_PROCEDIMIENTO'] = 'ERROR'

dfsalida3.loc[dfsalida3['Cantidad_Proc_1'] == dfsalida3['Cantidad_Proc_2'],'REVISAR_DETALLE'] = 'NO'
dfsalida3.loc[dfsalida3['Cantidad_Proc_1'] != dfsalida3['Cantidad_Proc_2'],'REVISAR_DETALLE'] = 'SI'
dfsalida3.loc[dfsalida3['Cantidad_Proc_2'].isnull() == True,'REVISAR_DETALLE'] = 'ERROR'

dfsalida3.drop(columns=['llave','llave_cod','FOLIO','NRO_CONTRATO','NRO_IDENTIFICACION_BENEF', 'llave_valida', 'Cantidad_Proc_1', 'Cantidad_Proc_2','digito'],inplace = True)
#%%

Campos_Texto = ['Carne','NIT','Procedimiento','Folio','Nro. Identificacion','Contrato final']

for i in Campos_Texto:
    dfsalida3[i] = CambioFormato(dfsalida3, a = i)


Nombre_Nits['NIT'] = CambioFormato(Nombre_Nits, a = 'NIT')

dfsalida3['valor neto'] = dfsalida3['valor neto'].astype(float)
dfsalida3 = dfsalida3.merge(Nombre_Nits, how = 'left', on = 'NIT')
#%%
print('Resumen: \n')

print('Los códigos de diagnósticos ANTES de éste proceso eran: ', '{:,}'.format(dfsalida3['Diagnostico 2'].isnull().value_counts()[0]))
print('Los códigos de diagnósticos DESPUÉS de éste proceso son: ', '{:,}'.format(dfsalida3['Dx_Egreso'].isnull().value_counts()[0]))
porc_inicial = str(round(dfsalida3['Diagnostico 2'].isnull().value_counts()[0]/dfsalida3.shape[0]*100,1))
porc_final = str(round(dfsalida3['Dx_Egreso'].isnull().value_counts()[0]/dfsalida3.shape[0]*100,1))

print('Es decir que se pasó de un ', porc_inicial, '% de datos a un ', porc_final,  '% de datos \n')
#gm_2023['valor neto'] = 
resumen = dfsalida3.copy()
resumen = resumen.groupby(['archivo']).agg({'Valor Hospital':'sum','Valor Cheques Hospital':'sum','valor neto':'sum'})
valores = ['valor neto','Valor Hospital','Valor Cheques Hospital']
for i in valores:
    resumen[i] = '$' + resumen[i].map('{:,.0f}'.format)
print(resumen)

#%%
## 7. EXPORTAR DATOS
print('\n Guardando archivo HYC')
os.chdir(path_salida)
writer = pd.ExcelWriter('GM HYC PRUEBA ' + mes.upper() + ' ' + anio + '.xlsx',engine = 'xlsxwriter', datetime_format='d/mm/yyyy')
dfsalida4 = dfsalida3[dfsalida3['archivo'] == 'HYC']
dfsalida4 = dfsalida4.drop(columns = {'archivo'})
dfsalida4.to_excel(writer,sheet_name = 'Data',index = False, encoding = 'latin-1')
workbook = writer.book
worksheet = writer.sheets['Data']
writer.save()
print('Archivo HYC guardado \n')

print(' Guardando archivo MPP')
os.chdir(path_salida)
writer = pd.ExcelWriter('GM MPP PRUEBA ' + mes.upper() + ' ' + anio + '.xlsx',engine = 'xlsxwriter', datetime_format='d/mm/yyyy')
dfsalida4 = dfsalida3[dfsalida3['archivo'] == 'MPP']
dfsalida4 = dfsalida4.drop(columns = {'archivo'})
dfsalida4.to_excel(writer,sheet_name = 'Data',index = False, encoding = 'latin-1')
workbook = writer.book
worksheet = writer.sheets['Data']
writer.save()
print('Archivo MPP guardado \n')

print("Tiempo del Proceso: " , datetime.now()-Tiempo_Total)
