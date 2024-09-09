
class Error:
    ERRORS = []
    def __init__(self,number,order,description) -> None:
        self.__number = number
        self.__order = order
        self.__description = description
        if isinstance(self,Error):
            Error.ERRORS.append(self)
    @classmethod
    def getError(cls,number):
        for error in Error.ERRORS:
            if error.number == number:
                return error
    @property
    def order(self):
        return self.__order
    @property
    def number(self):
        return self.__number
    @property
    def description(self):
        return self.__description

class ERROR_BASE:
    def __init__(self,number) -> None:
        self.__number = number
    @property
    def number(self):
        return self.__number

class AccountError(ERROR_BASE):
    """
    アカウントに関連するエラー
    """
    def __init__(self, number) -> None:
        super().__init__(number)

class DataIntegrityError(ERROR_BASE):
    """
    データの型や整合性に関するエラー
    """
    def __init__(self, number) -> None:
        super().__init__(number)

Error(0,ERROR_BASE,"エラーは発生していません")
Error(1,AccountError,"アカウントのログインに失敗")
Error(2,DataIntegrityError,"データの整合性が正しくありません")