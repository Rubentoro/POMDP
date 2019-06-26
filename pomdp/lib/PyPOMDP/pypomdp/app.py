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

    def run_tag_pomcp(self):

        params = RunnerParams("tag.pomdp", None, "pomcp", 1, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTag(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

    def run_tag_pbvi(self):

        params = RunnerParams("tag.pomdp", None, "pbvi", 1, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTag(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

    def run_tiger_pomcp(self):

        params = RunnerParams("tiger.pomdp", None, "pomcp", 10, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTiger(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

    def run_tiger_pbvi(self):

        params = RunnerParams("tiger.pomdp", None, "pbvi", 10, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTiger(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards


    def run_tiger3_pomcp(self):

        params = RunnerParams("Tiger-3D.POMDP", None, "pomcp", 10, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTiger(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

    def run_tiger3_pbvi(self):

        params = RunnerParams("Tiger-3D.POMDP", None, "pbvi", 10, 10, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards= runner.runTiger(**algo_params)
            return all_actions, all_total_rewards


    def run_bridge_repair_pomcp(self):
        params = RunnerParams("bridge_repair.pomdp", None, "pomcp", 10, 20, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards = runner.runBridge(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

    def run_bridge_repair_pbvi(self):
        params = RunnerParams("bridge_repair.pomdp", None, "pbvi", 10, 20, None, None)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions, all_total_rewards = runner.runBridge(**algo_params)
            print(str(all_actions))
            print(str(all_total_rewards))
            return all_actions, all_total_rewards

#App().run_tag_pomcp()
#App().run_tag_pbvi()

#App().run_tiger_pomcp()
#App().run_tiger_pbvi()

#App().run_tiger3_pomcp()
#App().run_tiger3_pbvi()

#App().run_bridge_repair_pomcp()
App().run_bridge_repair_pbvi()