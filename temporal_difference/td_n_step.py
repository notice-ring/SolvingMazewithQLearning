import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from collections import defaultdict, deque
import numpy as np
from common.mazeworld import MazeWorld

class TDNStepAgent:
    def __init__(self):
        self.gamma = 0.9
        self.alpha = 0.01
        self.lamda = 0.9
        self.action_size = 4

        random_actions = {0: 0.25, 1: 0.25, 2: 0.25, 3:0.25}
        self.pi = defaultdict(lambda: random_actions)
        self.V = defaultdict(lambda: 0)
        self.memory_R = []
        self.memory_G = []

    def get_action(self, state):
        action_probs = self.pi[state]
        actions = list(action_probs.keys())
        probs = list(action_probs.values())
        
        return np.random.choice(actions, p=probs)
    
    def reset(self):
        self.memory_R.clear()
        self.memory_G.clear()
    
    def eval_nstep(self, state, reward, next_state, done):
        self.memory_R.append(reward)

        next_V = 0 if done else self.V[next_state]
        G_n = next_V
        for r in reversed(self.memory_R):
           G_n *= self.gamma
           G_n += r
        
        self.memory_G.append(G_n)
        target = 0
        for g in reversed(self.memory_G):
            target *= self.lamda
            target += g
        target *= (1 - self.lamda)

        self.V[state] += (target - self.V[state]) * self.alpha


if __name__ == '__main__':
    env = MazeWorld()
    agent = TDNStepAgent()

    episodes = 5000
    for episode in range(episodes):
        state = env.reset()
        agent.reset()

        while True:
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)

            agent.eval_nstep(state, reward, next_state, done)
            if done:
                break
            state = next_state

    env.render_v(agent.V)