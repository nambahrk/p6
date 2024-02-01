import numpy as np
import matplotlib.pyplot as plt
from scipy import stats #chi2 calculation

# sample data
x = np.array([100, 200, 300, 400, 1000, 2000])
y = np.array([168.15, 321.85, 484.20, 646.82, 1623.11, 3049.19])

p = np.polyfit(x, y, 1) #polynomial fit (1d), Get a tuple containing coefficients

f = np.poly1d(p) #make polynomial

e = [p[0] * xi + p[1] for xi in x] # model value

data = stats.chisquare(y,e) #chi2 statistics

chi2 = float(data[0]) #chi2
ndf = len(x) - 2 #Number of Degrees of Freedom
chi2pndf = float("{:.6f}".format(chi2/ndf)) #chi2/ndf

#display up to three decimal places
a = float("{:.3f}".format(p[0]))
b = float("{:.3f}".format(p[1]))

plt.title("PulseVolt - ADC")
plt.xlabel("Pulse Volt(mV)")
plt.ylabel("ADC(ch)")
plt.grid(True)
plt.scatter(x, y, color = "b", label="data")
plt.plot(x, f(x), color = "r", label=rf'$y={{{a}}}x +{{{b}}}$  ,   $χ²/ndf={{{chi2pndf}}}$')
plt.legend(loc='lower right')

#Runtime Configuration Parameters
plt.rcParams["font.size"] = 14         

bbox_dict = dict(edgecolor="#ff0000",fill=False)
plt.savefig("calibration.png")
plt.show()
