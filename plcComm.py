%pip install python-snap7 #installations

import snap7 #import library
import ctypes #to create array to store results from reading


class plcComm:
    def __init__(self) -> None:#class construction
        pass

    def connection(self,ip_direction="192.168.0.2"): #connection method to plc
        client=snap7.client.Client()#connector instance
        client.connect(ip_direction, 0, 1)#make connection: rack 0, slot 1 as default
        return client
    
    def read_from_db(self):
        plc=self.connection()
        dbNumber=1
        startByte=0
        byteSize=4
        try:
            result = plc.db_read(dbNumber, startByte, byteSize)
            lecture=snap7.util.get_real(result,startByte)
            return lecture
        except Exception as err:
            print("Lectura no ejecutada")
            print(err)