import numpy as np
import matplotlib.pyplot as plt


#PHADCでのch数とPulseVoltの値の関係性


#カイ二乗計算
from scipy import stats

# サンプルデータ
x = np.array([100, 200, 300, 400,1000,2000])
y = np.array([168.15, 321.85,484.20 , 646.82, 1623.11, 3049.19])

#back=205

# 近似直線の式の係数が入ったタプルを得る。今回は1次の近似。
p = np.polyfit(x, y, 1)

# 一次関数の式のオブジェクトを生成する。1dとは独立変数の数が１つということ。
f = np.poly1d(p)

#小数点丸めこみ
a=float("{:.3f}".format(p[0]))
b=float("{:.3f}".format(p[1]))


#モデル計算された数値例
e = [a*100+b,a*200+b,a*300+b,a*400+b,a*1000+b,a*2000+b]

#χ二乗、P値を出力。yは実測データ。
data = stats.chisquare(y,e)

#χ二乗のみ取り出す。
c=float(data[0])

#自由度
ndf=6

#χ^2/ndf値
chi=float("{:.6f}".format(c/ndf))


# 散布図と近似直線を描く
plt.title("PulseVolt - ADC")
plt.xlabel("Pulse Volt(mV)")
plt.ylabel("ADC(ch)")
plt.grid(True)
plt.scatter(x, y, color = "b", label="data")
plt.plot(x, f(x), color = "r", label=rf'$y={{{a}}}x +{{{b}}}$  ,   $χ²/ndf={{{chi}}}$')
plt.legend(loc='lower right')

plt.rcParams["font.family"] = "Meiryo"   # 使用するフォント
plt.rcParams["font.size"] = 14           # 文字の大きさ

bbox_dict = dict(edgecolor="#ff0000",fill=False)
#plt.text(150,1250, 'y = ' + str(a) + ' x '  + str(b)+ '\n \n' 'χ²/ndf='+str(chi),bbox=bbox_dict)
plt.savefig("calibration.png")
plt.show()
