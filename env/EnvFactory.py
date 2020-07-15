from env.LocalEnv import LocalEnv
from env.LinetestEnv import LinetestEnv
from env.ProductEnv import ProductEnv

class EnvFactory():
    def getEnv(self, type):
        if (type == 'local'):
            return LocalEnv()
        if (type == 'linetest'):
            return LinetestEnv()
        if (type=='product'):
            return ProductEnv()


if __name__ == '__main__':
    ef = EnvFactory()
    env = ef.getEnv('product')
    print(env.getUrl())








