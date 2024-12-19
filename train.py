from env import Env
from stable_baselines3 import DQN

# from sb3_contrib import DQN
from stable_baselines3.common.callbacks import BaseCallback


class TensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TensorboardCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        self.logger.record("train/reward", self.locals["rewards"])
        return True


env = Env(8, 10, False)
model = DQN("MlpPolicy", env, tensorboard_log="logs/DQN")
model.learn(
    total_timesteps=10000000, callback=[TensorboardCallback()], progress_bar=True
)
model.save("DQN")
