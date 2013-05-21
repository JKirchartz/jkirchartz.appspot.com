import os, sys

# add lib to sys.path
path = os.path.dirname(__file__)
sys.path.append(path)

# import modules within the dir so they are cached
for name in os.listdir(path):
    if name.endswith('.py') and '__init__' not in name:
        name = name.rstrip('.py')
    elif not os.path.isdir(os.path.join(path,name)):
        continue
    __import__(name)
