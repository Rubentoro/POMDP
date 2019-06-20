import os
import re
import random
from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log


class App:

    config_file = "pomdp/problems_definition/tag.pomdp"

    POMDP= PomdpParser(config_file)
    POMDP.__enter__()
    #print("ESTADOS: " + str(POMDP.states))

   # print("ESTADO INICIAL: " + str(POMDP.init_state))
   # print("OBSERVACIONES: " + str(POMDP.observations))
   # print("ACCIONES: " + str(POMDP.actions))
   # print("COSTES: " + str(POMDP.costs))
   # print("T: " + str(POMDP.T))
    if(hasattr(POMDP, 'O')):
        print("O: " + str(POMDP.O))
    #print("R: " + str(POMDP.R))

    def set_initial_state(POMDP):
        states = POMDP.states
        rand = random.randint(0, len(states)-1)
        print(str(rand))
        POMDP.init_state = states[rand]
        print(str(POMDP.init_state))

    def stop_condition(POMDP):
            config_base_path = "pomdp/problems_definition/"
            #if(config_file == config_base_path+"tag.pomdp"): #TODO: Figure out how to get the global variable 'config_file'
            if("pomdp/problems_definition/tag.pomdp" == config_base_path+"tag.pomdp"): #TODO
                pattern = re.compile("^.*(tagged)$")
                return pattern.match(str(POMDP.init_state)) 
            else:
                return False

    # Initial state is set. Then we check if the random-set initial state is a stop condition, if so, we generate a new one
    set_initial_state(POMDP)
    if(stop_condition(POMDP)):
        set_initial_state(POMDP)
