import re
import types
import pickle
import logging
import os,sys
sys.path.append(f"{os.getcwd()}")

_py_ptn = re.compile("(.+)\.py\Z")

class Base:
    def __init__(self,path,name) -> None:
        self.__path = path
        self.__name = name
    def __setstate__(self,state):
        self.__dict__ = state
    def __getstate__(self):
        return self.__dict__
    @property
    def path(self):
        return self.__path
    @property
    def name(self):
        return self.__name

class AssetExplorer(Base):
    def __init__(self,path,name) -> None:
        super().__init__(path,name)
        self.__structure = []
    def PYTHON_ASSET(self,progress:types.ModuleType=None):
        if progress:
            for struct in self.__structure:
                if isinstance(struct,AssetPythonFile):
                    struct.LOAD()
                    print(struct.MODULE_NAME)
                    progress.__dict__[struct.MODULE_NAME] = struct.MODULE
                elif isinstance(struct,AssetExplorer):
                    package = types.ModuleType(self.name)
                    progress.__dict__[struct.name] = package
                    struct.PYTHON_ASSET(package)
            return progress
        else:
            progress = types.ModuleType(self.name,"AssetPackage")
            self.PYTHON_ASSET(progress)
            return progress
    def dump(self,place):
        with open(place,"wb") as f:
            f.write(pickle.dumps(self))
    def get(self,name):
        for _ in self.__structure:
            if _.name == name:
                return _
    def loot(self,*names):
        progress = None
        for _,name in enumerate(names):
            if progress:
                progress = progress.get(name)
            else:
                progress = self.get(name)
            if not progress:
                logging.error(f"Your search '{name}' not found")
                return
            if _ == len(names)-1:
                return progress
            if not isinstance(progress,AssetExplorer):
                logging.error(f"Searched '{progress.name}' cannot proceed any further")
                return
        return progress
    @classmethod
    def view(cls,exploror,indent=0,space=2):
        for _ in exploror.structure:
            IDN = (" "*space)*indent
            if isinstance(_,AssetFile):
                print(IDN+"◇ "+_.name)
            elif isinstance(_,AssetExplorer):
                print(IDN+"◆ "+_.name)
                AssetExplorer.view(_,indent+1,space)
    def _DICT_STRUCT(self):
        for _ in self.structure:
            self.__dict__[_.name] = _
    @property
    def structure(self):
        return self.__structure
    def add(self,struc):
        if isinstance(struc,(AssetExplorer,AssetFile)):
            self.__structure.append(struc)
        else:
            raise TypeError(f"Objects not supported.{struc}")
    @classmethod
    def patch(cls,path,progress,name,first=True,BASE=None):
        if first:
            BASE = progress
        if isinstance(progress,AssetExplorer):
            nn = path[len(name):]
            try:
                structs = os.listdir(path)
            except NotADirectoryError:
                match = _py_ptn.match(path)
                if bool(match):
                    progress.add(AssetPythonFile(path,nn[1:],home=BASE))
                else:
                    progress.add(AssetFile(path,nn[1:],home=BASE))
            else:
                if first:
                    for _ in structs:
                        AssetExplorer.patch(f"{path}/{_}",progress,path,False,BASE)
                else:
                    expl = AssetExplorer(path,nn[1:])
                    for _ in structs:
                        AssetExplorer.patch(f"{path}/{_}",expl,path,False,BASE)
                    progress.add(expl)
        #progress._DICT_STRUCT()
        return progress

class AssetFile(Base):
    def __init__(self,path,name,home=None) -> None:
        super().__init__(path,name)
        self.__data = None
        self.base = home
    def __getstate__(self):
        return super().__getstate__().update(self.__dict__)
    @property
    def data(self):
        return self.__data
    def set_deta(self,deta:str):
        if isinstance(deta,str):
            self.__data = deta
    def load_data(self,path,mode="r",encode="UTF-8"):
        with open(path,mode,encoding=encode) as f:
            self.__data = f.read()

class AssetPythonFile(AssetFile):
    _INSTANS = []
    def __init__(self, path, base,home=None, load=True,data=True) -> None:
        super().__init__(path,base,home=home)
        self.__load = load
        self.__data = data
        self.__module_name = _py_ptn.match(self.name).group(1)
        self.__MODULE = None
        AssetPythonFile._INSTANS.append(self)
        if self.__data:
            self.load_data(self.path)
        if self.__load:
            self.LOAD()
    @classmethod
    def EXEC(cls):
        for instance in AssetPythonFile._INSTANS:
            instance.LOAD()
    def __setstate__(self,state):
        if self.__data:
            self.load_data(self.path)
        if self.__load:
            self.LOAD()
    def __getstate__(self):
        self.load_data(self.path)
        self.__MODULE = None
        self.__data = False
        self.__code = None
        self.__load = True
        return self.__dict__
    def __del__(self):
        if self in AssetPythonFile._INSTANS:
            AssetPythonFile._INSTANS.remove(self)
    @property
    def MODULE_NAME(self):
        return self.__module_name
    @property
    def MODULE(self):
        return self.__MODULE
    def RUN(self):
        def _import(*loots):
            _ = self.base.loot(*loots)
            if isinstance(_,AssetPythonFile):
                _.RUN()
            return _.MODULE
        self.__MODULE.__dict__["_import"] = _import
        exec(self.__code,self.__MODULE.__dict__)
    def LOAD(self):
        self.__MODULE = types.ModuleType(self.path,"AssetModule")
        self.__code = compile(self.data,"<No definition>","exec")

class AssetUnpicker(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        __module_name = __name__
        return super().find_class(__module_name, __global_name)


