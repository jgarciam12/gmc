 # -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:16:22 2022

@author: jcgarciam
"""
"""
Este codigo esta creado para alistar los reportes MPP, los cuales se descargan del aplicativo SIRUP con fecha del 26 del mes anterior
al 25 del mes siguiente, el cual está relacionado al mes de cierre, es decir si vamos a hacer el cierre de junio las
bases se deben descargar del 26 de mayo al 25 de junio. Estas bases tienen nombre como ReporteX1_CCM..., ReporteX2_CCH...,
ReporteX3_CPT..., ReporteX4_DCM..., ReporteX5_DDL..., ReporteX6_BLA... y ReporteX9_CCM_Medicamentos. Otro archivo clave en
el procedimiento es el que se encuentra el archivo zip Cierre Mes Año, donde el Mes y Anio hacen referencia a la fecha en 
que se hace el reporte, la ruta  es \\dc1pvfnas1\Autos\Soat_Y_ARL\Backup_Brian\Cierre\.
Al final este codigo entrega una archivo excel con los hojas de los reportes y una resumen donde se puede analizar
la validez de la informacion extraida. 
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime

Tiempo_Total = datetime.now()

path_input1 = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\Gasto Medico Contable\Input'
Anio = input('Ingrese el año del archivo del cierre: ')
Mes = input('Ingrese el mes del archivo de cierre, ejemplo: Mayo: ')
Mes = Mes.title()
path_input2 = r'\\dc1pvfnas1\Autos\Soat_Y_ARL\Pagos_Arl_Salud\Cierre' + '/' + Anio +'/' + Mes +'\Salud\Archivos_contables'
path_salida = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\Gasto Medico Contable\Output/{}'

print('Extrayendo archivos')
files_SIRUP = os.listdir(path_input1 + '\Reportes SIRUP')
    
#Extracción de archivos MPP
Data = {} #En esta base van los reportes 

for file in files_SIRUP:
    df = pd.read_csv(path_input1 + '\Reportes SIRUP/' + file, delimiter='|', header=0)        
    Data[file] = df
        
Name_Data = list(Data.keys())
    
CCM = Data[Name_Data[0]]
CCH = Data[Name_Data[1]]
CPT = Data[Name_Data[2]]
DCM = Data[Name_Data[3]]
DDL = Data[Name_Data[4]]
BLA = Data[Name_Data[5]]
Medicamentos = Data[Name_Data[6]]

def CambioFormato(df, a = 'a'):
    df[a] = df[a].astype(str).str.strip().str.strip('\x02').str.strip('')
    df[a] = np.where(df[a].str[-2::] == '.0', df[a].str[0:-2], df[a])
    df[a] = np.where(df[a] == 'nan', np.nan, df[a])
    
    return df[a]
    
    
Cierre = pd.read_excel(path_input2 + '\Cierre BH ' + Mes.upper() + ' ' + Anio + ' MPP y HyC.xlsx', sheet_name='Detalle', usecols=['CONSECUTIVO'])
print('Archivos extraidos')            
    
#Creacion de nuevos campos
print('Creando nuevos campos')
CCM['Valor'] = CCM['CCM_NETO-FACT'] + CCM['CCM_VALOR-VALES'] + CCM['CCM_COPAGO'] + CCM['CCM_MODERA']
CCM['vlr_neto_contable'] = (CCM['CCM_SUMTOT'] - CCM['CCM_DESGENERAL'])-(CCM['CCM_VALOR-VALES'] / 1.05) 
CCM = CCM.assign(Tipo_Iden_Inst=CCM['CCM_TIPO_DOC'])
    
CCH['CCH-PROCED'] = pd.Categorical(CCH['CCH-PROCED'].apply(str))
CCH['Procedimiento'] = CCH['CCH-PROCED'].str[0:7] 
    
DCM['DCM_PROCEDIMIENTO'] = pd.Categorical(DCM['DCM_PROCEDIMIENTO'].apply(str))
DCM['Procedimiento'] = DCM['DCM_PROCEDIMIENTO'].str[0:7]
DCM['Tipo_Ident_Medico'] = np.nan
    
DDL[['Tipo_Ident_Medico','Numero_Ident_Medico']] = np.nan
    
BLA['BLA_CODSERV'] = pd.Categorical(BLA['BLA_CODSERV'].apply(str))
BLA['Procedimiento'] = BLA['BLA_CODSERV'].str[0:7]
print('Campos creaods')    

#Se renombran algunos campos de las bases
print('Renombrando las columnas')
CCM = CCM.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                        'CCM_TIPO_CUENTA':'Tipo_Cuenta','CCM_FECHA_CONTA':'Fecha_Contabilizacion',
                        'CCM_NIT':'NIT','CCM-NUMFAC':'Numero_factura','CCM-FECFAC':'Fecha_Factura',
                        'CCM_FECHA_FOLIO':'Fecha_Folio','CCM_NETO-FACT':'Valor_Neto_Factura',
                        'CCM_VALOR-VALES':'Valor_Cheques','CCM_COPAGO':'Copago','CCM_DESGENERAL':'Descuento_General',
                        'CCM_MODERA':'Moderadora','CCM_SUMTOT':'Suma_Total'})

CCH = CCH.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                       'CCM_FECHA_CONTA':'Fecha_Contabilizacion','CCH_CORR':'Correlativo',
                       'CCH_FECHA_SERV':'Fecha_Servicio','CCH_VALTOT':'Valor_Hospital',
                       'CCH_VALCHEQUE':'Valor_Cheques_Hospital','CCH_PAGOPAC':'Copago_hospital',
                       'CCM_DESCUENTO':'Descuento_Hospital','CCH_MODERA':'Moderadora_Hospital',
                       'CCH_TIPIDE':'Tipo_Identificacion','CCH_NUMIDE':'Numero_Identificacion',
                       'CCH_NROCARNE':'Numero_Carne','CCH_SERVCIO':'servicio','CCH-DIAG-1':'Diagnostico_Ingreso',
                       'CCH-DIAG-2':'Diagnostico_Principal','CCH-DIAS':'dias','CCH-TIPCONTI':'Tipo_Contingencia',
                       'CCH-CLASEATEN':'Clase_Atencion','CCH-TIPOATEN':'Tipo_Atencion','CCH-TIPOSERVIC':'Tipo_Servicio'})
    
CPT = CPT.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                        'CCM_FECHA_CONTA':'Fecha_Contabilizacion','CCH_CORR':'Correlativo',
                        'CPT-CONCEPTO':'Concepto','CPT-VALOR':'Valor','CPT-CANTIDAD':'Cantidad',
                        'CPT-PORDESC':'Por_Descuento','CPT-DESCUENTOS':'Descuento'})
    
DCM = DCM.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                        'CCM_FECHA_CONTA':'Fecha_Contabilizacion','DCM_CONSECUTIVO':'Consecutivo',
                        'DCM_CORR':'Correlativo','DCM_FECHA':'Fecha_Servicio','DCM_VALOR':'Valor_Consulta',
                        'DCM_VALCHEQUE':'Valor_cheque_consulta','DCM_COPAGO':'Copago_Consulta',
                        'DCM_MODERA':'Moderadora_Consulta','DCM_TIPIDE':'Tipo_Identificacion',
                        'DCM_NUMIDE':'Numero_Identificacion','DCM_CARNE':'Numero_Carne',
                        'DCM_SERV':'Servicio','DCM_DIAG1':'Diagnostico_Ingreso','DCM_DIAG2':'Diagnostico_Principal',
                        'DCM_TIPCONTI':'Tipo_Contigencia','DCM_CANTIDAD':'Cantidad',
                        'ADE_NCODE':'Numero_Ident_Medico','DCM_CLASEATEN':'Clase_Atencion'})
    
DDL = DDL.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                       'CCM_FECHA_CONTA':'Fecha_Contabilizacion','DDI_CONSECUTIVO':'Consecutivo',
                       'DDI_CORR':'Correlativo','DDI_FECHA':'Fecha_Servicio','DDI_VALOR':'Valor_Diagnostico',
                       'DDI_VALCHEQUE':'Valor_Cheque_Diagnostico','DDI_COPAGO':'Copago_Diagnostico',
                       'DDI_MODERA':'Moderadora_Diagnostico','DDI_TIPIDE':'Tipo_Identificacion',
                       'DDI_NUMIDE':'Numero_Identificacion','DDI_CARNE':'Numero_Carne',
                       'DDI_SERVICIO':'Servicio','DDI_DIAG1':'Diagnostico_Ingreso','DDI_TIPCONTI':'Tipo_Contingencia',
                       'DCM_CANTIDAD':'Cantidad','DDI_CLASEATEN':'Clase_Atencion'})
    
BLA = BLA.rename(columns = {'CCM_SUCURSAL':'Sucursal','CCM_FOLIO':'Folio','CCM_TIPO_DOC':'Tipo_Documento',
                        'CCM_FECHA_CONTA':'Fecha_Contabilizacion','DDI_CONSECUTIVO':'Consecutivo',
                        'DDI_CORR':'Correlativo','BLA_CONSEC':'Consecutivos','BLA_CANT':'Cantidad',
                        'BLA-VALUNI':'Valor_Unitario','BLA-TOTSERV':'Total_Servicio','BLA-COPAGO':'Copago'})
    
print('Columnas renombradas')
#Cambiamos el formato de las columnas que tienen una fecha, ya que aparecen AAAA/MM/DD
#y se necesitan en formato DD/MM/AAAA
    
#Primero los pasamos a tipo fecha
print('Cambiando los formatos de las columnas fechas')
CCM['Fecha_Contabilizacion'] = pd.to_datetime(CCM['Fecha_Contabilizacion'])
CCM['Fecha_Factura'] = pd.to_datetime(CCM['Fecha_Factura'])
CCM['Fecha_Folio'] = pd.to_datetime(CCM['Fecha_Folio'])
CCH['Fecha_Contabilizacion'] = pd.to_datetime(CCH['Fecha_Contabilizacion'])
CCH['Fecha_Servicio'] = pd.to_datetime(CCH['Fecha_Servicio'])
CPT['Fecha_Contabilizacion'] = pd.to_datetime(CPT['Fecha_Contabilizacion'])
DCM['Fecha_Contabilizacion'] = pd.to_datetime(DCM['Fecha_Contabilizacion'])
DCM['Fecha_Servicio'] = pd.to_datetime(DCM['Fecha_Servicio'])
DDL['Fecha_Contabilizacion'] = pd.to_datetime(DDL['Fecha_Contabilizacion'])
DDL['Fecha_Servicio'] = pd.to_datetime(DDL['Fecha_Servicio'])
BLA['Fecha_Contabilizacion'] = pd.to_datetime(BLA['Fecha_Contabilizacion'])
Medicamentos['FechaCon'] = pd.to_datetime(Medicamentos['FechaCon'])

#Ahora cambiamos el orden de la fecha a DD/MM/AAAA
CCM['Fecha_Contabilizacion'] = CCM['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
CCM['Fecha_Factura'] = CCM['Fecha_Factura'].dt.strftime('%d/%m/%Y')
CCM['Fecha_Folio'] = CCM['Fecha_Folio'].dt.strftime('%d/%m/%Y')
CCH['Fecha_Contabilizacion'] = CCH['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
CCH['Fecha_Servicio'] = CCH['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
CPT['Fecha_Contabilizacion'] = CPT['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
DCM['Fecha_Contabilizacion'] = DCM['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
DCM['Fecha_Servicio'] = DCM['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
DDL['Fecha_Contabilizacion'] = DDL['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
DDL['Fecha_Servicio'] = DDL['Fecha_Servicio'].dt.strftime('%d/%m/%Y')
BLA['Fecha_Contabilizacion'] = BLA['Fecha_Contabilizacion'].dt.strftime('%d/%m/%Y')
Medicamentos['FechaCon'] = Medicamentos['FechaCon'].dt.strftime('%d/%m/%Y')

print('Formatos de fechas cambiados')    
    
#Guardamos las bases de datos con un orden en las columnas
print('Reordenando las columnas de las tablas')
CCM = CCM[['Sucursal','Folio','Tipo_Documento','Tipo_Cuenta','Fecha_Contabilizacion','Tipo_Iden_Inst',
          'NIT','Numero_factura','Fecha_Factura','Fecha_Folio','Valor','Valor_Neto_Factura','Valor_Cheques',
          'Copago','Descuento_General','Moderadora','Suma_Total','vlr_neto_contable']]
    
CCH = CCH[['Sucursal','Folio','Tipo_Documento','Fecha_Contabilizacion','Correlativo','Fecha_Servicio',
           'Valor_Hospital','Valor_Cheques_Hospital','Copago_hospital','Descuento_Hospital','Moderadora_Hospital',
           'Tipo_Identificacion','Numero_Identificacion','Numero_Carne','servicio','Procedimiento','Diagnostico_Ingreso',
           'Diagnostico_Principal','dias','Tipo_Contingencia','Clase_Atencion','Tipo_Atencion','Tipo_Servicio']]
    
CPT = CPT[['Sucursal','Folio','Tipo_Documento','Fecha_Contabilizacion','Correlativo','Concepto','Valor',
           'Cantidad','Por_Descuento','Descuento']]
    
    
DCM = DCM[['Sucursal','Folio','Tipo_Documento','Fecha_Contabilizacion','Consecutivo','Correlativo',
           'Fecha_Servicio','Valor_Consulta','Valor_cheque_consulta','Copago_Consulta','Moderadora_Consulta',
           'Tipo_Identificacion','Numero_Identificacion','Numero_Carne','Servicio','Procedimiento','Diagnostico_Ingreso',
           'Diagnostico_Principal','Tipo_Contigencia','Cantidad','Tipo_Ident_Medico','Numero_Ident_Medico','Clase_Atencion']]
    
    
DDL = DDL[['Sucursal','Folio','Tipo_Documento','Fecha_Contabilizacion','Consecutivo','Correlativo',
           'Fecha_Servicio','Valor_Diagnostico','Valor_Cheque_Diagnostico','Copago_Diagnostico',
           'Moderadora_Diagnostico','Tipo_Identificacion','Numero_Identificacion','Numero_Carne',
           'Servicio','Diagnostico_Ingreso','Tipo_Contingencia','Cantidad','Clase_Atencion','Tipo_Ident_Medico',
           'Numero_Ident_Medico']]
    
BLA = BLA[['Sucursal','Folio','Tipo_Documento','Fecha_Contabilizacion','Consecutivo','Correlativo','Procedimiento',
           'Consecutivos','Cantidad','Valor_Unitario','Total_Servicio','Copago']]
print('Columnas reordenadas\n')  

Medicamentos['CantiMedica'] = Medicamentos['CantiMedica'].astype(str).str.replace(',','.').astype(float).astype(int)

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

Cierre['CONSECUTIVO'] = CambioFormato(Cierre, a = 'CONSECUTIVO')

def BuscarFolioEnCierre(df, Cierre):
    df = df[df['Folio'].isin(Cierre['CONSECUTIVO'])]
    return df

print('Cruzando los archivos MPP con el archivo de Cierre BH')
CCM = BuscarFolioEnCierre(CCM, Cierre)
CCH = BuscarFolioEnCierre(CCH, Cierre)
CPT = BuscarFolioEnCierre(CPT, Cierre)
DCM = BuscarFolioEnCierre(DCM, Cierre)
DDL = BuscarFolioEnCierre(DDL, Cierre)
BLA = BuscarFolioEnCierre(BLA, Cierre)
print('Archivos cruzados')
    
#%%
print('Guardando las tablas finales')
Tablas_Finales = [CCM,CCH,CPT,DCM,DDL,BLA,Medicamentos] 
Tablas_Nombres = ['CCM','CCH','CPT','DCM','DDL','BLA','Medicamentos'] 

dir_db = path_salida.format('DB_MOD_MPP.xlsx')
with pd.ExcelWriter(dir_db, mode='a', engine = 'openpyxl') as writer:
    WorkBook = writer.book
    try:
        for i in range(len(Tablas_Finales)):    
            print(Tablas_Nombres[i])
            WorkBook.remove(WorkBook[Tablas_Nombres[i]])  
    finally:
        for i in range(len(Tablas_Finales)):    
            Tablas_Finales[i].to_excel(writer, index = False, sheet_name = Tablas_Nombres[i])
            
writer.save()
writer.close()
print('Tablas finales guardadas')

print("Tiempo del Proceso: " , datetime.now()-Tiempo_Total)
print('Proceso finalizado con exito. Presionar ENTER para salir')

