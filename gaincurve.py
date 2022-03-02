import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import norm


#時間幅
time=2*10**(-8)

#PMT波形の見えている部分
mint=200
maxt=350

#chargeのfitのmean
fitcharge=[]

#chargeの95%
deltacharge=[]

#1200V～2400Vまで
for k in range(1200,2500,100):
    charge=[]
    #1桁データ目
    for j in range(1,10):
        code= './' + str(k) + 'v/Sample_0000' + str(j) + '.csv'

        df = pd.read_csv(code, skiprows=26)
        df2=df['Ch1 V']
        data = df2.tolist()

        v=0
        for i in range(mint,maxt):
            if data[i]>0:
                v=v+data[i]
            else:
                pass

        q=int(v*time*(0.02)*10**(12))
        charge.append(q)

    #2桁データ目
    for j in range(10,100):
        code= './' + str(k) + 'v/Sample_000' + str(j) + '.csv'

        df = pd.read_csv(code, skiprows=26)
        df2=df['Ch1 V']
        data = df2.tolist()

        v=0
        for i in range(mint,maxt):
            if data[i]>0:
                v=v+data[i]
            else:
                pass

        q=int(v*time*(0.02)*10**(12))
        charge.append(q)

    #3桁データ目
    for j in range(100,500):
        code= './' + str(k) + 'v/Sample_00' + str(j) + '.csv'

        df = pd.read_csv(code, skiprows=26)
        df2=df['Ch1 V']
        data = df2.tolist()

        v=0
        for i in range(mint,maxt):
            if data[i]>0:
                v=v+data[i]
            else:
                pass

        q=int(v*time*(0.02)*10**(12))
        charge.append(q)

    mean=sum(charge)/len(charge)

    # gaussian function
    def gaussian_func(x, A, mu, sigma):
        return A * np.exp( - (x - mu)**2 / (2 * sigma**2))

    #初期変数(height,中心,σ)
    parameter_initial = np.array([30, mean, 30])

    #yの配列用意
    y = []

    #最小値と最大値を簡易変数化、整数化
    mins=int(min(charge))
    maxs=int(max(charge))

    #あるchに何粒子入ってきたかをyとしてカウント
    for i in range(mins,maxs):
        s=charge.count(i)
        y.append(s)

    #ch数を横軸に取る
    x=list(range(mins, maxs, 1))

    #ch数(x),データ数(y)
    x = np.array(x)
    y = np.array(y)

    #fittingして、パラメーターと共分散を出力
    popt, pcov = curve_fit(gaussian_func, x, y, p0=parameter_initial)

    popt = popt.tolist()

    #小数点丸めこみ
    #height
    popt[0]=float("{:.3f}".format(popt[0]))
    #mean
    popt[1]=float("{:.3f}".format(popt[1]))
    #sigma
    popt[2]=float("{:.3f}".format(popt[2]))

    #標準偏差誤差
    StdE = np.sqrt(np.diag(pcov))

    #95%信頼区間(標準正規分布の1.96の幅でもいいけど今回はこれでやる。)
    alpha=0.025
    #ppfは累積分布関数が指定した値を取る，変数を返す。
    delta = norm.ppf(q=alpha)*StdE

    #95%距離
    delta[1]=float("{:.3f}".format(delta[1]))

    fitcharge.append(popt[1])
    deltacharge.append(delta[1])

# サンプルデータ
x = np.array([1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400])
y = np.array(fitcharge)

y_err = np.log10(np.array(deltacharge))

#初期変数
parameter_initial = np.array([2, 9])

# function
def func(x, a, b):
    return a * x + b

popt2, pcov2 = curve_fit(func, x, np.log10(y), p0=parameter_initial)
popt2 = popt2.tolist()

#小数点丸めこみ
a=float("{:.3f}".format(popt2[0]))
b=float("{:.3f}".format(popt2[1]))

estimated_curve = func(x, popt2[0], popt2[1])

# 散布図と近似直線を描く
plt.title("GainCurve")
plt.xlabel("HV[V]")
plt.ylabel("log10 charge[mI ns]")
plt.grid(True)
plt.scatter(x, np.log10(y), color = "b", label="data")
plt.plot(x, estimated_curve, color = "r", label=rf'$y={{{a}}}x +{{{b}}}$')
plt.errorbar(x, np.log10(y), yerr = y_err, capsize=5, fmt='o', markersize=1, ecolor='black', markeredgecolor = "black", color='w')

#数式追加
plt.legend(loc='lower right')
plt.rcParams["font.family"] = "Meiryo"   # 使用するフォント
plt.rcParams["font.size"] = 14           # 文字の大きさ
bbox_dict = dict(edgecolor="#ff0000",fill=False)

#保存と表示
plt.savefig("gaincurve.png")
plt.show()
