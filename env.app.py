'''
setup environemnt and retrieve variables
'''
import os

if __name__ == '__main__' :
    print("__main__")
    os.environ["TEST"] = "Hello, world"
    print("env TEST : ", os.environ["TEST"])
    print("env PATH : ", os.environ["PATH"])

