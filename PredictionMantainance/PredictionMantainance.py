from nptdms import TdmsFile
import os
import numpy as np
from sklearn import linear_model
from scipy import signal
import pickle
from datetime import datetime

path = 'data/ALL'
resFiles = []
resFFTSpectrum = []
resPeakSpectrum = []
resMean = []
resStdDeviation = []
resSlope = []
results = []

def readFiles():
    files=os.listdir(path)
    files.sort()
    
    for filename in files:
        if filename.endswith(".tdms"):
            #print(filename)
            tdms_file = TdmsFile(path+"/"+filename)
            channel = tdms_file.object("Untitled", "Canale 4")
            data = channel.data
            fftSpectrum, peakSpectrum, mean, stdDeviation, slope = evaluateFeature(data)
            resFiles.append(cleanFilename(filename))
            resFFTSpectrum.append(fftSpectrum)
            resPeakSpectrum.append(peakSpectrum)
            resMean.append(mean)
            resStdDeviation.append(stdDeviation)
            resSlope.append(slope)
            #mean, mean1 = avg(data)
            #print("Filename - " + filename + " Mean: " + str(mean))
    saveResults(resFiles, "featureObtained/Date.p")
    saveResults(resFFTSpectrum, "featureObtained/FFTSpectrum.p")
    saveResults(resPeakSpectrum, "featureObtained/PeakSpectrum.p")
    saveResults(resMean, "featureObtained/Mean.p")
    saveResults(resStdDeviation, "featureObtained/StdDeviation.p")
    saveResults(resSlope, "featureObtained/Slope.p")
            #print(data)
            
def evaluateFeature(data):
    """This evaluate some feature of some data

    @param data:([float]) array of float representing the input data.
    
    @return: FFT spectrum
    @return: Spectrum Peak
    -----@return: Plateau level IN FUTURE
    @return: Mean
    @return: Standard deviation
    @return: Slopes(m of Y=mx+q)
    """
    
    dataN=np.array(data)
    
    freqs, bins,Pxx =signal.spectrogram(dataN, return_onesided=True,  nperseg=10000)
    
    fftSpectrum=Pxx
    peakSpectrum=Pxx.max()
    
    mean=dataN.mean()
    
    stdDeviation=dataN.std()
    
    regr = linear_model.LinearRegression()
    X=np.array(list(range(0, len(data)))).transpose()
    regr.fit(X[:,np.newaxis], dataN[:,np.newaxis])        
    slope=regr.coef_[0][0]
    
    return fftSpectrum, peakSpectrum, mean, stdDeviation, slope

def cleanFilename(name):
    #GIORNO10-I4,0_20170915@162230.tdms
    names = name.split("_")
    names2 = names[len(names)-1].split(".")
    if(names2[0]==''):
        print("error")
    return datetime.strptime(names2[0], "%Y%m%d@%H%M%S") 

def saveResults(values, name):
    results.append(values)
    pickle.dump( results, open( name, "wb" ) )
    results.clear()

readFiles()

