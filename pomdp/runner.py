import os
import re

from lib.PyPOMDP.pypomdp.models import SampleModel, Model
from lib.PyPOMDP.pypomdp.solvers import POMCP, PBVI
from lib.PyPOMDP.pypomdp.parsers import PomdpParser, GraphViz
from lib.PyPOMDP.pypomdp.logger import Logger as log

class Runner:

    def __init__(self, params):
        self.params = params
        if params.logfile is not None:
            log.new(params.logfile)

    def create_model(self, env_configs):
        """
        Builder method for creating model (i,e, agent's environment) instance
        :param env_configs: the complete encapsulation of environment's dynamics
        :return: concrete model
        """
        MODELS = {
            'Sample': SampleModel,
        }
        return MODELS.get(env_configs['model_name'], Model)(env_configs)

    def create_solver(self, algo, model):
        """
        Builder method for creating solver instance
        :param algo: algorithm name
        :param model: model instance, e.g, TigerModel or RockSampleModel
        :return: concrete solver
        """
        SOLVERS = {
            'pbvi': PBVI,
            'pomcp': POMCP,
        }
        return SOLVERS.get(algo)(model)

    def snapshot_tree(self, visualiser, tree, filename):
        visualiser.update(tree.root)
        visualiser.render('./dev/snapshots/{}'.format(filename))  # TODO: parametrise the dev folder path

    def run_tag_interactive(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
            Starting Budget:  {}
            Init Belief: {}
            Time Horizon: {}
            Max Play: {}
        ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        def stop_condition(state):
               
                pattern = re.compile("^.*(tagged)$")
                return pattern.match(state) 
            
        i=0
        while not stop_condition(model.curr_state):
            
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            # print ino
            log.info('\n'.join([
            'Taking action: {}'.format(action),
            'Observation: {}'.format(obs),
            'Reward: {}'.format(reward),
            'Budget: {}'.format(budget),
            'New state: {}'.format(new_state),
            'New Belief: {}'.format(belief),
            '=' * 20
            ]))

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break
        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_tag_silent(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        def stop_condition(state):
               
                pattern = re.compile("^.*(tagged)$")
                return pattern.match(state) 
            
        i=0
        while not stop_condition(model.curr_state):
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break
        # print ino
        log.info('\n'.join([
        'Last reward: {}'.format(reward),
        'Final state: {}'.format(new_state),
        '=' * 20
        ]))
        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_tag_benchmark(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        steps = list()
        def stop_condition(state):
               
                pattern = re.compile("^.*(tagged)$")
                return pattern.match(state) 
            
        i=0
        for x in range(30): # 30 steps in order to get statistics
            print("========================================")
            while not stop_condition(model.curr_state): 
            
                # plan, take action and receive environment feedbacks
                pomdp.solve(T)
                action = pomdp.get_action(belief)

                # Add action of iteration to a list 
                all_actions.append(action)

                new_state, obs, reward, cost = pomdp.take_action(action)

                if params.snapshot and isinstance(pomdp, POMCP):
                    # takes snapshot of belief tree before it gets updated
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
                
                # update states
                belief = pomdp.update_belief(belief, action, obs)
                # Add total reward of iteration to a list 
                total_rewards += reward

                all_TotalRewards.append(float(total_rewards))
                all_rewards.append(float(reward))
                budget -= cost
                
                if budget <= 0:
                    log.info('Budget spent.')
                    break
                i=i+1
                if not stop_condition(model.curr_state):
                    steps.append(i)

            # print info
            print('Iteration: #'+str(x+1))
            log.info('\n'.join([
            'Last reward: {}'.format(reward),
            'Final state: {}'.format(new_state)
            ]))
            log.info('-- {} games played. Total reward = {}'.format(i, total_rewards))
            i = 0
            total_rewards = 0
            print("========================================\n")
        return all_actions, all_TotalRewards, all_rewards, steps

    def run_tiger_interactive(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
            Starting Budget:  {}
            Init Belief: {}
            Time Horizon: {}
            Max Play: {}
        ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
      
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            # print ino
            log.info('\n'.join([
            'Taking action: {}'.format(action),
            'Observation: {}'.format(obs),
            'Reward: {}'.format(reward),
            'Budget: {}'.format(budget),
            'New state: {}'.format(new_state),
            'New Belief: {}'.format(belief),
            '=' * 20
            ]))

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1
           
            stop_condition = str(action) == "open-left" or str(action) == "open-right"
            if stop_condition:
                break

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break


        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_tiger_silent(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1
           
            if  str(action) == "open-left" or str(action) == "open-right":
                break

        # print ino
        log.info('\n'.join([
        'Last reward: {}'.format(reward),
        'Final state: {}'.format(new_state),
        '=' * 20
        ]))

        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_tiger_benchmark(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        steps = list()
        i=0
        for x in range(30): # 30 steps in order to get statistics
            print("========================================")
            while True: # 30 steps in order to get statistics
            
                # plan, take action and receive environment feedbacks
                pomdp.solve(T)
                action = pomdp.get_action(belief)
                

                # Add action of iteration to a list 
                all_actions.append(action)

                new_state, obs, reward, cost = pomdp.take_action(action)

                if params.snapshot and isinstance(pomdp, POMCP):
                    # takes snapshot of belief tree before it gets updated
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
                
                # update states
                belief = pomdp.update_belief(belief, action, obs)
                # Add total reward of iteration to a list 
                total_rewards += reward

                all_TotalRewards.append(float(total_rewards))
                all_rewards.append(float(reward))
                budget -= cost

                if budget <= 0:
                    log.info('Budget spent.')
                    break
                i=i+1

                if  str(action) == "open-left" or str(action) == "open-right":
                    steps.append(i)
                    break
            # print info
            print('Iteration: #'+str(x+1))
            log.info('\n'.join([
            'Last reward: {}'.format(reward),
            'Final state: {}'.format(new_state)
            ]))
            log.info('-- {} games played. Total reward = {}'.format(i, total_rewards))
            i = 0
            total_rewards = 0
            print("========================================\n")
        return all_actions, all_TotalRewards, all_rewards, steps


    def run_bridge_interactive(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
            Starting Budget:  {}
            Init Belief: {}
            Time Horizon: {}
            Max Play: {}
        ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
      
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            # print ino
            log.info('\n'.join([
            'Taking action: {}'.format(action),
            'Observation: {}'.format(obs),
            'Reward: {}'.format(reward),
            'Budget: {}'.format(budget),
            'New state: {}'.format(new_state),
            'New Belief: {}'.format(belief),
            '=' * 20
            ]))

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1
           
            paint_visual = "clean-paint-and-visual-inspect"
            paint_strength = "paint-strengthen-and-visual-inspect"
            repair_ut_inspect = "structural-repair-and-ut-inspect"
            stop_condition = paint_visual in all_actions and paint_strength in all_actions and repair_ut_inspect in all_actions

            if  stop_condition:
                break

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break
        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards


    def run_bridge_silent(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')

        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
      
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1
           
            paint_visual = "clean-paint-and-visual-inspect"
            paint_strength = "paint-strengthen-and-visual-inspect"
            repair_ut_inspect = "structural-repair-and-ut-inspect"
            stop_condition = paint_visual in all_actions and paint_strength in all_actions and repair_ut_inspect in all_actions

            if  stop_condition:
                break

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break
        # print ino
        log.info('\n'.join([
        'Last reward: {}'.format(reward),
        'Final state: {}'.format(new_state),
        '=' * 20
        ]))
        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards


    def run_bridge_benchmark(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))
        
        print('\n~~~ Running simulation ~~~\n')

        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        steps = list()

        i=0
        for x in range(30): # 30 steps in order to get statistics
            print("========================================")
            while True:
            
                # plan, take action and receive environment feedbacks
                pomdp.solve(T)
                action = pomdp.get_action(belief)
                

                # Add action of iteration to a list 
                all_actions.append(action)

                new_state, obs, reward, cost = pomdp.take_action(action)

                if params.snapshot and isinstance(pomdp, POMCP):
                    # takes snapshot of belief tree before it gets updated
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
                
                # update states
                belief = pomdp.update_belief(belief, action, obs)
                # Add total reward of iteration to a list 
                total_rewards += reward

                all_TotalRewards.append(float(total_rewards))
                all_rewards.append(reward)
                budget -= cost

                if budget <= 0:
                    log.info('Budget spent.')
                    break

                i=i+1
                paint_visual = "clean-paint-and-visual-inspect"
                paint_strength = "paint-strengthen-and-visual-inspect"
                repair_ut_inspect = "structural-repair-and-ut-inspect"
                stop_condition = paint_visual in all_actions and paint_strength in all_actions and repair_ut_inspect in all_actions

                if  stop_condition:
                    steps.append(i)
                    break
                
            # print info
            print('Iteration: #'+str(x+1))
            log.info('\n'.join([
            'Last reward: {}'.format(reward),
            'Final state: {}'.format(new_state)
            ]))
            log.info('-- {} games played. Total reward = {}'.format(i, total_rewards))
            i = 0
            total_rewards = 0
            print("========================================\n")
        return all_actions, all_TotalRewards, all_rewards, steps



    def run_car_interactive(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
            Starting Budget:  {}
            Init Belief: {}
            Time Horizon: {}
            Max Play: {}
        ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))
        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
      
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(reward)
            budget -= cost

            # print ino
            log.info('\n'.join([
            'Taking action: {}'.format(action),
            'Observation: {}'.format(obs),
            'Reward: {}'.format(reward),
            'Budget: {}'.format(budget),
            'New state: {}'.format(new_state),
            'New Belief: {}'.format(belief),
            '=' * 20
            ]))

            if budget <= 0:
                log.info('Budget spent.')
                break

            i=i+1
             
            stop_condition = str(action) == "choose-mid" or str(action) == "choose-right" or str(action) == "choose-left"

            if  stop_condition:
                break

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break


        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_car_silent(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))

        print('\n~~~ Running simulation ~~~\n')

        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
      
        i=0
        while True:
           
            # plan, take action and receive environment feedbacks
            pomdp.solve(T)
            action = pomdp.get_action(belief)
            

            # Add action of iteration to a list 
            all_actions.append(action)

            new_state, obs, reward, cost = pomdp.take_action(action)

            if params.snapshot and isinstance(pomdp, POMCP):
                # takes snapshot of belief tree before it gets updated
                self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
            
            # update states
            belief = pomdp.update_belief(belief, action, obs)
            # Add total reward of iteration to a list 
            total_rewards += reward

            all_TotalRewards.append(float(total_rewards))
            all_rewards.append(float(reward))
            budget -= cost

            if budget <= 0:
                log.info('Budget spent.')
                break
            i=i+1
             
            stop_condition = str(action) == "choose-mid" or str(action) == "choose-right" or str(action) == "choose-left"

            if  stop_condition:
                break

            # If params.max_play <= 0 then, it means that max_play is unlimited 
            if params.max_play>0 and i>=params.max_play:
                break

        # print ino
        log.info('\n'.join([
        'Last reward: {}'.format(reward),
        'Final state: {}'.format(new_state),
        '=' * 20
        ]))
        log.info('{} games played. Total reward = {}'.format(i, total_rewards))
        return all_actions, all_TotalRewards, all_rewards

    def run_car_benchmark(self, algo, T, **kwargs):
        
        visualiser = GraphViz(description='tmp')
        params, pomdp = self.params, None
        total_rewards, budget = 0, params.budget

        log.info('~~~ initialising ~~~')
        with PomdpParser(params.env_config) as ctx:
            # creates model and solver
            model = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algo, model)

            # supply additional algo params
            belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

            if algo == 'pbvi':
                belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                pomdp.add_configs(belief_points)
            elif algo == 'pomcp':
                pomdp.add_configs(budget, belief, **kwargs)

        
        log.info('''
        ++++++++++++++++++++++
            Starting State:  {}
        ++++++++++++++++++++++'''.format(model.curr_state))

        print('\n~~~ Running simulation ~~~\n')

        
        all_actions = list()
        all_TotalRewards= list()
        all_rewards = list()
        steps = list()
      
        i=0
        for x in range(30): # 30 steps in order to get statistics
            print("========================================")
            while True:
            
                # plan, take action and receive environment feedbacks
                pomdp.solve(T)
                action = pomdp.get_action(belief)
                

                # Add action of iteration to a list 
                all_actions.append(action)

                new_state, obs, reward, cost = pomdp.take_action(action)

                if params.snapshot and isinstance(pomdp, POMCP):
                    # takes snapshot of belief tree before it gets updated
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))
                
                # update states
                belief = pomdp.update_belief(belief, action, obs)
                # Add total reward of iteration to a list 
                total_rewards += reward

                all_TotalRewards.append(float(total_rewards))
                all_rewards.append(float(reward))
                budget -= cost

                if budget <= 0:
                    log.info('Budget spent.')
                    break
                    
                i=i+1
                stop_condition = str(action) == "choose-mid" or str(action) == "choose-right" or str(action) == "choose-left"

                if  stop_condition:
                    steps.append(i)
                    break
            
            # print info
            print('Iteration: #'+str(x+1))
            log.info('\n'.join([
            'Last reward: {}'.format(reward),
            'Final state: {}'.format(new_state)
            ]))
            log.info('-- {} games played. Total reward = {}'.format(i, total_rewards))
            i = 0
            total_rewards = 0
            print("========================================\n")
        return all_actions, all_TotalRewards, all_rewards, steps