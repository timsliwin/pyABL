#
#Library to calculate mean profiles of various ABL parameters
#

import numpy as np

#---------------------------------------------------

def MeanVerticalProfile(var):

    (nT,nZ,nX,nY) = var.shape

    prof = np.zeros((nT,nZ),dtype=np.float64)

    for t in range(nT):
	for z in range(nZ):
             prof[t,z] = np.mean(var[t,z,:,:])
		    
    return prof

#---------------------------------------------------

def MeanVarianceProfile(var):

    (nT,nZ,nX,nY) = var.shape

    prof = np.zeros((nT,nZ),dtype=np.float64)

    for t in range(nT):
        for z in range(nZ):
            prof[t,z] = np.var(var[t,z,:,:])

    return prof

#---------------------------------------------------

def PerturbationFromVerticalMean(var, varmean):

    (nT,nZ,nX,nY) = var.shape

    pert = np.zeros((nT,nZ,nX,nY),dtype=np.float64)

    for t in range(nT):
        for z in range(nZ):
            pert[t,z,:,:] = var[t,z,:,:]-varmean[t,z]    
    
    return pert

#---------------------------------------------------

def wrf_MeanVVvarProf(wpert):

    (nT,nZ,nX,nY) = wpert.shape

    prof  = np.zeros((nT,nZ),dtype=np.float64)

    for t in range(nT):
        for z in range(nZ):
            prof[t,z] = np.mean(wpert[t,z,:,:]*wpert[t,z,:,:])

    return prof

#---------------------------------------------------

def wrf_MeanVVskewnessProf(wpert):

    (nT,nZ,nX,nY) = wpert.shape

    prof  = np.zeros((nT,nZ),dtype=np.float64)

    for t in range(nT):
        for z in range(nZ):
            prof[t,z] = np.mean(wpert[t,z,:,:]*wpert[t,z,:,:]*wpert[t,z,:,:])

    return prof

#---------------------------------------------------

if __name__ == "__main__":

    W = np.arange(0,4000,dtype=np.float64)
    W = W.reshape((2,5,20,20))

    print W.shape
    print W

    wMeanProf = wrf_MeanVVprof(W)

    print wMeanProf.shape
    print wMeanProf

    wPert     = wrf_PertFromVerticalMean(W,wMeanProf)

    print wPert.shape
    print wPert

    wVariance = wrf_MeanVVvarProf(wPert)

    print wVariance.shape
    print wVariance

    wSkewness = wrf_MeanVVskewnessProf(wPert)

    print wSkewness.shape
    print wSkewness
   
