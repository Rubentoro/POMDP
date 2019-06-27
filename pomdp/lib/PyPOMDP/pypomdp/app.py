import os
import re
import random
import json
import warnings
import math
from models import SampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log
from pomdp_runner import PomdpRunner
from util.runner_params import RunnerParams

warnings.filterwarnings("ignore") # Ignore numba related warnings

config_file = "pomdp/problems_definition/" # Config_file base path

class App:

    def compute_sd(self, list, average):
        result = 0
        for i in range(len(list)):
            result = result + (list[i]-average)**2
        return math.sqrt(result/len(list))
    
    def compute_average(self, list):
        result = 0
        for i in range(len(list)):
            result = result + list[i]
        return result/len(list)

    def compute_statistics(self, all_actions, all_total_rewards, all_rewards, steps):
        reward_average = all_total_rewards[-1]/len(all_total_rewards)
        reward_sd = self.compute_sd(all_rewards, reward_average)
        steps_average = self.compute_average(steps)
        steps_sd = self.compute_sd(steps, steps_average)
        return reward_average, reward_sd, steps_average, steps_sd


    def run_tag(self, logfile, algorithm, budget, max_play, snapshot, random_prior, mode):
        if str(mode)=="benchmark":
            budget = 1000000000000
            max_play=30
        params = RunnerParams("tag.pomdp", logfile, str(algorithm), budget, max_play, snapshot, random_prior)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions = list()
            all_total_rewards = list()
            if str(mode)=="interactive":
                all_actions, all_total_rewards, all_rewards= runner.run_tag_interactive(**algo_params)
            if str(mode)=="silent":
                all_actions, all_total_rewards, all_rewards= runner.run_tag_silent(**algo_params)
            if str(mode)=="benchmark":
                all_actions, all_total_rewards, all_rewards, steps= runner.run_tag_benchmark(**algo_params)
            print("\n++++++++++++++++++++\nActions taken: "+str(all_actions)+"\n++++++++++++++++++++")
            print("\n++++++++++++++++++++\nReward update: "+str(all_total_rewards)+"\n++++++++++++++++++++")
            if str(mode)=="benchmark":
                reward_average, reward_sd, steps_average, steps_sd = self.compute_statistics(all_actions, all_total_rewards, all_rewards, steps)
                print("\n++++++++++++++++++++\nReward average: "+str(reward_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nReward standard deviation: "+str(reward_sd)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps average: "+str(steps_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps standard deviation: "+str(steps_sd)+"\n++++++++++++++++++++")

    def run_tiger(self, logfile, algorithm, budget, max_play, snapshot, random_prior, mode):
        if str(mode)=="benchmark":
            budget = 1000000000000
            max_play=30
        params = RunnerParams("tiger.pomdp", logfile, str(algorithm), budget, max_play, snapshot, random_prior)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions = list()
            all_total_rewards = list()
            if str(mode)=="interactive":
                all_actions, all_total_rewards, all_rewards= runner.run_tiger_interactive(**algo_params)
            if str(mode)=="silent":
                all_actions, all_total_rewards, all_rewards= runner.run_tiger_silent(**algo_params)
            if str(mode)=="benchmark":
                all_actions, all_total_rewards, all_rewards, steps= runner.run_tiger_benchmark(**algo_params)
            print("\n++++++++++++++++++++\nActions taken: "+str(all_actions)+"\n++++++++++++++++++++")
            print("\n++++++++++++++++++++\nReward update: "+str(all_total_rewards)+"\n++++++++++++++++++++")
            if str(mode)=="benchmark":
                reward_average, reward_sd, steps_average, steps_sd = self.compute_statistics(all_actions, all_total_rewards, all_rewards, steps)
                print("\n++++++++++++++++++++\nReward average: "+str(reward_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nReward standard deviation: "+str(reward_sd)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps average: "+str(steps_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps standard deviation: "+str(steps_sd)+"\n++++++++++++++++++++")

    def run_bridge_repair(self, logfile, algorithm, budget, max_play, snapshot, random_prior, mode):
        if str(mode)=="benchmark":
            budget = 1000000000000
            max_play=30
        params = RunnerParams("bridge_repair.pomdp", logfile, str(algorithm), budget, max_play, snapshot, random_prior)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions = list()
            all_total_rewards = list()
            if str(mode)=="interactive":
                all_actions, all_total_rewards, all_rewards= runner.run_bridge_interactive(**algo_params)
            if str(mode)=="silent":
                all_actions, all_total_rewards, all_rewards= runner.run_bridge_silent(**algo_params)
            if str(mode)=="benchmark":
                all_actions, all_total_rewards, all_rewards, steps= runner.run_bridge_benchmark(**algo_params)
            print("\n++++++++++++++++++++\nActions taken: "+str(all_actions)+"\n++++++++++++++++++++")
            print("\n++++++++++++++++++++\nReward update: "+str(all_total_rewards)+"\n++++++++++++++++++++")
            if str(mode)=="benchmark":
                reward_average, reward_sd, steps_average, steps_sd = self.compute_statistics(all_actions, all_total_rewards, all_rewards, steps)
                print("\n++++++++++++++++++++\nReward average: "+str(reward_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nReward standard deviation: "+str(reward_sd)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps average: "+str(steps_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps standard deviation: "+str(steps_sd)+"\n++++++++++++++++++++")


    def run_car(self, logfile, algorithm, budget, max_play, snapshot, random_prior, mode):
        if str(mode)=="benchmark":
            budget = 1000000000000
            max_play=30
        params = RunnerParams("car.pomdp", logfile, str(algorithm), budget, max_play, snapshot, random_prior)

        with open(params.algo_config) as algo_config:
            algo_params = json.load(algo_config)
            print("------------" + str(algo_params) + "-------------------")
            runner = PomdpRunner(params)
            all_actions = list()
            all_total_rewards = list()
            if str(mode)=="interactive":
                all_actions, all_total_rewards, all_rewards= runner.run_car_interactive(**algo_params)
            if str(mode)=="silent":
                all_actions, all_total_rewards, all_rewards= runner.run_car_silent(**algo_params)
            if str(mode)=="benchmark":
                all_actions, all_total_rewards, all_rewards, steps= runner.run_car_benchmark(**algo_params) 
            print("\n++++++++++++++++++++\nActions taken: "+str(all_actions)+"\n++++++++++++++++++++")
            print("\n++++++++++++++++++++\nReward update: "+str(all_total_rewards)+"\n++++++++++++++++++++")
            if str(mode)=="benchmark":
                reward_average, reward_sd, steps_average, steps_sd = self.compute_statistics(all_actions, all_total_rewards, all_rewards, steps)
                print("\n++++++++++++++++++++\nReward average: "+str(reward_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nReward standard deviation: "+str(reward_sd)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps average: "+str(steps_average)+"\n++++++++++++++++++++")
                print("\n++++++++++++++++++++\nSteps standard deviation: "+str(steps_sd)+"\n++++++++++++++++++++")

    


#App().run_tag(None, "pomcp", 10, 10, None, None, "benchmark")
#App().run_tag(None, "pbvi", 10, 10, None, None, "benchmark")


#App().run_tiger(None, "pomcp", 10, 10, None, None, "benchmark")
#App().run_tiger(None, "pbvi", 1, 10, None, None, "benchmark")

#App().run_bridge_repair(None, "pomcp", 10, 10, None, None, "benchmark")
#App().run_bridge_repair(None, "pbvi", 10, 10, None, None, "benchmark")

#App().run_car(None, "pomcp", 10, 10, None, None, "benchmark")
#App().run_car(None, "pbvi", 10, 10, None, None, "benchmark")