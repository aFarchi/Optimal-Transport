#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

######################
# extractFinalState.py
######################

import numpy   as np
import cPickle as pck

from extractConfig import extractConfig
from files         import fileFinalState
#from files import fileConfig

from ..interpolate.interpolate import interpolateTimeFinalStateMultiSim

def reverseTime(f):
    shape = f.shape
    dim   = len(shape)

    fReversed = np.zeros(shape=shape)

    if dim == 0:
        return f

    elif dim == 1:
        for t in xrange(shape[0]):
            fReversed[t] = f[shape[0]-1-t]
        return fReversed

    elif dim == 2:
        for t in xrange(shape[1]):
            fReversed[:,t] = f[:,shape[1]-1-t]
        return fReversed

    elif dim == 3:
        for t in xrange(shape[2]):
            fReversed[:,:,t] = f[:,:,shape[2]-1-t]
        return fReversed

    return f

def extractFinalState(outputDir):

    f              = open(fileFinalState(outputDir), 'rb')
    p              = pck.Unpickler(f)
    finalState     = p.load().convergingStaggeredField()
    f.close()

    config         = extractConfig(outputDir)
 
    if config.swappedInitFinal:
        finit  = config.boundaries.temporalBoundaries.bt1
        ffinal = config.boundaries.temporalBoundaries.bt0
        f      = reverseTime(finalState.f)
    else:
        finit  = config.boundaries.temporalBoundaries.bt0
        ffinal = config.boundaries.temporalBoundaries.bt1
        f      = finalState.f

    mini   = np.min( [ finit.min() , ffinal.min() , f.min() ] )
    maxi   = np.max( [ finit.max() , ffinal.max() , f.max() ] )

    return (f, finit, ffinal, mini, maxi, config.P)

def extractFinalStateMultiSim(outputDirList):

    fs           = []
    finits       = []
    ffinals      = []
    Plist        = []

    minis        = []
    maxis        = []

    for outputDir in outputDirList:
        (f, finit, ffinal, mini, maxi, P) = extractFinalState(outputDir)
        
        fs.append(f)
        finits.append(finit)
        ffinals.append(ffinal)

        minis.append(f.min())
        minis.append(finit.min())
        minis.append(ffinal.min())

        maxis.append(f.max())
        maxis.append(finit.max())
        maxis.append(ffinal.max())

        Plist.append(P)

    Pmax = np.max(Plist)
    mini = np.min(minis)
    maxi = np.max(maxis)

    fs   = interpolateTimeFinalStateMultiSim(fs, Pmax, copy=False)

    return (fs, finits, ffinals, mini, maxi, Pmax)

