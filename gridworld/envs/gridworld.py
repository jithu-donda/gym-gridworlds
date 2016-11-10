import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

""" n x n gridworld
"""

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class GridWorld(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, n = 5, noise = 0.0, terminal_reward = 1.0, 
          border_reward = -1.0, step_reward = 0.0, start_state = 'random'):
    self.n = n
    self.noise = noise
    self.terminal_reward = terminal_reward
    self.border_reward = border_reward
    self.step_reward = step_reward
    self.n_states = self.n ** 2 + 1
    self.terminal_state = self.n_states - 2
    self.absorbing_state = self.n_states - 1
    self.done = False
    self.start_state = start_state #if not isinstance(start_state, str) else np.random.rand(n**2)
    self._reset()

    self.action_space = spaces.Discrete(4)
    self.observation_space = spaces.Discrete(self.n_states) # with absorbing state
    #self._seed()

  def _step(self, action):
    assert self.action_space.contains(action)

    [row, col] = self.ind2coord(self.state)

    if np.random.rand() < self.noise:
      action = self.action_space.sample()

    if action == UP:
      row = max(row - 1, 0)
    elif action == DOWN:
      row = min(row + 1, self.n - 1)
    elif action == RIGHT:
      col = min(col + 1, self.n - 1)
    elif action == LEFT:
      col = max(col - 1, 0)

    self.state = self.coord2ind([row, col])

    if self.state == self.terminal_state:
      self.state = self.absorbing_state
      self.done = True

    reward = self._get_reward()

    return self.state, reward, self.done, None

  def _get_reward(self):
    if self.done:
      return self.terminal_reward

    reward = self.step_reward
    [row, col] = self.ind2coord(self.state)
    if row == 0 or row == self.n - 1 or col == 0 or col == self.n - 1:
      reward = self.border_reward
    return reward


  def ind2coord(self, index):
    assert(index >= 0)
    assert(index < self.n_states - 1)

    col = index // self.n
    row = index % self.n

    return [row, col]


  def coord2ind(self, coord):
    [row, col] = coord
    assert(row < self.n)
    assert(col < self.n)

    return col * self.n + row


  def _reset(self):
    self.state = self.start_state if not isinstance(self.start_state, str) else np.random.randint(self.n_states-1)
    self.done = False
    return self.state

  def _render(self, mode='human', close=False):
    return None