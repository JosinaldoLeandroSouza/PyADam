#PyADam Pre-Processing
"""
Created on 30/12/2023
DiaolgBox code with ABAQUS/CAE
@author: Josinaldo Leandro de Souza
"""

from rsg.rsgGui import *
from abaqusConstants import INTEGER, FLOAT

# Connection with script
dialogBox = RsgDialog(title='PyADam - Pre Processing', kernelModule='PyADam_script', kernelFunction='DAM_ret', includeApplyBtn=True, includeSeparator=True, okBtnText='OK', applyBtnText='Apply', execDir=thisDir)
RsgTabBook(name='TabBook_1', p='DialogBox', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')

# Input Data Tab Interface
RsgTabItem(name='TabItem_1', p='TabBook_1', text='Input data')
RsgTextField(p='TabItem_1', fieldType='String', ncols=12, labelText='Name section', keyword='part', default='Barragem')
RsgSeparator(p='TabItem_1')
RsgLabel(p='TabItem_1', text='Dam Section Points', useBoldFont=True)
RsgHorizontalFrame(name='HFrame_1', p='TabItem_1', layout='LAYOUT_FILL_X', pl=0, pr=0, pt=0, pb=0)
RsgIcon(p='HFrame_1', fileName=r'juca-Model.png')
RsgTable(p='HFrame_1', numRows=5, columnData=[('X', 'Float', 50), ('Y', 'Float', 50)], showRowNumbers=True, showGrids=True, keyword='Pontos', popupFlags='AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE')
RsgLabel(p='TabItem_1', text='Maximum number of points for the dam section is 25 points.', useBoldFont=False)
RsgSeparator(p='TabItem_1')
RsgGroupBox(name='GroupBox_5', p='TabItem_1', text='Dam Gallery', layout='LAYOUT_FILL_X')
RsgLabel(p='GroupBox_5', text='Dam Gallery Points', useBoldFont=True)
RsgTable(p='GroupBox_5', numRows=2, columnData=[('X', 'Float', 50), ('Y', 'Float', 50)], showRowNumbers=True, showGrids=True, keyword='Pontos2', popupFlags='AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_READ_FROM_FILE|AFXTable.POPUP_WRITE_TO_FILE')
RsgLabel(p='GroupBox_5', text='If the gallery does not exist, leave the table empty.', useBoldFont=False)

# Physical Data Tab Interface
RsgTabItem(name='TabItem_2', p='TabBook_1', text='Physical Data')
RsgGroupBox(name='GroupBox_6', p='TabItem_2', text='Physical Data of the Dam Material', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgTextField(p='GroupBox_6', fieldType='String', ncols=40, labelText='Name of Dam Material', keyword='material1', default='Concreto CCR')
RsgTextField(p='GroupBox_6', fieldType='Float', ncols=20, labelText='Dam Material Density (kN/m3)', keyword='Rho_ccr', default='2120')
RsgTextField(p='GroupBox_6', fieldType='Float', ncols=20, labelText='Modulus of Elasticity of the Dam Material (kN/m2)', keyword='Es_ccr', default='24464000000')
RsgTextField(p='GroupBox_6', fieldType='Float', ncols=10, labelText='Poissons Ratio', keyword='nu_ccr', default='0.2')
RsgTextField(p='GroupBox_6', fieldType='Float', ncols=12, labelText='Material Permeability (m/s)', keyword='Ks_ccr', default='0.000000001')
RsgTextField(p='GroupBox_6', fieldType='Float', ncols=12, labelText='Void Index', keyword='iv_ccr', default='0.02')
RsgGroupBox(name='GroupBox_7', p='TabItem_2', text='Physical Data of the Foundation Material', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgTextField(p='GroupBox_7', fieldType='String', ncols=33, labelText='Name of Foundation Material', keyword='material2', default='Rocha Granitica')
RsgTextField(p='GroupBox_7', fieldType='Float', ncols=15, labelText='Rock Material Density (kN/m3)', keyword='Rho_rocha', default='2700')
RsgTextField(p='GroupBox_7', fieldType='Float', ncols=20, labelText='Modulus of Elasticity of the Foundation Material (kN/m2)', keyword='Es_rocha', default='40000000000')
RsgTextField(p='GroupBox_7', fieldType='Float', ncols=12, labelText='Poissons Tation', keyword='nu_rocha', default='0.2')
RsgTextField(p='GroupBox_7', fieldType='Float', ncols=12, labelText='Foundation Material Permeability (m/s)', keyword='Ks_rocha', default='0.000000000001')
RsgTextField(p='GroupBox_7', fieldType='Float', ncols=5, labelText='Void Index', keyword='iv_rocha', default='0.02')

# Solution Stage Tab Interface
RsgTabItem(name='TabItem_3', p='TabBook_1', text='Solution Stage')
RsgGroupBox(name='GroupBox_12', p='TabItem_3', text='Global Coordinate System', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgIcon(p='GroupBox_12', fileName=r'galeria.png')
RsgLabel(p='GroupBox_12', text='Indicate the location of Point P0 in the global coordinate system, for numerical analysis.', useBoldFont=False)
RsgTable(p='GroupBox_12', numRows=1, columnData=[('X', 'Float', 40), ('Y', 'Float', 40)], showRowNumbers=True, showGrids=True, keyword='Origem', popupFlags='')
RsgGroupBox(name='GroupBox_8', p='TabItem_3', text='Choosing the type of Solver', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgLabel(p='GroupBox_8', text='The type of Solver will imply the type of results to be obtained.', useBoldFont=True)
RsgList(name='List_1', p='GroupBox_8', nvis=2, keyword='Solucionador', default='', layout='LAYOUT_FILL_X')
RsgListItem(p='List_1', text='Structural Mechanics - Uncoupled (UN)')
RsgListItem(p='List_1', text='Hydromechanics - Coupled (CO)')

# Load Tab Interface
RsgTabItem(name='TabItem_4', p='TabBook_1', text='Load')
RsgGroupBox(name='GroupBox_10', p='TabItem_4', text='Loading due to Water Accumulation', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgSlider(p='GroupBox_10', text='Upstream Water Height (%)', minLabelText='Minimum level', maxLabelText='Maximum level', valueType=FLOAT, minValue=0, maxValue=100, decimalPlaces=2, showValue=True, width=400, keyword='NA_montante', default=100)
RsgIcon(p='GroupBox_10', fileName=r'dam_load.png')
RsgTextField(p='GroupBox_10', fieldType='Float', ncols=12, labelText='Downstream Water Height (m)', keyword='NA_jusante', default='0.0')
RsgLabel(p='GroupBox_10', text='the value of the water level downstream must always be lower than the height of the dam.', useBoldFont=False)
RsgGroupBox(name='GroupBox_11', p='TabItem_4', text='Weight', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgCheckButton(p='GroupBox_11', text='Consider the Set\x92s Own Weight', keyword='Peso_p', default=True)

# Mesh Tab Interface
RsgTabItem(name='TabItem_5', p='TabBook_1', text='Mesh')
RsgGroupBox(name='GroupBox_13', p='TabItem_5', text='Element shape', layout='LAYOUT_FILL_X')
RsgLabel(p='GroupBox_13', text='Choose the type of algorithm for developing the mesh.', useBoldFont=True)
RsgLabel(p='GroupBox_13', text='Progressive = Tends to create a structured mesh.', useBoldFont=False)
RsgLabel(p='GroupBox_13', text='Reduce Deformity = Tends to reduce mesh distortion,', useBoldFont=False)
RsgLabel(p='GroupBox_13', text='but may deviate further in specific locations.', useBoldFont=False)
RsgList(name='List_2', p='GroupBox_13', nvis=2, keyword='forma_algorit', default='Progressive', layout='0')
RsgListItem(p='List_2', text='Progressive')
RsgListItem(p='List_2', text='Reduce Deformity')
RsgLabel(p='TabItem_5', text='Choose between Linear Element or Quadratic Element', useBoldFont=False)
RsgHorizontalFrame(name='HFrame_2', p='TabItem_5', layout='0', pl=0, pr=0, pt=0, pb=0)
RsgIcon(p='HFrame_2', fileName=r'elementos.png')
RsgList(name='List_3', p='HFrame_2', nvis=2, keyword='elemento_tipo', default='Linear', layout='0')
RsgListItem(p='List_3', text='Linear')
RsgListItem(p='List_3', text='Quadratic')
RsgListItem(p='List_3', text='Item 3')
RsgGroupBox(name='GroupBox_15', p='TabItem_5', text='Mesh Size', layout='LAYOUT_FILL_X')
RsgTextField(p='GroupBox_15', fieldType='Float', ncols=12, labelText='Mesh Size', keyword='tamanho', default='')

# job Solution Tab Interface
RsgTabItem(name='TabItem_6', p='TabBook_1', text='Job Solution')
RsgGroupBox(name='GroupBox_16', p='TabItem_6', text='Configuration for Processing', layout='LAYOUT_FILL_X')
RsgTextField(p='GroupBox_16', fieldType='String', ncols=35, labelText='ODB File Name', keyword='job_nome', default='')
RsgGroupBox(name='GroupBox_17', p='GroupBox_16', text='Processing Cores', layout='LAYOUT_FILL_X')
RsgLabel(p='GroupBox_17', text='ABAQUS offers the possibility of choosing ', useBoldFont=False)
RsgSpinner(p='GroupBox_17', text='the number of cores for processing.', ncols=4, valueType=INTEGER, increment=1, minValue=1, maxValue=4, keyword='cpu', default=2)
dialogBox.show()