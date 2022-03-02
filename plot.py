#pandasでcsvデータを取得、csvモジュールでもできる
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

charge=[]

#ch数の変更
#codeの読み込み位置の変更(コピペで対応する？)

#時間幅
time=2*10**(-8)

#PMT波形の見えている部分
mint=200
maxt=350

#1桁データ目
for j in range(1,10):
    code= 'Sample_0000' + str(j) + '.csv'

    df = pd.read_csv(code, skiprows=26)
    df2 = df['Ch1 V']
    data=df2.tolist()

    v=0
    for i in range(mint,maxt):
        if data[i]>0:
            v=v+data[i]
        else:
            pass

    q=int(v*time*(0.02)*10**(11))
    charge.append(q)

#2桁データ目
for j in range(10,100):
    code= 'Sample_000' + str(j) + '.csv'

    df = pd.read_csv(code, skiprows=26)
    df2 = df['Ch1 V']
    data=df2.tolist()

    v=0
    for i in range(mint,maxt):
        if data[i]>0:
            v=v+data[i]
        else:
            pass

    q=int(v*time*(0.02)*10**(11))
    charge.append(q)

#3桁データ目
for j in range(100,1000):
    code= 'Sample_00' + str(j) + '.csv'

    df = pd.read_csv(code, skiprows=26)
    df2 = df['Ch1 V']
    data=df2.tolist()

    v=0
    for i in range(mint,maxt):
        if data[i]>0:
            v=v+data[i]
        else:
            pass

    q=int(v*time*(0.02)*10**(11))
    charge.append(q)

#4桁データ目
for j in range(1000,5000):
    code= 'Sample_0' + str(j) + '.csv'

    df = pd.read_csv(code, skiprows=26)
    df2 = df['Ch1 V']
    data=df2.tolist()

    v=0
    for i in range(mint,maxt):
        if data[i]>0:
            v=v+data[i]
        else:
            pass

    q=int(v*time*(0.02)*10**(11))
    charge.append(q)

#yの配列用意
y = []

#グラフでのchargeの最大と最小設定
min=int(min(charge))
max=int(max(charge))

#あるcharge値のデータ数をそれぞれカウントしていく
for i in range(min,max):
    s=charge.count(i)
    y.append(s)

#charge
x = np.array(list(range(min, max, 1)))

#データ数
y = np.array(y)

#plot
plt.bar(x,y,color='w',edgecolor='b')
plt.xlim(0,300)
plt.grid()
plt.yscale('log')
plt.title("1 p.e.")
plt.xlabel("charge(10^-11)")
plt.ylabel("Events")

#画像保存
plt.savefig("plot.png")

#グラフ表示
plt.show()
