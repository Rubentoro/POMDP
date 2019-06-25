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



    env="tag.pomdp"
    logfile=None
    config="pomcp"
    budget=10
    max_play=10
    snapshot=None
    random_prior=None

    params = RunnerParams("tag.pomdp", None, "pomcp", 1, 10, None, None)

    with open(params.algo_config) as algo_config:
        algo_params = json.load(algo_config)
        print("------------" + str(algo_params) + "-------------------")
        runner = PomdpRunner(params)
        all_actions, all_TotalRewards= runner.run(**algo_params)
        print(str(all_actions))
        print(str(all_TotalRewards))


