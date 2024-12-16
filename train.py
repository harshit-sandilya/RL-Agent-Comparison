from env import Env
from stable_baselines3 import DDPG
from stable_baselines3.common.callbacks import BaseCallback


class TensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TensorboardCallback, self).__init__(verbose)

    def _on_step(self):
        self.logger.record("train/reward", self.locals["rewards"])
        return True


env = Env(8, 10)
model = DDPG("MlpPolicy", env, tensorboard_log="logs/DDPG", verbose=1)
model.learn(total_timesteps=1000000, callback=[TensorboardCallback()])
model.save("DDPG")
