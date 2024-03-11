# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:40:30 2022

@author: jcgarciam
"""

"""
El siguiente codigo se utiliza para crear los archivos del informe Gasto Medico Contable el cual se debe correr mensualmente.
Este codigo se alimenta de 6 archivos principales, los cuales se encuentran en el archivo excel que genera el codigo 
ConsultasMPP. Los archivos son: CCM, CCH, DCM, DDL, BLA y Medicamentos. Tambien, este informe se alimenta de una lista de codigos 
que se encuentran en el input de la carpeta Input que conforma este programa. Por ultimo, existe dos archivos en la ruta 
\\dc1pvfnas1\Autos\Soat_Y_ARL\Backup_Brian\Cierre\1. Contratos_salud los cuales se utilizan para al final obtener las sucursales 
de los archivos finales. 

Las salidas de este programa entrega 2 reportes de gasto médico, uno para MPP y otro para HYC. 

"""
import pandas as pd
from Extract import ExtraccionBases
from Transform_Joins import CreacionNuevasTablas
from Transform_New_Fields import NuevosCampos
from Transform_New_Fields import GroupByValores
from datetime import datetime

#%%
Tiempo_Total = datetime.now()

path_input1 = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\Gasto Medico Contable\Input'
Anio = input('Ingrese el año del archivo del cierre: ')
Mes = input('Ingrese el mes del archivo de cierre, ejemplo: Mayo: ')
Mes = Mes.title()
path_input3 = r'\\dc1pvfnas1\Autos\Soat_Y_ARL\Pagos_Arl_Salud\Cierre\1. Contratos_salud'
path_salida = r'D:\DATOS\Users\jcgarciam\OneDrive - AXA Colpatria Seguros\Documentos\Informes\Gasto Medico Contable\Output/{}'

#%%
#Extraccion de los archivos
print('Extrayendo archivos')
CCM, CCH, DCM, DDL, BLA, Medicamentos, Codigos_Procedimiento, Codigos_Servicio, Codigos_Diagnostico = ExtraccionBases(path_input1,path_salida)

print('Archivos extraidos')
#Creacion de nuevas tablas
print('Creacion de la tablas HYC y MPP')
HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED = CreacionNuevasTablas(CCM, CCH, DCM, DDL, BLA, Medicamentos, Codigos_Procedimiento, Codigos_Servicio, Codigos_Diagnostico)
print('Tablas HYC y MPP creadas')
#%%

#Creacion de nuevos camopos
print('Creando nuevos campos')
HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED, MPP_total_acum_CCH = NuevosCampos(HyC_total_acum_CCH, HyC_total_acum_DCM, HyC_total_acum_DDL, MPP_total_acum_DCM, MPP_total_acum_DDL, MPP_total_acum_MED)
print('Nuevos campos creados')

#%%
#Se ordenas las columnas de las tablas
print('Reordenando las columnas de las tablas')
HyC_total_acum_CCH = HyC_total_acum_CCH[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Valor_Hospital', 'Valor_Cheques_Hospital','Descuento_General',
                                         'Nombre','DESCRIPCION SERVICIO','DESCRIPCION AGRUPACION','Diagnostico_Principal',
                                         'DESCRIPCION','Procedimiento','Descripcion','dias','Fecha_Servicio',
                                         'Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura','Tabla']]


HyC_total_acum_DCM = HyC_total_acum_DCM[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Valor_Consulta','Valor_cheque_consulta','Descuento','Expr1','DESCRIPCION SERVICIO',
                                         'DESCRIPCION AGRUPACION','Diagnostico_Ingreso','DESCRIPCION','Procedimiento','Descripcion',
                                         'dias','Fecha_Servicio','Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura',
                                         'Tabla']]
                                         
HyC_total_acum_DDL = HyC_total_acum_DDL[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Suma_Total_Servicio','Vales','Descuento','Descripcion','DESCRIPCION SERVICIO',
                                         'DESCRIPCION AGRUPACION','dx','descripcion dx','Procedimiento','Descripcion',
                                         'dias','Fecha_Servicio','Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura',
                                         'Tabla']]         

     
MPP_total_acum_CCH = MPP_total_acum_CCH[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Valor_Hospital', 'Valor_Cheques_Hospital','Descuento_General',
                                         'Nombre','DESCRIPCION SERVICIO','DESCRIPCION AGRUPACION','Diagnostico_Principal',
                                         'DESCRIPCION','Procedimiento','Descripcion','dias','Fecha_Servicio',
                                         'Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura','Tabla']]

MPP_total_acum_DCM = MPP_total_acum_DCM[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Suma_Valor_Consulta','Suma_Valor_Cheque_Consulta','Descuento','Nombre','DESCRIPCION SERVICIO',
                                         'DESCRIPCION AGRUPACION','Diagnostico_Ingreso','DESCRIPCION','Procedimiento','Descripcion',
                                         'dias','Fecha_Servicio','Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura',
                                         'Tabla']]

MPP_total_acum_DDL = MPP_total_acum_DDL[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo_Contrato','Numero_Carne','Tipo_Identificacion','Numero_Identificacion',
                                         'Suma_Total_Servicio','Vales','Descuento','Nombre','DESCRIPCION SERVICIO',
                                         'DESCRIPCION AGRUPACION','dx','descripcion dx','Procedimiento','Descripcion',
                                         'dias','Fecha_Servicio','Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura',
                                         'Tabla']]   

MPP_total_acum_MED = MPP_total_acum_MED[['Tipo_Documento','Folio','Fecha_Contabilizacion','Sucursal','Plan',
                                         'Tipo Contrato','CarneUsuario','TipIdUsuario','NunIdUsuario',
                                         'Suma_Vlr_Tot_Medica','Val cheques','Val descuento','Nombre','DESCRIPCION SERVICIO',
                                         'DESCRIPCION AGRUPACION','dx','descripcion dx','CodMedicamento','Medicamento',
                                         'CantiMedica','FecServicio','Tipo_Iden_Inst','NIT','Fecha_Folio','Numero_factura',
                                         'Tabla']]   
print('Columnas ordenadas')
#Los nuevos nombres de las tablas
Nombres_Finales = ['Tipo_Negocio','Folio','Fecha_Contabilizacion','Sucursal','Plan','Tipo_Contrato','Carne',
                   'Tipo_Identificacion_Usuario','Nro_Identificacion','Valor_Hospital','Valor_Cheques_Hospital',
                   'Descuento_General','Nombre','Descripcion_Servicio','Descripcion_Agrupacion','Diagnostico_2',
                   'Codigos_Diagnostico_Descripcion','Procedimiento','Codigos_Procedimiento_Descripcion','Dias',
                   'Fecha_Servicio','Tipo_Identificacion_Institucion','NIT','Fecha_Radicacion','Numero_Factura','Tabla']


#%%
#Se reemplazan los nombres de las tablas por los nuevos
print('Homegenizando los nombres de las tablas')
HyC_total_acum_CCH.columns = Nombres_Finales
HyC_total_acum_DCM.columns = Nombres_Finales
HyC_total_acum_DDL.columns = Nombres_Finales
MPP_total_acum_CCH.columns = Nombres_Finales
MPP_total_acum_DCM.columns = Nombres_Finales
MPP_total_acum_DDL.columns = Nombres_Finales 
MPP_total_acum_MED.columns = Nombres_Finales
print('Nombres homogenizados')


#%%
#Se agrupan los datos de 5 tablas
print('Agrupando los registros de las tablas')
HyC_total_acum_DCM = GroupByValores(HyC_total_acum_DCM, Nombres_Finales)
HyC_total_acum_DDL = GroupByValores(HyC_total_acum_DDL, Nombres_Finales)
MPP_total_acum_DCM = GroupByValores(MPP_total_acum_DCM, Nombres_Finales)
MPP_total_acum_DDL = GroupByValores(MPP_total_acum_DDL, Nombres_Finales) 
MPP_total_acum_MED = GroupByValores(MPP_total_acum_MED, Nombres_Finales)
print('Registros agrupados')


#%%
#Se crean los reportes que entrega este codigo
print('Creando los archivos finales de gasto medico MPP y HYC')
Data_HYC = [HyC_total_acum_CCH,HyC_total_acum_DCM,HyC_total_acum_DDL]
Data_MPP = [MPP_total_acum_CCH,MPP_total_acum_DCM,MPP_total_acum_DDL,MPP_total_acum_MED]
df_HYC = pd.concat(Data_HYC).reset_index(drop = True)
df_MPP = pd.concat(Data_MPP).reset_index(drop = True)

df_HYC['Valor_Neto'] = df_HYC['Valor_Hospital'] - df_HYC['Valor_Cheques_Hospital']/1.05 - df_HYC['Descuento_General']
df_MPP['Valor_Neto'] = df_MPP['Valor_Hospital'] - df_MPP['Valor_Cheques_Hospital']/1.05 - df_MPP['Descuento_General']

df_HYC['Carne'] = pd.Categorical(df_HYC['Carne'].apply(str))
df_MPP['Carne'] = pd.Categorical(df_MPP['Carne'].apply(str))

df_HYC['Contrato_Final'] =  df_HYC['Carne'].str[0:8]
df_MPP['Contrato_Final'] =  df_MPP['Carne'].str[0:8]

#Se extraen los codigos de las sucursales de la ruta antes mencionada
sucursales_HYC = pd.read_excel(path_input3+'\Contratos Hyc Sucusal.xlsx', sheet_name='BD', usecols=['Contrato','CODIGO SUCURSAL PRINCIPAL'])
sucursales_HYC = sucursales_HYC.drop_duplicates('Contrato', keep='last')

sucursales_MPP = pd.read_excel(path_input3+'\Contratos Mpp Sucursal.xlsx', sheet_name='HISTORICO', usecols=['Contrato 1','Cod. Regional'])
sucursales_MPP = sucursales_MPP.drop_duplicates('Contrato 1', keep='last')
#%%
# Se le asigna la sucursal final a los registros por el campo Contrato_Final
df_HYC['Contrato_Final'] = pd.Categorical(df_HYC['Contrato_Final'].apply(int))
df_MPP['Contrato_Final'] = pd.Categorical(df_MPP['Contrato_Final'].apply(int))

df_HYC = df_HYC.merge(sucursales_HYC, how = 'left', left_on = 'Contrato_Final', right_on = 'Contrato')
df_MPP = df_MPP.merge(sucursales_MPP, how = 'left', left_on = 'Contrato_Final', right_on = 'Contrato 1')
#%%
df_HYC = df_HYC.loc[:,df_HYC.columns != 'Contrato']
df_MPP = df_MPP.loc[:,df_MPP.columns != 'Contrato 1']

df_HYC = df_HYC.rename(columns = {'CODIGO SUCURSAL PRINCIPAL':'Sucursal_Final'})
df_MPP = df_MPP.rename(columns = {'Cod. Regional':'Sucursal_Final'})
print('Gasto medico MPP y HYC creados')
#%%
#Se guardan los archivos finales en el Ouput de este codigo
print('Guardando los informes finales')
dir_db = path_salida.format('GM HyC '+ Mes + ' ' + Anio + '.xlsx')
writer= pd.ExcelWriter(dir_db)

df_HYC.to_excel(writer, index = False, sheet_name = 'HYC')

writer.save()
writer.close()

dir_db = path_salida.format('GM MPP '+ Mes + ' ' + Anio + '.xlsx')
writer= pd.ExcelWriter(dir_db)

df_MPP.to_excel(writer, index = False, sheet_name = 'MPP')

writer.save()
writer.close()
print('Informes guardados')

print("Tiempo del Proceso: " , datetime.now()-Tiempo_Total)
print('Proceso finalizado con exito. Presionar ENTER para salir')





