

class SessionBase:
    def __init__(self,ServerAdress,PortNumber) -> None:
        self.__server_address = ServerAdress
        self.__port_number = PortNumber
    def connect(self):
        raise NotImplementedError
    @property
    def ServerAdress(self):
        return self.__server_address
    @property
    def PortNumber(self):
        return self.__port_number

class GeneralSession(SessionBase):
    def __init__(self, ServerAdress, PortNumber) -> None:
        super().__init__(ServerAdress, PortNumber)