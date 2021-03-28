import csv
import pandas_datareader as web
import yfinance as yf 
import sys

## Tableau de symboles
def symbol_extract(filename):
    
    Symboles = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        line = 0
        for i in reader: 
            if line == 0: 
                line+=1
            else :
                Symboles.append([i[0],i[1]])
                line+=1
    nInit = len(Symboles)
    print("Nombre de symboles:",nInit)
    return Symboles

#print(Symboles[1])

## Dictionnaire de données (pas optimal, à changer)
Symboles= symbol_extract("symboles.csv")
with open('dataset.csv','w', newline='') as wfile:
    writer = csv.writer(wfile)
    
    Data = {}
    errorList = []
    i = 0 
    for s in Symboles:
        try :
            
    
            #values = web.DataReader(s[1], 'yahoo', '1/1/2021')
            sf = yf.Ticker(s[1])
            donnees = ''
            for _ , d in sf.info.items():
                donnees+=str(d)+';'
            
            #Data[s[1]] = [values, sf.info]
            writer.writerow([donnees]) 
            i+=1
            print(i)
            if(i %25 ==0 ) :
    
                print(f"Il y a {i} valeurs ")
    
            #print(s[1])
        except web._utils.RemoteDataError :
            #print('Unable to read data from symbol {0}'.format(s[1]))
            errorList.append(s)
            Symboles.remove(s)
        except Exception as e:
            #print('Unable to read data from date {0}'.format('1/1?2021'))
            errorList.append(s)
            Symboles.remove(s)
    nFinal = len(Symboles)
    print(f"Taille final des données: {nFinal} ({nInit/nFinal })")

    

