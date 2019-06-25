import os
import re
import random
import json
from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log
from pomdp_runner import PomdpRunner
from util.runner_params import RunnerParams

config_file = "pomdp/problems_definition/" # Config_file base path

class App:

    def run_tag(self):

        params = RunnerParams("tag.pomdp", None, "pomcp", 1, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_TotalRewards= runner.runTag(**algo_params)
            print(str(all_actions))
            print(str(all_TotalRewards))

    def run_tiger(self):

        params = RunnerParams("Tiger-3D.POMDP", None, "pomcp", 10, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_TotalRewards= runner.runTag(**algo_params)
            print(str(all_actions))
            print(str(all_TotalRewards))

App().run_tiger()
