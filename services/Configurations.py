import configparser

CONFIGURATIONS = configparser.ConfigParser()
CONFIGURATIONS.read("/home/hedi/wattabot/wattabot.ini")


def connectorConfig(name: str):
    return int(CONFIGURATIONS["CONNECTORS"][name])


def cameraConfig(name: str):
    return int(CONFIGURATIONS["CAMERA"][name])


def secretConfig(name: str):
    return CONFIGURATIONS["SECRET"][name]
