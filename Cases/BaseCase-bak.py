#coding=utf-8
import configparser
from env.EnvFactory import EnvFactory
import unittest
import os

class BaseCase(unittest.TestCase):

    def __init__(self, methodName):
        config = configparser.ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)
        envname = config.get("testServer", "env")
        ef = EnvFactory()
        env = ef.getEnv(envname)
        self.env = env
        self.config = config