import json

class jsonUpdater:
    base:        dict = {}
    docs:        dict = {}
    methods:     dict = {}
    props:       dict = {}
    profs:       dict = {}
    tricks:     dict = {}

    basePath: str  = 'database/datas/base.json'
    docsPath: str = "database/datas/docs.json"
    methodsPath: str = "database/datas/methods.json"
    propsPath: str = "database/datas/props.json"
    profsPath: str = "database/datas/profiles.json"
    tricksPath: str = "database/datas/tricks.json"

    def updateJson(self) -> None:

        with open(self.basePath, "r", encoding="utf-8") as jsonBase:
            self.base = json.load(jsonBase)
        with open(self.docsPath, "r", encoding="utf-8") as jsonDocs:
            self.docs = json.load(jsonDocs)
        with open(self.methodsPath, "r", encoding="utf-8") as jsonMethods:
            self.methods = json.load(jsonMethods)
        with open(self.propsPath, "r", encoding="utf-8") as jsonProps:
            self.props = json.load(jsonProps)
        with open(self.profsPath, "r", encoding="utf-8") as jsonProfs:
            self.profs = json.load(jsonProfs)
        with open(self.tricksPath, "r", encoding="utf-8") as jsontricks:
            self.tricks = json.load(jsontricks)