import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#時間幅
time=1*10**(-9)

#AMP
amp=20

#1charge(電気素量だが、gainがあるため対応するものは大きくなっている)
q=10**(7)*amp*1.6*10**(-19)

87,96,176,291,826

list=['Sample_00087.csv','Sample_00096.csv','Sample_00176.csv','Sample_00291.csv','Sample_00826.csv']


for j in list:
    #読み込み
    df = pd.read_csv(j, skiprows=26)
    df1 = df['Ch1 V']-df['Ch1 V'][0]
    df2 = df['Ch2 V']-df['Ch2 V'][0]
    df3 = df['Ch3 V']-df['Ch3 V'][0]

    data1=df1.tolist()
    data2=df2.tolist()
    data3=df3.tolist()

    #1つ目
    v1=0
    for i in range(0,500):
        if data1[i]>0:
            v1=v1+data1[i]
        else:
            pass

    #charge
    q1=v1*time*(0.02)

    #2つ目
    v2=0
    for i in range(0,500):
        if data2[i]>0:
            v2=v2+data2[i]
        else:
            pass

    #charge
    q2=v2*time*(0.02)

    #3つ目
    v3=0
    for i in range(0,500):
        if data3[i]>0:
            v3=v3+data3[i]
        else:
            pass

        #charge
        q3=v3*time*(0.02)

    #count数
    print(int(q1/q),int(q2/q),int(q3/q))
