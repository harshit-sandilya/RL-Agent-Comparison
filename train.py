from env import Env
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback


class TensorboardCallback(BaseCallback):
    def __init__(self, env, verbose=0):
        super(TensorboardCallback, self).__init__(verbose)
        self.env = env

    def _on_step(self) -> bool:
        self.logger.record("env/index", self.env.index)
        self.logger.record("env/visited_same", self.env.visited_same)
        self.logger.record("env/on_mine", self.env.on_mine)
        self.logger.record("env/won_game", self.env.won_game)
        self.logger.record("env/reward", self.env.reward)
        return True


class DebugCallback(BaseCallback):
    def __init__(self, env, verbose=0):
        super(DebugCallback, self).__init__(verbose)
        self.env = env

    def _on_step(self) -> bool:
        print(
            f"Step: {self.num_timesteps}, Reward: {self.locals['rewards']}, Index: {self.env.index}, Won Last: {self.env.wonLast}, Action: {self.env.action}"
        )
        return True


env = Env(8, 10)
model = PPO("MlpPolicy", env, tensorboard_log="logs/PPO", gamma=0, learning_rate=0.0001)
model.learn(
    total_timesteps=10000000,
    callback=[TensorboardCallback(env), DebugCallback(env)],
    progress_bar=True,
)
model.save("models/PPO")
