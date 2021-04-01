import csv
import pandas_datareader as web
import yfinance as yf 
import sys
import multiprocessing as mp
nInit=0
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
def div_symbol_extract(t):
    """Nombre de processeurs 8"""
    d = len(t)
    m = int(d/8)
    #print("TAILLE ",m)
    a,b,c,d,e,f,g,h = t[:m],t[  m:2*m], t[2*m:3*m], t[3*m:4*m], t[4*m:5*m], t[5*m:6*m], t[6*m:7*m], t[7*m:]
    return a, b,c,d,e,f,g,h 
def finalSymbol(tab):
    with open('savedSymbols.csv','w', newline='') as nfile:
        writer = csv.writer(nfile)
        for t in tab:
            writer.writerow([t])



def get_data(table, nbT):
    nTable = table
    namefile= 'dataset'+str(nbT) + '.csv'
    i = 0
    with open (namefile,'w', newline = '') as nfile:
        writer = csv.writer(nfile)
        for s in table:
            try: 
                sf= yf.Ticker(s[1])
                donnees=''
                for name , d in sf.info.items():
                    #if name == 'logo_url' : donnees+=str(d)
                    donnees+= str(d)+'; '

                if donnees!='':
                    donnees = donnees.replace('\n',' ')
                    writer.writerow([donnees])
                else:
                    nTable.remove(s)
                i+=1 
                if (i%100==0):
                    print(f'More: {i}')
                                     
            except web._utils.RemoteDataError :
                #print('Unable to read data from symbol {0}'.format(s[1]))
                nTable.remove(s)
            except Exception as e:
                #print('Unable to read data from date {0}'.format('1/1?2021'))
                nTable.remove(s)
    return (nTable, nbT )
#print(Symboles[1])
results = []
def collect(result):
    global results 
    results.append(result)
def main():
    
    Symboles= symbol_extract("symboles.csv")
    pool = mp.Pool(mp.cpu_count())    
    ## Dictionnaire de données (pas optimal, à changer)
    s1,s2,s3,s4,s5,s6,s7,s8 = div_symbol_extract(Symboles)

    #print(s2,s3,s1)
    Sj = [s1,s2,s3,s4,s5,s6,s7,s8]
    #print(s1) 
    #for k , st in enumerate( Sj ):A
    for k, st in enumerate(Sj):
        """Partie de parallélisation"""
        pool.apply_async(get_data, args=(st,k),callback= collect)
        #results.append(pool.apply(get_data, args= (st,k)))
        #results=[pool.apply(get_data, args=(st, k)) for k, st in enumerate (Sj)]
    pool.close()
    pool.join()
    print(" !!!!! END !!!!!!!")

    results.sort(key=lambda x: x[0])
    results_p = [i for i, r in results]
    listS =  [r for i, r in results]

    results_final=[]
    for k in listS:
        results_final.append(results_p[k])     
    #    with open ('dataset.csv','w', newline = '') as nfile:
                



    finalSymbol(results_final)
    


if __name__== "__main__":
    main()




















































