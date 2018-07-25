#Este Script abre los archivos .txt que contienen las capturas y crea archivos .csv con los paquetes de DR0 y DR3
#Al final, genera un archivo Total
#Creado por: Pablo E. Avila C - UCuenca
import csv
import subprocess
import statistics
#Directorios de las mediciones y de los resultados
path = 'D:\\Users\\Pablo\\MEGAsync\\LoRaTesis\\Data\\Capturas\\Clase'
pathr = 'D:\\Users\\Pablo\\MEGAsync\\LoRaTesis\\Data\\Capturas\\Clase\\Conversiones'
npackets = 10                                                                                                           #No de paquetes por transmisión
ncaptures = 1                                                                                                          #No. de capturas en la medición
RSSIAVEA = [0]*ncaptures
RSSIAVEB = [0]*ncaptures
SNRAVEA = [0]*ncaptures
SNRAVEB = [0]*ncaptures
DIST = [0]*ncaptures
PERSA = [0]*ncaptures
PERSB = [0]*ncaptures
STDDEVRSSIA = [0]*ncaptures
STDDEVRSSIB = [0]*ncaptures
STDDEVSNRA = [0]*ncaptures
STDDEVSNRB = [0]*ncaptures

for file in range(1,ncaptures+1):
    #Name of file
    nfile= str(file)
    data = open(path+'\\'+nfile+'.txt','r').read()
    dataDic = {}
    dataDicA = {}
    dataDicB = {}
    #Index of values
    tmstp=[pos for pos in range(len(data)) if data[pos:].startswith('tmst')]
    chanp=[pos for pos in range(len(data)) if data[pos:].startswith('chan')]
    rfchp=[pos for pos in range(len(data)) if data[pos:].startswith('rfch')]
    freqp=[pos for pos in range(len(data)) if data[pos:].startswith('freq')]
    modup=[pos for pos in range(len(data)) if data[pos:].startswith('modu')]
    datrp=[pos for pos in range(len(data)) if data[pos:].startswith('datr')]
    codrp=[pos for pos in range(len(data)) if data[pos:].startswith('codr')]
    lsnrp=[pos for pos in range(len(data)) if data[pos:].startswith('lsnr')]
    rssip=[pos for pos in range(len(data)) if data[pos:].startswith('rssi')]
    sizep=[pos for pos in range(len(data)) if data[pos:].startswith('size')]
    datap=[pos for pos in range(len(data)) if data[pos:].startswith('data')]
    #Packet Number
    n = int(len(tmstp)/2)
    #Extract data
    dataDic[0] = 'TMST','CHAN','RFCH','FREQ','MODU','DATR','CODR','LSNR','RSSI','SIZE','DATA'
    dataDicA[0] = 'TMST','CHAN','RFCH','FREQ','MODU','DATR','CODR','LSNR','RSSI','SIZE','DATA'
    dataDicB[0] = 'TMST','CHAN','RFCH','FREQ','MODU','DATR','CODR','LSNR','RSSI','SIZE','DATA'
    for index in range(0, n):
        DATA = data[datap[index]+7:datap[index]+36]                                                                         #Tomo la parte de los Datos
        DATAB = DATA[0:DATA.index('"')]                                                                                     #Tomo solo hasta las comillas (Data es variable)
        DATAC = subprocess.check_output('lora-decrypt ' + DATAB, shell=True).decode('utf-8')                                #Desemcripto y convierto a string
        DATAD = DATAC[8:DATAC.index('>')].replace(" ", "")                                                                  #Tomo solo los datos hasta > y elimino espacios
        dataDic[index+1] = int(data[tmstp[index]+6:chanp[index]-2]),int(data[chanp[index]+6:rfchp[index]-2]),int(data[rfchp[index]+6:freqp[index]-2]),float(data[freqp[index]+6:freqp[index]+16]),str(data[modup[index]+7:datrp[index]-3]),str(data[datrp[index]+7:codrp[index]-3]),str(data[codrp[index]+7:lsnrp[index]-3]),float(data[lsnrp[index]+6:rssip[index]-2]),int(data[rssip[index]+6:sizep[index]-2]),int(data[sizep[index]+6:datap[index]-2]),int(DATAD)

    #Separe DRO and DR3
    i=1
    j=1
    for index in range(0,n):
        line = dataDic[index+1]
        if line[5] == "SF10BW125":
            dataDicA[i]=line
            i+=1
        else:
            dataDicB[j]=line
            j+=1
    #No of Received Data
    npacketsrecA = len(dataDicA)-1
    npacketsrecB = len(dataDicB)-1

    #Extract RSSIs into vectors
    RSSIA = [0]*npacketsrecA
    RSSIB = [0]*npacketsrecB

    for index in range(1,npacketsrecA+1):
        line = dataDicA[index]
        RSSIA[index-1]= line[8]

    for index in range(1,npacketsrecB+1):
        line = dataDicB[index]
        RSSIB[index-1]= line[8]
    #Extract SNRs into vectors
    SNRA = [0]*npacketsrecA
    SNRB = [0]*npacketsrecB

    for index in range(1,npacketsrecA+1):
        line = dataDicA[index]
        SNRA[index-1]= line[7]

    for index in range(1,npacketsrecB+1):
        line = dataDicB[index]
        SNRB[index-1]= line[7]

    DIST[file - 1] = file * 10                                                                                          #Distances Vector

    if len(dataDicA) > 1: #To avoid 0 files. When there are just DR0 messages or none
        RSSIAVEA[file-1] = statistics.mean(RSSIA)
        SNRAVEA[file-1] = statistics.mean(SNRA)
        PERSA[file-1] = (npackets-npacketsrecA)/(npackets)
        if len(dataDicA) > 2: #STANDARDDEV needs at least two values
            STDDEVRSSIA[file-1] = statistics.stdev(RSSIA)
            STDDEVSNRA[file-1] = statistics.stdev(SNRA)
        # Saving Data into the .csv file
        w = csv.writer(open(pathr+'\\'+nfile+"A"+".csv", "w", newline=''))
        for key, val in dataDicA.items():
            w.writerow(val)

    if len(dataDicB) > 1: #To avoid 0 files. When there are just DR0 messages or none
        RSSIAVEB[file-1] = statistics.mean(RSSIB)
        SNRAVEB[file-1] = statistics.mean(SNRB)
        PERSB[file-1] = (npackets-npacketsrecB)/(npackets)
        if len(dataDicB) > 2: #STANDARDDEV needs at least two values
            STDDEVRSSIB[file-1] = statistics.stdev(RSSIB)
            STDDEVSNRB[file-1] = statistics.stdev(SNRB)
        # Saving Data into the .csv file
        w = csv.writer(open(pathr+'\\'+nfile+"B"+".csv", "w", newline=''))
        for key, val in dataDicB.items():
            w.writerow(val)

headers = ['Distancia(m)','RSSI_DR0(dBm)','SNR_DR0','STDEVRSSI_DR0','STDEVSNR_DR0','PER_DR0','RSSI_DR3(dBm)','SNR_DR3','STDEVRSSI_DR3','STDEVSNR_DR3','PER_DR3']
rows = zip(DIST,RSSIAVEA,SNRAVEA,STDDEVRSSIA,STDDEVSNRA,PERSA,RSSIAVEB,SNRAVEB,STDDEVRSSIB,STDDEVSNRB,PERSB)
w = csv.writer(open(pathr+'\\'+'RESULTADOS'+'.csv',"w", newline=''))
w.writerow(headers)
for row in rows:
    w.writerow(row)
print('Decodificacion Terminada!')