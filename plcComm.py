import snap7 #import library
import matplotlib.pyplot as plt

class plcComm:
    def __init__(self) -> None:#class construction
        pass

    def connection(self,ip_direction): #connection method to plc
        try:
            global client
            client=snap7.client.Client()#connector instance
            client.connect(ip_direction, 0, 1)#make connection: rack 0, slot 1 as default
            return client
        except Exception as err:
            print("Conexión no lograda")
            print(err)
            return(str(err))


    
    def read_from_db(self):
        #plc=self.connection() #connect to plc
        dbNumber=1
        startByte=0 #byte from which to start reading
        byteSize=4 #size of value to be read
        try:
           #result = plc.db_read(dbNumber, startByte, byteSize)
            result=client.db_read(dbNumber, startByte, byteSize)
            lecture=snap7.util.get_real(result,startByte)
            return lecture #get raw data and value on readable format
        except Exception as err:
            print("Lectura no ejecutada")
            print(err)

    def write_to_db(self,newValue=5.0):
        dbNumber=1
        startByte=0 #byte from which to start reading
        try:
            result = client.read_from_db() #read value to change it
            snap7.util.set_real(result,startByte,newValue)
            client.db_write(dbNumber,startByte,result)
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