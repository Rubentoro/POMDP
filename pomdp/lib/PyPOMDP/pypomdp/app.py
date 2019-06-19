import os

from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log




class App:

    config_file = "D:/Users/ruben/Desktop/IA REPO/POMDP/pomdp/problems_definition/tag.pomdp"

    POMDP= PomdpParser(config_file)
    print(str(POMDP))
    POMDP.__enter__()
    print(str(POMDP))
    #print("ESTADOS: " + str(POMDP.states))

    #print("ESTADO INICIAL: " + str(POMDP.init_state))
    print("OBSERVACIONES: " + str(POMDP.observations))
    print("ACCIONES: " + str(POMDP.actions))
    print("COSTES: " + str(POMDP.costs))
    print("T: " + str(POMDP.T))
    print("O: " + str(POMDP.O))
    print("R: " + str(POMDP.R))
