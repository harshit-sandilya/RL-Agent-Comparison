import gymnasium as gym
from stable_baselines3.common.env_checker import check_env
from env import Env

env = Env(8, 10)
check_env(env)
