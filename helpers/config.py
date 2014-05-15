import json
import io

defaultConfigName = "exampleTdster.cfg"

def makeDefaultConfig():
    config = {}
    config["reportOutputDirectory"] = "/PATH/TO/REPORT/OUTPUT/DIR"
    config["tmpDataDir"] = '/tmp'
    config["testServers"] =  ["http://thredds.ucar.edu/", "http://thredds-test.unidata.ucar.edu/"]
    config["dateFormat"] = "%Y-%m-%d %H%M"
    configName = defaultConfigName
    with io.open(configName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(config, ensure_ascii=False, indent=2)))

def readConfig(configFile = defaultConfigName):
    with io.open(configFile, 'r', encoding='utf-8') as cfg:
        config = json.load(cfg)
    return config
