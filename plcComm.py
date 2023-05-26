import snap7 #import library
import matplotlib.pyplot as plt

class plcComm:
    def __init__(self) -> None:#class construction
        pass

    def connection(self,ip_direction="192.168.0.2"): #connection method to plc
        try:
            client=snap7.client.Client()#connector instance
            client.connect(ip_direction, 0, 1)#make connection: rack 0, slot 1 as default
            return client
        except Exception as err:
            print("Conexión no lograda")
            print(err)
    
    def read_from_db(self):
        plc=self.connection() #connect to plc
        dbNumber=1
        startByte=0 #byte from which to start reading
        byteSize=4 #size of value to be read
        try:
            result = plc.db_read(dbNumber, startByte, byteSize)
            lecture=snap7.util.get_real(result,startByte)
            return result,lecture #get raw data and value on readable format
        except Exception as err:
            print("Lectura no ejecutada")
            print(err)

    def write_to_db(self,newValue=5.0):
        plc=self.connection()
        dbNumber=1
        startByte=0 #byte from which to start reading
        try:
            result = self.read_from_db()[0] #read value to change it
            snap7.util.set_real(result,startByte,newValue)
            plc.db_write(dbNumber,startByte,result)
            print("Escritura ejecutada")
        except Exception as err:
            print("Escritura no ejecutada")
            print(err)

    '''
    def plotting_level(self,flag=True):
        if flag==True:
            plc=self.connection()
            try:
                fig,ax=plt.subplots(11) #create plot object
                ax.plot()
            except Exception as err:
                print("Graficación no realizada")
                print(err)
        else:
            print("Graficación terminada")
    #unused for now
    '''