#PyADam Processing
"""
Created on 30/12/2023
Connection code with ABAQUS/CAE
@author: Josinaldo Leandro de Souza
"""

from abaqusGui import getAFXApp, Activator, AFXMode
from abaqusConstants import ALL
import os

#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

# Connection with script and DialogBox
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='PyADam - Processing', 
    object=Activator(os.path.join(thisDir, 'PyADam_02DB.py')),
    kernelInitString='import PyADam_script',
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
