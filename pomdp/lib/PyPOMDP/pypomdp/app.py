import os
import re
import random
from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log

config_file = "pomdp/problems_definition/" # Config_file base path

class App:

    def get_config_file(problem):
        if(problem=="tiger"):
            return config_file+"tiger.pomdp"
        if(problem=="tag"):
            return config_file+"tag.pomdp"

    config_file = get_config_file("tag")

    POMDP= PomdpParser(config_file)
    POMDP.__enter__()

    def set_initial_state(POMDP):
        states = POMDP.states
        rand = random.randint(0, len(states)-1)
        print(str(rand))
        POMDP.init_state = states[rand]
        print("Initial state: "+str(POMDP.init_state))

    def stop_condition(POMDP):
            config_base_path = "pomdp/problems_definition/"
            global config_file
            if(config_file == config_base_path+"tag.pomdp"):
                pattern = re.compile("^.*(tagged)$")
                return pattern.match(str(POMDP.init_state)) 
            else:
                return False

    # Initial state is set. Then we check if the random-set initial state is a stop condition, if so, we generate a new one.
    set_initial_state(POMDP)
    if(stop_condition(POMDP)):
        set_initial_state(POMDP)
