import os

from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log




class App:

    config_file = open("pomdp/problems_definition/tag.pomdp","r+")

    POMDP= PomdpParser.__init__(config_file)
    print(str(POMDP))

    def get_initial_state():
        print(str(POMDP.states))

