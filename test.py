import numpy as np
from env import Env
from stable_baselines3 import PPO

env = Env(8, 10)
model = PPO("MlpPolicy", env)
model = model.load("models/PPO.zip")

games = 10
won = 0
for i in range(games):
    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs = np.array(obs)
        obs, reward, done, _, info = env.step(action)
        env.render()
        print(f"Reward: {reward}")
        if reward == 100:
            won += 1

print(f"Total games: {games}, Total wins: {won}, Win rate: {won / games:.2f}")
