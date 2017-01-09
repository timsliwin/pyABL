from mpi4py import MPI
import numpy as np
import sys
import warnings

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#------------------------------------------------------------------------------

def iprint(astring):

    stringtemplate = "Process %d of %d : %s\n"
    sys.stdout.write(stringtemplate % (rank,size,astring))

#------------------------------------------------------------------------------

def calcfactors(n):

    pairs = [[i,n/i] for i in range(1, int(n**0.5)+1) if n % 1 == 0]

    factors = []

    for f in pairs:
        if f[0]*f[1] == n: factors.append(f)

    return factors

#------------------------------------------------------------------------------

def gridProcessors(numProcs,dim1,dim2,ignorePrimes=False):

    if dim1==1:
	ps1=1
        ps2=numProcs
    elif dim2==1:
        ps1=numProcs
        ps2=1
    else:
        factors = calcfactors(numProcs)
        ps1,ps2 = factors[-1]

        # check for prime number of processors....
        if len(factors)<2 and numProcs>2 and ignorePrimes==False:
            errtext = "Number of processes is a prime number. "           \
                      "Distribution of data will be limited to a single " \
                      "choice and either fail or perform inefficiently. " \
                      "Consider running with a non-prime number or "      \
                      "silencing this error with \"ignorePrimes=True\" "  \
                      "in the gridProcessors() function call."

            raise RuntimeError(errtext)

                    
        # check if default selected factors will work for data sizes specified.
        if ps1>dim1 or ps2>dim2:
            factlen = len(factors)
            iter    = 1

            while (ps1>dim1 or ps2>dim2) and iter<factlen:
                ps1,ps2 = factors[factlen-1-iter]
                iter += 1

            # if none of the factors proves successful for decomposition, 
            # then raise error as data size is too small or the number 
            # of processors is too big.
            if ps1>dim1 or ps2>dim2:

                errtext = "User is attempting to decompose data with "      \
                          "dimensions ("+str(dim1)+","+str(dim2)+") among " \
                          "many processors ("+str(numProcs)+"). There is "  \
                          "too little data per processor to distribute "    \
                          "data effectively. Either decrease the number "   \
                          "of processors, or increase the dimensions of "   \
                          "the data."

                raise RuntimeError(errtext) 
             
    return ps1,ps2

#------------------------------------------------------------------------------

def gridIndicies(pDim1,pDim2,dim1idxs,dim2idxs):

    dim1list = []
    dim2list = []

    for i in range(0,pDim1):
        for j in range(0,pDim2):
            dim1list.append(dim1idxs[i].tolist())
            dim2list.append(dim2idxs[j].tolist())

    return dim1list,dim2list

#------------------------------------------------------------------------------

def pointsPerGridbox(dimLength, dimProcs):

    pointNums = np.ones((dimProcs,),dtype=np.uint16)

    pts,rem = divmod(dimLength,dimProcs)

    pointNums *= pts

    if rem != 0:
        for i,num in enumerate(pointNums):
	    if rem > 0:
                pointNums[i] = num+1
                rem -= 1
            else:
                continue

    return pointNums

#------------------------------------------------------------------------------

def gridboxIndicies(dimLength, dimProcs):

    pointsPerBox = pointsPerGridbox(dimLength, dimProcs)

    idxs = np.zeros([dimProcs,2],dtype=np.int)

    for i,ppb in enumerate(pointsPerBox):
        idxs[i][1] = idxs[i][0] + ppb
	if i<dimProcs-1: idxs[i+1][0] = idxs[i][1]

    return idxs
    
#------------------------------------------------------------------------------
#
#def divideAndConquer1D(numSlices,numNodes):
#
#    remainder = 0
#    idxs = np.zeros([numNodes,2],dtype=np.int)
#
#    while (numSlices%numNodes != 0):
#	numSlices=numSlices-1
#	remainder=remainder+1
#
#    unitsPerNode = numSlices/numNodes
#
#    for n in range(numNodes):
#	if n==0:
#		idxs[n][0] = 0
#	else:
#		idxs[n][0] = idxs[n-1][1]
#	idxs[n][1] = idxs[n][0]+unitsPerNode
#
#	if remainder>0:
#	    idxs[n][1]=idxs[n][1]+1
#	    remainder=remainder-1
#
#    return idxs
#
#------------------------------------------------------------------------------

if __name__ == "__main__":

    if (rank==0):

#        print calcfactors(24)
#        stop

        numprocs = 12
        dim1     = 2
        dim2     = 200

        ps1,ps2 = gridProcessors(numprocs,dim1,dim2,ignorePrimes=False)

        print ps1,ps2

        ps1_ppgb = pointsPerGridbox(dim1,ps1)
        ps1_idxs = gridboxIndicies(dim1,ps1)

        ps2_ppgb = pointsPerGridbox(dim2,ps2)
        ps2_idxs = gridboxIndicies(dim2,ps2)

        print ps1_ppgb
        print ps1_idxs

        print ps2_ppgb
        print ps2_idxs

        dim1,dim2 = gridIndicies(ps1,ps2,ps1_idxs,ps2_idxs)

        print dim1
        print dim2
