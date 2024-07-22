# -*- coding: utf-8 -*-
"""
Created on 30/12/2023
ABAQUS/CAE workflow implementation code
@author: Josinaldo Leandro de Souza
"""

from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import odbAccess
from operator import add


import numpy as np
#import matplotlib.pyplot as plt

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Funcoes

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Modulo de Criacao de particao
def DAM_ret(Pontos,Pontos2,part,material1,Rho_ccr,Es_ccr,nu_ccr,Ks_ccr,iv_ccr,material2,Rho_rocha,Es_rocha,nu_rocha,Ks_rocha,iv_rocha,Origem,Solucionador,NA_montante,NA_jusante,Peso_p,forma_algorit,elemento_tipo,tamanho,job_nome,cpu):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=50.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    # cricao do tracado da barragem   
    for i in range(len(Pontos) - 1):
        s.Line(point1=Pontos[i], point2=Pontos[i + 1])
    #criar a fundacao automatico
    # Encontre o maior valor de coordenada x e y
    maior_x = max(Pontos, key=lambda ponto: ponto[0])[0]
    maior_y = max(Pontos, key=lambda ponto: ponto[1])[1]
    # faz a fundacao em rocha automatico
    s.Line(point1=( maior_x, 0.0), point2=( maior_x + maior_y, 0.0))
    s.Line(point1=( maior_x + maior_y, 0.0), point2=( maior_x + maior_y, -maior_y))
    s.Line(point1=( maior_x + maior_y, -maior_y), point2=(-maior_y, -maior_y))
    s.Line(point1=(-maior_y, -maior_y), point2=(-maior_y, 0.0))
    s.Line(point1=(-maior_y, 0.0), point2=(0.0, 0.0))
    #cria a galeria
    if Pontos2 == ():
        # finaliza a criacao da particao
        p = mdb.models['Model-1'].Part(name=part, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts[part]
        p.BaseShell(sketch=s)
        s.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']
    else:
        s.rectangle(point1=Pontos2[0], point2=Pontos2[1])
        # finaliza a criacao da particao
        p = mdb.models['Model-1'].Part(name=part, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts[part]
        p.BaseShell(sketch=s)
        s.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']
    
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -        

    #Centroide da barragem
    xb =  maior_x/2
    yb =  maior_y/2

    #Centroide da fundacao
    xr =  maior_x/2
    yr =  -maior_y/2    
    
    # Sequencia para encontrar os pontos a montante e jusante conforme as alturas informadas    
    # Plano de divisão
    ponto1 = max(Pontos, key=lambda ponto: ponto[1])
        
    # Dividir a lista em lados esquerdo e direito com base no plano de divisão
    lado_esquerdo = [ponto for ponto in Pontos if ponto[0] <= ponto1[0]]
    lado_direito = [ponto for ponto in Pontos if ponto[0] > ponto1[0]]
 
    # Altura informada
    altura_informada = NA_jusante
    altura_informada2 = (maior_y-0.1)*(NA_montante/100)   # altura_informada2 > altura_informada 
    
    # Encontre os pontos maiores e menores que a altura de Y=10 no lado direito
    pontos_menores_que_altura = [ponto for ponto in lado_direito if ponto[1] <= altura_informada]
    pontos_maiores_que_altura = [ponto for ponto in lado_direito if ponto[1] > altura_informada]
    
    # Encontre os pontos maiores e menores que a altura de Y=10 no lado direito
    pontos_menores_que_altura_e = [ponto for ponto in lado_esquerdo if ponto[1] <= altura_informada2]
    pontos_maiores_que_altura_e = [ponto for ponto in lado_esquerdo if ponto[1] > altura_informada2]
    
    # Encontre os pontos maiores e menores que a altura de Y=10 no lado direito
    pontos_menores_que_altura_e2 = [ponto for ponto in lado_esquerdo if ponto[1] <= altura_informada]
    pontos_maiores_que_altura_e2 = [ponto for ponto in lado_esquerdo if ponto[1] > altura_informada]
    
    # Encontre os pontos maiores e menores que a altura montante no lado direito
    pontos_menores_que_altura_d2 = [ponto for ponto in lado_direito if ponto[1] <= altura_informada2]
    pontos_maiores_que_altura_d2 = [ponto for ponto in lado_direito if ponto[1] > altura_informada2]

    # Inicialize as variáveis para armazenar o ponto anterior e o ponto seguinte
    ponto_anterior = pontos_maiores_que_altura[-1]
    ponto_seguinte = pontos_menores_que_altura[0]
    
    # Coordenadas dos pontos A e B
    XA, YA = ponto_anterior
    XB, YB = ponto_seguinte
    
    # Verifique se a inclinação é zero
    if XB == XA:
        XP = XA
    else:
        # Calcule a inclinação (m)
        m = (YB - YA) / (XB - XA)
        # Use a fórmula completa para encontrar X_p
        XP = XA + (altura_informada - YA) / m
    
    # Encontre os pontos de interseção entre a linha da altura informada e os pontos menores que a altura
    if NA_jusante > 0:
        intersecao = [(XP,altura_informada)] + pontos_menores_que_altura
    else:
        intersecao = pontos_menores_que_altura
    pontos_intersecao = sorted(intersecao, key=lambda x: x[0])
    
    # Encontrar as coordenadas medias entre os pontos de interseccao
    coordenadas_medias = []
        
        # Calcula as coordenadas médias entre os pontos
    for i in range(len(pontos_intersecao) - 1):
        ponto_atual = pontos_intersecao[i]
        proximo_ponto = pontos_intersecao[i + 1]
        
        coordenada_x_media = (ponto_atual[0] + proximo_ponto[0]) / 2
        coordenada_y_media = (ponto_atual[1] + proximo_ponto[1]) / 2
        
        coordenadas_medias.append((coordenada_x_media, coordenada_y_media))
    
    # Inicialize as variáveis para armazenar o ponto anterior e o ponto seguinte do lado esquerdo
    ponto_anterior2 = pontos_maiores_que_altura_e[0]
    ponto_seguinte2 = pontos_menores_que_altura_e[-1]
    
    # Coordenadas dos pontos A e B
    XA2, YA2 = ponto_anterior2
    XB2, YB2 = ponto_seguinte2
    
    # Verifique se a inclinação é zero
    if XB2 == XA2:
        XP2 = XA2
    else:
        # Calcule a inclinação (m)
        m2 = (YB2 - YA2) / (XB2 - XA2)
        # Use a fórmula completa para encontrar X_p
        XP2 = XA2 + (altura_informada2 - YA2) / m2
    
    # Inicialize as variáveis para armazenar o ponto anterior e o ponto seguinte do lado esquerdo
    ponto_anterior3 = pontos_maiores_que_altura_e2[0]
    ponto_seguinte3 = pontos_menores_que_altura_e2[-1]
    
    # Coordenadas dos pontos A e B
    XA3, YA3 = ponto_anterior3
    XB3, YB3 = ponto_seguinte3
    
    # Verifique se a inclinação é zero
    if XB3 == XA3:
        XP3 = XA3
    else:
        # Calcule a inclinação (m)
        m3 = (YB3 - YA3) / (XB3 - XA3)
        # Use a fórmula completa para encontrar X_p
        XP3 = XA3 + (altura_informada - YA3) / m3
    
    # Encontre os pontos de interseção entre a linha da altura informada e os pontos menores que a altura
    if NA_jusante > 0:
        intersecao2 = [(XP2,altura_informada2),(XP3,altura_informada)] + pontos_menores_que_altura_e
    else:
        intersecao2 = [(XP2,altura_informada2)] + pontos_menores_que_altura_e
    pontos_intersecao2 = sorted(intersecao2, key=lambda x: x[0])
    
    # Encontrar as coordenadas medias entre os pontos de interseccao
    coordenadas_medias2 = []
        
        # Calcula as coordenadas médias entre os pontos
    for i in range(len(pontos_intersecao2) - 1):
        ponto_atual2 = pontos_intersecao2[i]
        proximo_ponto2 = pontos_intersecao2[i + 1]
        
        coordenada_x_media2 = (ponto_atual2[0] + proximo_ponto2[0]) / 2
        coordenada_y_media2 = (ponto_atual2[1] + proximo_ponto2[1]) / 2
        
        coordenadas_medias2.append((coordenada_x_media2, coordenada_y_media2))
    
    # Encontrar as coordenadas medias entre os pontos de interseccao lado direito acima do nivel jusante
    
    # Inicialize as variáveis para armazenar o ponto anterior e o ponto seguinte do lado esquerdo
    ponto_anterior4 = pontos_menores_que_altura_d2[0]
    if pontos_maiores_que_altura_d2 == []:
        ponto_seguinte4 = ponto1
    else:
        ponto_seguinte4 = pontos_maiores_que_altura_d2[-1]
    
    # Coordenadas dos pontos A e B
    XA4, YA4 = ponto_anterior4
    XB4, YB4 = ponto_seguinte4
    
    # Verifique se a inclinação é zero
    if XB4 == XA4:
        XP4 = XA4
    else:
        # Calcule a inclinação (m)
        m4 = (YB4 - YA4) / (XB4 - XA4)
        # Use a fórmula completa para encontrar X_p
        XP4 = XA4 + (altura_informada2 - YA4) / m4
    
    # listar os pontos médios do lado direito incluindo o ponto correspondente ao nivel montante
    coord_med3 = [(XP4,altura_informada2)]
        
        # Calcula as coordenadas médias entre os pontos
    for i in range(len(lado_direito) - 1):
        ponto_atual3 = lado_direito[i]
        proximo_ponto3 = lado_direito[i + 1]
        
        coordenada_x_media3 = (ponto_atual3[0] + proximo_ponto3[0]) / 2
        coordenada_y_media3 = (ponto_atual3[1] + proximo_ponto3[1]) / 2
        
        coord_med3.append((coordenada_x_media3, coordenada_y_media3))
    
    # Crie uma cópia de lado_direito para evitar a modificação durante a iteração
    coord_medias3 = list(coord_med3)
    coordenadas_medias3 = sorted(coord_medias3, key=lambda x: x[0])
    
    # Itere para remover os pontos abaixo do nivel jusante
    for ponto in coordenadas_medias:
        if ponto in coordenadas_medias3:
            coordenadas_medias3.remove(ponto)
        
 #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    set_name = "Modulo_Geral"
    #Modulo de Criacao SET Geral
    
    def Set_Geral(part,set_name):
        p = mdb.models['Model-1'].parts[part]
        f = p.faces[:]
        p.Set(faces=f, name=set_name)
    Set_Geral(part,set_name)
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
#Modulo de Criacao de plano de corte
    #offset_plane = 0.0
    def Plano_corte(part,offset_plane):
        p = mdb.models['Model-1'].parts[part]
        myPlane = p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=offset_plane)
        myID = myPlane.id # realizado automaticamente
        return myID
    myID_0 = Plano_corte(part,0.0)
    myID_1 = Plano_corte(part,altura_informada)
    myID_2 = Plano_corte(part,altura_informada2)
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

#Modulo de Criacao de particao com base em um plano de corte

    def Corte_Plano(part,myID):
        p = mdb.models['Model-1'].parts[part]
        f = p.faces[:]
        d = p.datums
        p.PartitionFaceByDatumPlane(datumPlane=d[myID], faces=f)
    Corte_Plano(part,myID_0) # realizado automaticamente

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao SET de Area Especifica

    def Set_Face(x,y,part,set_name):
        face = ()
        p = mdb.models['Model-1'].parts[part]
        f = p.faces
        myFace = f.findAt((x,y,0),)
        face = face + (f[myFace.index:myFace.index+1],)
        p.Set(faces=face, name=set_name)
        return myFace
    
    Set_Face(xb,yb,part,"CCR") # realizado automaticamente
    Set_Face(xr,yr,part,"ROCHA")
   
    # Criando Planos apos a criancao das regiões de cada material
    if NA_jusante > 0:
        Corte_Plano(part,myID_1)
    
    if NA_montante > 0:
        Corte_Plano(part,myID_2)
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao SET de linha Especifica

    def Set_linha(x,y,part,set_name):
        borda = ()
        p = mdb.models['Model-1'].parts[part]
        e = p.edges
        myBorda = e.findAt((x,y,0),)
        borda = borda + (e[myBorda.index:myBorda.index+1],)
        p.Set(edges=borda, name=set_name)
        return myBorda

    # Criar Set Especificos

    # selecionado toda a borda da fundacao no ponto medio da linha
    Set_linha(maior_x/2, -maior_y, part,"Fundacao") # realizado automaticamente
    
    # selecionado SET toda a borda montande no ponto medio da linha
    Set_linha(-maior_y/2,0.0,part,"Montante_0") # realizado automaticamente
    # cricao do tracado do SET a Montante
    for i in range(len(coordenadas_medias2)):
        x_mi,y_mi = coordenadas_medias2[i]
        Set_linha(x_mi,y_mi, part,"Montante_"+ str(i+1))

    # selecionado SET toda a borda montande no ponto medio da linha
    Set_linha(maior_x + maior_y/2, 0.0, part,"Jusante_0") # realizado automaticamente
    # cricao do tracado do SET a Jusante
    for i in range(len(coordenadas_medias)):
        x_mi,y_mi = coordenadas_medias[i]
        Set_linha(x_mi,y_mi, part,"Jusante_"+ str(i+1))

    # selecionado SET para a borda jusante nula no ponto medio da linha
    # cricao do tracado da Borda a Jusante nula
    for i in range(len(coordenadas_medias3)):
        x_mi,y_mi = coordenadas_medias3[i]
        Set_linha(x_mi,y_mi, part,"Jusante_nula_"+ str(i))

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

#Modulo de Criacao SET de Borda Especifico
    
    def Set_borda(x,y,part,set_name):
        borda = ()
        p = mdb.models['Model-1'].parts[part]
        s = p.edges
        myBorda = s.findAt((x,y,0),)
        borda = borda + (s[myBorda.index:myBorda.index+1],)
        p.Surface(side1Edges=borda, name=set_name)
        return myBorda
    
    # selecionado SET toda a borda montante no ponto medio da linha
    Set_borda(-maior_y/2,0.0,part,"Borda_Montante_0") # realizado automaticamente
# cricao do tracado da Borda a Montante
    for i in range(len(coordenadas_medias2)):
        x_mi,y_mi = coordenadas_medias2[i]
        Set_borda(x_mi,y_mi, part,"Borda_Montante_"+ str(i+1))
#    Set_borda(0.0,maior_y/2,part,"Borda_Montante_1")

    # selecionado SET toda a borda jusante no ponto medio da linha
    Set_borda(maior_x + maior_y/2, 0.0, part,"Borda_Jusante_0") # realizado automaticamente
    # cricao do tracado da Borda a Jusante
    for i in range(len(coordenadas_medias)):
        x_mi,y_mi = coordenadas_medias[i]
        Set_borda(x_mi,y_mi, part,"Borda_Jusante_"+ str(i+1))

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

#Modulo de criacao de material 

    def cria_material_aplica(part,material_nome,Rho,Es,nu,Ks,iv,secao_nome,set_name):
        p = mdb.models['Model-1'].parts[part]
        mdb.models['Model-1'].Material(name=material_nome)
        mdb.models['Model-1'].materials[material_nome].Density(table=((Rho, ), ))
        mdb.models['Model-1'].materials[material_nome].Elastic(table=((Es,nu), ))
        mdb.models['Model-1'].materials[material_nome].Permeability(specificWeight=0.001, inertialDragCoefficient=0.142887, table=((Ks,iv), ))
        mdb.models['Model-1'].HomogeneousSolidSection(name=secao_nome, material=material_nome, thickness=None)
        p = mdb.models['Model-1'].parts[part]
        region = p.sets[set_name]
        p = mdb.models['Model-1'].parts[part]
        p.SectionAssignment(region=region, sectionName=secao_nome, offset=0.0,offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)

    cria_material_aplica(part,"Concreto_CCR",Rho_ccr,Es_ccr,nu_ccr,Ks_ccr,iv_ccr,"secao_concreto","CCR")

    cria_material_aplica(part,"Rocha_granito",Rho_rocha,Es_rocha,nu_rocha,Ks_rocha,iv_rocha,"secao_rocha","ROCHA")

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao do Sistema global

    def Conjunto_assembly(part, instance,x,y):
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts[part]
        a.Instance(name=instance, part=p, dependent=OFF)
        p = a.instances[instance]
        p.translate(vector=(x,y,0))

    instance = 'Analise Barragem'
    X_origem, Y_origem = Origem[0]
         
    Conjunto_assembly(part,instance,X_origem,Y_origem)

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao do tipo de Solucionador

    def Solucionador_solos(step_name,pre_step_name):
        a = mdb.models['Model-1'].SoilsStep(name=step_name, previous=pre_step_name, response=STEADY_STATE, creep=OFF, end=None, utol=None, cetol=None, amplitude=RAMP)

    def Solucionador_estatico(step_name,pre_step_name):
        a = mdb.models['Model-1'].StaticStep(name=step_name, previous=pre_step_name,adiabatic=ON)
        
    # Verifique a escolha do tipo de solucinador correspondente

    if Solucionador == "Hydromechanics - Coupled (CO)":
        step_name = "Solos"
        pre_step_name = "Initial"
        Solucionador_solos(step_name,pre_step_name)
    else:
        step_name = "Estatico"
        pre_step_name = "Initial"         
        Solucionador_estatico(step_name,pre_step_name)
    
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao do peso proprio

    def Peso_proprio(instance,set_name,load_name,step_name,load):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name]
        mdb.models['Model-1'].Gravity(name=load_name, createStepName=step_name, comp2=-load, distributionType=UNIFORM, field='', region=region)
    
    # Criar o peso proprio
    load_name = "Peso"
    load = 9.81   # aceleracao da gravidade
    if Peso_p == True:
        Peso_proprio(instance,set_name,load_name,step_name,load)

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
#Modulo de Criacao da forca triangular devido o empuxo

    def Forca_EMP(nome_forca,load_a, height):
        p = mdb.models['Model-1'].ExpressionField(name=nome_forca, localCsys=None, description='', expression = '{} * ({} - Y)'.format(load_a,height))
        
        # Criar a forca triangular do empuxo de agua
    agua = 1000
    ag_a = load * agua

    Forca_EMP("Empuxo_montante",ag_a,altura_informada2)
    Forca_EMP("Empuxo_jusante",ag_a,altura_informada)      
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de criacao do Empuxo de agua

    def Emp_agua(instance,Borda_nome,nome_empuxo,solucionador,formula):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].surfaces[Borda_nome]
        mdb.models['Model-1'].Pressure(name=nome_empuxo, createStepName=solucionador,region=region, distributionType=FIELD, field=formula, magnitude=1.0,amplitude=UNSET)
    
    # Criar o empuxo lateral devido a agua no lado Montante
    if NA_montante > 0:
        Emp_agua(instance,"Borda_Montante_0","Empuxo_0",step_name,"Empuxo_montante")
        for i in range(len(coordenadas_medias2)):
            Emp_agua(instance,"Borda_Montante_"+ str(i+1),"Empuxo_"+ str(i+1),step_name,"Empuxo_montante")
          
    # Criar o empuxo lateral devido a agua no lado Jusante
    if NA_jusante > 0:
        Emp_agua(instance,"Borda_Jusante_0","Empuxo_Jus_0",step_name,"Empuxo_jusante")
        for i in range(len(coordenadas_medias)):
            Emp_agua(instance,"Borda_Jusante_"+ str(i+1),"Empuxo_Jus_"+ str(i+1),step_name,"Empuxo_jusante")
            
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -      

# Modulo de Criacao da Poropressao a montante

    def Poro_pressao(instance,set_name,poro_nome,solucionador,formula):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name]
        a = mdb.models['Model-1'].PorePressureBC(name=poro_nome,createStepName=solucionador, region=region, fixed=OFF,distributionType=FIELD, fieldName=formula, magnitude=1.0,amplitude=UNSET)

    #Criar a Poropressao na barragem a Montante
    if Solucionador == "Hydromechanics - Coupled (CO)":
        if NA_montante > 0:
            Poro_pressao(instance,"Montante_0","Poro_montante_0",step_name,"Empuxo_montante")
            for i in range(len(coordenadas_medias2)):
                Poro_pressao(instance,"Montante_"+ str(i+1),"Poro_montante_"+ str(i+1),step_name,"Empuxo_montante")
    
        # Criar o empuxo lateral devido a agua no lado Jusante
        if NA_jusante > 0:
            Poro_pressao(instance,"Jusante_0","Poro_Jus_0",step_name,"Empuxo_jusante")
            for i in range(len(coordenadas_medias)):
                Poro_pressao(instance,"Jusante_"+ str(i+1),"Poro_Jus_"+ str(i+1),step_name,"Empuxo_jusante")
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao da Poropressao a jusante

    def Poro_jusante(instance,set_name,poro_nome,solucionador):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name]
        mdb.models['Model-1'].PorePressureBC(name=poro_nome,createStepName=solucionador, region=region, fixed=OFF, distributionType=UNIFORM, fieldName='', magnitude=0.0, amplitude=UNSET)

    #Criar a Poropressao nula na barragem a Jusante
    if Solucionador == "Hydromechanics - Coupled (CO)":
        if NA_jusante > 0:
        #Poro_jusante(instance,"Jusante_0","Poro_jusante0","Solos")
            for i in range(len(coordenadas_medias3)):
                Poro_jusante(instance,"Jusante_nula_"+ str(i),"Poro_nulo_"+ str(i),step_name)
        else:
            Poro_jusante(instance,"Jusante_0","Poro_nulo_0",step_name)
            for i in range(len(coordenadas_medias3)):
                Poro_jusante(instance,"Jusante_nula_"+ str(i),"Poro_nulo_"+ str(i+1),step_name)
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao do engastamento na fundacao

    def Engaste_fundacao(instance,set_name,Engaste_nome):    
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name]
        mdb.models['Model-1'].EncastreBC(name=Engaste_nome,createStepName='Initial', region=region, localCsys=None)

    # Criar o Engaste na Fundacao
    Engaste_fundacao(instance,"Fundacao","FUNDACAO_modelo")

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao do indice de vazios

    def Indice_vazios(instance,set_name,indice_nome):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name]
        mdb.models['Model-1'].VoidsRatio(name=indice_nome, region=region,voidsRatio1=0.01, distributionType=UNIFORM, variation=CONSTANT_RATIO)

    #Criar o Indice de Vazios
    Indice_vazios(instance,set_name,"Indice_VAZIOS")

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao do controle de malha

    def Controle_Malha(instance,set_name,forma_algorit):
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name].faces[:]
        a.setMeshControls(regions=region, technique=FREE, elemShape=QUAD, algorithm=forma_algorit)
    
    #Criar o controle da malha
    if forma_algorit == "Progressive":
        Controle_Malha(instance,set_name,ADVANCING_FRONT)
    else:
        Controle_Malha(instance,set_name,MEDIAL_AXIS)
        
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao do tipo de elemento

    def Tipo_elemento(instance,set_name,elemento1,elemento2):
        elemType1 = mesh.ElemType(elemCode=elemento1, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=elemento2, elemLibrary=STANDARD)
        a = mdb.models['Model-1'].rootAssembly
        region = a.instances[instance].sets[set_name].faces[:]
        faces1 = region.getSequenceFromMask(mask=('[#1f ]', ), )
        pickedRegions =(faces1, )
        a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    #Criar o tipo de elemento
    if Solucionador == "Hydromechanics - Coupled (CO)": # Solucionador de solos
        if elemento_tipo == "Linear":  # elemento linear
            elemento1 = CPE4P
            elemento2 = UNKNOWN_TRI
            Tipo_elemento(instance,set_name,elemento1,elemento2)
        
        else:   # elemento quadratico
            elemento1 = CPE8P
            elemento2 = CPE6MP
            Tipo_elemento(instance,set_name,elemento1,elemento2)
    
    else:  # Solucionador estatico
        if elemento_tipo == "Linear":  # elemento linear
            elemento1 = CPS4R
            elemento2 = CPS3
            Tipo_elemento(instance,set_name,elemento1,elemento2)
        
        else:   # elemento quadratico
            elemento1 = CPS8
            elemento2 = CPS6M
            Tipo_elemento(instance,set_name,elemento1,elemento2)

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao da malha

    def Malha(instance,tamanho):
        a = mdb.models['Model-1'].rootAssembly
        partInstances =(a.instances[instance], )
        a.seedPartInstance(regions=partInstances, size=tamanho, deviationFactor=0.1, minSizeFactor=0.1)
        a.generateMesh(regions=partInstances)

    #Criar a malhar
    Malha(instance,tamanho)
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criacao do job (processamento)  
    
    def job(job_nome,cpu):
        a = mdb.models['Model-1'].rootAssembly
        mdb.Job(name=job_nome, model='Model-1', description='',type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=cpu, numDomains=cpu, numGPUs=0)    

    # Criando o Job
    #cpu_inteiro = int(cpu)
    job(job_nome,cpu)

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de inicar o processamento
    
def Submit_Job(arq_job_nome,run):
    #mdb.jobs[arq_job_nome].submit(consistencyChecking=OFF)

    # Iniciar o processamento
    if run == True:
        #Submit_Job(arq_job_nome)
        mdb.jobs[arq_job_nome].submit(consistencyChecking=OFF)

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    


#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# POS-PROCESSAMENTO
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

# Modulo de Criar o tracado para o grafico

def mypath(nome_path,instance,noo):

    session.Path(name=nome_path, type=NODE_LIST, expression=((instance.upper(),noo), ))

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Modulo de criar o dado com base no tracado e exporta

def dadoXY(dado1,dado2,nome_path,nome_dado):
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel=dado1, outputPosition=INTEGRATION_POINT, refinement=(dado2))
    pth = session.paths[nome_path]
    
    session.XYDataFromPath(name=nome_dado, path=pth,includeIntersections=True,projectOntoMesh=False,pathStyle=PATH_POINTS, numIntervals=10,projectionTolerance=0, shape=DEFORMED, labelType=TRUE_DISTANCE)
    # Exporta o dado criado com base no tracado
    x0 = session.xyDataObjects[nome_dado]
    session.xyReportOptions.setValues(numDigits=8, numberFormat=AUTOMATIC)
    session.writeXYReport(fileName=str(nome_dado)+'.txt', xyData=(x0, ))

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
