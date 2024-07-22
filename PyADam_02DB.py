#PyADam Processing
"""
Created on 30/12/2023
DiaolgBox code with ABAQUS/CAE
@author: Josinaldo Leandro de Souza
"""

from rsg.rsgGui import *
from abaqusConstants import INTEGER, FLOAT

# Connection with script
dialogBox = RsgDialog(title='PyADan - Processing', kernelModule='PyADam_script', kernelFunction='Submit_Job', includeApplyBtn=False, includeSeparator=True, okBtnText='OK', applyBtnText='Apply', execDir=thisDir)

# Processing Tab Interface
RsgGroupBox(name='GroupBox_1', p='DialogBox', text='Processing', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgGroupBox(name='GroupBox_2', p='GroupBox_1', text='Processing file saved in the Pre-Processing stage', layout='LAYOUT_FILL_X')
RsgTextField(p='GroupBox_2', fieldType='String', ncols=35, labelText='ODB file', keyword='arq_job_nome', default='')
RsgGroupBox(name='GroupBox_4', p='GroupBox_1', text='Start Processing', layout='LAYOUT_FILL_X|LAYOUT_FILL_Y')
RsgLabel(p='GroupBox_4', text='After indicating the name of the ODB file, select processing ', useBoldFont=False)
RsgLabel(p='GroupBox_4', text='(RUN) and click OK to start processing.', useBoldFont=False)
RsgCheckButton(p='GroupBox_4', text='RUN', keyword='run', default=False)
dialogBox.show()