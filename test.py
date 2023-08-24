import configparser

parser = configparser.ConfigParser()
parser.read("config.txt")
print(parser.sections())
config = parser["config"]["db"]
print(config)
