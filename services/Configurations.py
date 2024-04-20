import configparser

CONFIGURATIONS = configparser.ConfigParser()
CONFIGURATIONS.read("wattabot.ini")


def connectorConfig(name: str):
    return int(CONFIGURATIONS["CONNECTORS"][name])


def cameraConfig(name: str):
    return int(CONFIGURATIONS["CAMERA"][name])
