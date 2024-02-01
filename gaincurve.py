import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import norm

time=2*10**(-8) #delta t

mint=200 #min pulse range
maxt=350 #max pulse range

#chargeのfitのmean
fitcharge=[]

#chargeの95%
deltacharge=[]

#loop Volt
for k in range(1200, 2500, 100): 
    charge=[]

    #the first digit
    for j in range(1,10): 
        code= './' + str(k) + 'v/Sample_0000' + str(j) + '.csv'

        df   = pd.read_csv(code, skiprows=26)
        df2  = df['Ch1 V']
        data = df2.tolist()

        v=0
        for i in range(mint,maxt):
            if data[i]>0:
                v=v+data[i]
            else:
                pass

        q=int(v*time*(0.02)*10**(12))
        charge.append(q)

    #the second digit
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

    #the third digit
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

    parameter_initial = np.array([30, mean, 30]) #initial value

    y = []
    mins=int(min(charge))
    maxs=int(max(charge))

    #count number of particles into the channel
    for i in range(mins,maxs):
        s=charge.count(i)
        y.append(s)

    x=list(range(mins, maxs, 1))

    #channel number(x), data number(y)
    x = np.array(x)
    y = np.array(y)

    #fitting
    popt, pcov = curve_fit(gaussian_func, x, y, p0=parameter_initial)
    popt = popt.tolist()
    popt[0]=float("{:.3f}".format(popt[0])) #height
    popt[1]=float("{:.3f}".format(popt[1])) #mean
    popt[2]=float("{:.3f}".format(popt[2])) #sigma

    StdE = np.sqrt(np.diag(pcov)) #standard deviation

    alpha=0.025 #95% confidence level
    delta = norm.ppf(q=alpha)*StdE
    delta[1]=float("{:.3f}".format(delta[1]))
    fitcharge.append(popt[1])
    deltacharge.append(delta[1])

# sample data
x = np.linspace(1200, 2400, 13)
y = np.array(fitcharge)

y_err = np.log10(np.array(deltacharge))

parameter_initial = np.array([2, 9])

def func(x, a, b):
    return a * x + b

popt2, pcov2 = curve_fit(func, x, np.log10(y), p0=parameter_initial)
popt2 = popt2.tolist()

a=float("{:.3f}".format(popt2[0]))
b=float("{:.3f}".format(popt2[1]))

estimated_curve = func(x, popt2[0], popt2[1])

plt.title("GainCurve")
plt.xlabel("HV[V]")
plt.ylabel("log10 charge[mI ns]")
plt.grid(True)
plt.scatter(x, np.log10(y), color = "b", label="data")
plt.plot(x, estimated_curve, color = "r", label=rf'$y={{{a}}}x +{{{b}}}$')
plt.errorbar(x, np.log10(y), yerr = y_err, capsize=5, fmt='o', markersize=1, ecolor='black', markeredgecolor = "black", color='w')
plt.legend(loc='lower right')
plt.rcParams["font.size"] = 14         
bbox_dict = dict(edgecolor="#ff0000",fill=False)

plt.savefig("gaincurve.png")
plt.show()
