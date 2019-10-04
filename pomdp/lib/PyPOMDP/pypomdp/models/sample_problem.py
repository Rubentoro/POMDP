from .model import Model

class SampleModel(Model):
    def __init__(self, env):
        Model.__init__(self, env)
        size, num = self.model_spec.split('x')
        self.size = int(size)
        self.num = int(num)
