import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

#必要な変更点
#ch数、時間幅、PMTの見えている部分(mint,maxt)、データ数(5000or10000)
#整数化する累乗部分、xlabelの累乗、xの表示範囲
#fitting式の表示場所、fitting初期値




charge=[]

#時間幅
time=5*10**(-10)

#PMT波形の見えている部分
mint=0
maxt=40

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

    q=int(v*time*(0.02)*10**(14))
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

    q=int(v*time*(0.02)*10**(14))
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

    q=int(v*time*(0.02)*10**(14))
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

    q=int(v*time*(0.02)*10**(14))
    charge.append(q)

#yの配列用意
y = []

#グラフでのchargeの最大と最小設定
min=int(min(charge))
max=int(max(charge))

#あるcharge値のデータ数をそれぞれカウントしていく
for i in range(min,max):
    if charge.count(i) != 0:
        s=np.log10(charge.count(i))
        y.append(s)
    else:
        y.append(0)

#charge
x = np.array(list(range(min, max, 1)))

#データ数
y = np.array(y)

# gaussian function
def gaussian_func(x, A, mu, sigma, B, nu, sig):
    return A * np.exp( - (x - mu)**2 / (2 * sigma**2))+B * np.exp( - (x - nu)**2 / (2 * sig**2))

#初期変数(height,中心,σ)
parameter_initial = np.array([4, 50, 10, 2, 120, 20])


#fittingして、パラメーターと共分散を出力
popt, pcov = curve_fit(gaussian_func, x, y, p0=parameter_initial, maxfev=1000000)

popt = popt.tolist()

#小数点丸めこみ
popt[0]=float("{:.3f}".format(popt[0]))
popt[1]=float("{:.3f}".format(popt[1]))
popt[2]=float("{:.3f}".format(popt[2]))
popt[3]=float("{:.3f}".format(popt[3]))
popt[4]=float("{:.3f}".format(popt[4]))
popt[5]=float("{:.3f}".format(popt[5]))

#標準偏差誤差
StdE = np.sqrt(np.diag(pcov))

#95%信頼区間(標準正規分布の1.96の幅でもいいけど今回はこれでやる。)
alpha=0.025
#ppfは累積分布関数が指定した値を取る，変数を返す。
lwCI = popt + norm.ppf(q=alpha)*StdE
upCI = popt + norm.ppf(q=1-alpha)*StdE

#小数点丸めこみ
lwCI[1]=float("{:.3f}".format(lwCI[1]))
upCI[1]=float("{:.3f}".format(upCI[1]))
lwCI[4]=float("{:.3f}".format(lwCI[4]))
upCI[4]=float("{:.3f}".format(upCI[4]))

#fitting関数
estimated_curve = gaussian_func(x, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])


#plot
plt.bar(x, y ,color='w',edgecolor='b')
plt.title("1 p.e.")
plt.xlabel("charge(10^-14)")
plt.ylabel("Events")
plt.grid()
plt.xlim([-50,800])
plt.plot(x, estimated_curve, label="Estimated curve", color="r")
plt.legend()
plt.text(300,1.5, 'height:'+str(popt[0])+','+str(popt[3])+ '\n' 'mean:'+str(popt[1])+','+str(popt[4])+'\n' 'sigma:' +str(popt[2])+','+str(popt[5])+ '\n' '95%信頼区間' + str(lwCI[1]) + '≦x≦' + str(upCI[1])+ '\n' +str(lwCI[4]) + '≦x≦' + str(upCI[4]) , fontname="MS Gothic" )

#保存
plt.savefig("twofit.png")

#グラフ表示
plt.show()
