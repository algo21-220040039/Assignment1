import numpy as np
import pandas as pd
import pandas_datareader.data as web

class ERC:
    def __init__(self, covar):
        self.covar = covar # covariance matrix
        self.weights = 0
        self.ctr = 0 # contribution to risk
        self.tErr = 0 # total deviation of weights compared to ERC weights
        self.iternum = 0 # number of iterations

    def solve(self, precision, seed):
        w = seed.copy() # initial guess of weights
        iternum = 0
        n = len(w) # number of stocks
        grad = np.zeros(3) # derivatives of CtR

        while True:
            print(self.covar)
            iternum += 1
            print('iternum: ', iternum)
            risk = (w.T.dot(self.covar).dot(w))**0.5
            print('risk', risk)
            ctr = np.array([w[i]*(self.covar.dot(w)[i])/risk**2 for i in range(n)])
            print('ctr', ctr)
            err =  1/n-ctr
            tErr = ((err**2).sum()/n)**0.5
            mErr = np.max(abs(err)) # minimum error
            iErr = int(np.argmax(abs(err))) # location where minimum error occurs
            print('iErr:', iErr)

            # exit condition
            if tErr < 10**-precision or iternum > 10**precision : break

            # calculating the gradient of CtR
            grad[0] = -mErr
            corr = self.getSign(w[iErr])*(self.covar[iErr].dot(w))/(self.covar[iErr][iErr]**0.5)/risk
            grad[1] = w[iErr]*self.covar[iErr][iErr]*(1-2*corr**2)/risk**2 + self.covar[iErr][iErr]**0.5*corr/risk
            grad[2] = self.covar[iErr][iErr]*(1-2*corr**2)/risk**2 - corr*w[iErr]*self.covar[iErr][iErr]**1.5*(2-3*corr**2)/risk**3
            print('grad',grad)
            # calculating the step size
            if grad[2] != 0:
                delta = abs((grad[1]**2-4*grad[2]*grad[0]))**0.5
                if grad[1] >= 0:
                    step = (-grad[1]+delta)/2/grad[2]
                else:
                    step = (-grad[1]-delta)/2/grad[2]
            else:
                step = -grad[0]/grad[1]
            print('step', step)
            # adjust the step
            w[iErr] += step
            print('w', w)

    # generating an initial guess of weights, based on OLS estimation
    def getSeed(self, col):
        a = self.covar.copy()
        a = np.delete(a, col, axis=0)
        a = np.delete(a, col, axis=1)
        a = np.linalg.inv(a)
        b = self.covar[:,col]
        b = np.delete(b, col, axis=0)
        c = a.dot(b)
        c = np.insert(c, col, -1, axis=0)
        return -c

    def getSign(self,x):
        if x == 0:  return 0
        if x < 0: return -1
        if x > 0: return 1

def main():
    # get historical data of four stocks
    all_data = {ticker: web.get_data_yahoo(ticker)
                for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']}
    price = pd.DataFrame({ticker: data['Adj Close']
                          for ticker, data in all_data.items()})
    priceDiff = price.diff()
    covar = np.array(priceDiff.corr())
    precision = 5

    erc = ERC(covar)

    for i in range(covar.shape[0]):
        seed = erc.getSeed(i)
        print(seed)
        erc.solve(precision, seed)
        print(erc.weights)

if __name__=='__main__': main()
