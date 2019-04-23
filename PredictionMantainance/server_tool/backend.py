import os
from flask import Flask, request, redirect, url_for, jsonify
import requests
import pandas as pd
import json
import itertools
import flask
import smtplib
import numpy as np

from nptdms import TdmsFile
import os
import numpy as np
from sklearn import linear_model
from scipy import signal
import pickle

from flask_cors import CORS

path = '../../PredictionMantainance/data/ALL'
resFiles = []
resFFTSpectrum = []
resPeakSpectrum = []
resMean = []
resStdDeviation = []
resSlope = []
results = []

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def readFiles():
    found=False
    try:
        with open("last_file", "rb") as fp:   # Unpickling
            last_file = pickle.load(fp)
            print(last_file)
    except:
        print("No file found")
        found=True
        
    files=os.listdir(path)
    files.sort()
    for filename in files:
        if filename.endswith(".tdms") and found:
            tdms_file = TdmsFile(path+"/"+filename)
            channel = tdms_file.object("Untitled", "Canale 4")
            data = channel.data 
            pickle.dump( filename, open( "last_file", "wb" ) )
            fftSpectrum, peakSpectrum, mean, stdDeviation, slope= evaluateFeature(data)
            return filename, fftSpectrum, peakSpectrum, mean, stdDeviation, slope
        if(last_file==filename):
            found=True
    return 0,0,0,0,0

            
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
    names2 = names[1].split(".")
    return names2[0]

def saveResults(values, name):
    results.append(values)
    pickle.dump( results, open( name, "wb" ) )
    results.clear()
    



@app.route('/')
@app.route('/home')                       
def getData():

    filename, fftSpectrum, peakSpectrum, mean, stdDeviation, slope=readFiles()
    '''filename="aaa"
    peakSpectrum=34.9
    mean=10.3
    stdDeviation=17.8
    slope=3.7'''
    """return jsonify(
        dateTime=cleanFilename(filename),
        ok=str(mean<2 and mean>-4),
        mean=mean,
        standardDeviation=stdDeviation,
        Slope=slope,
        PeakFrequency=peakSpectrum
    )"""
    data_out=dict()
    data_out["dateTime"]=cleanFilename(filename)
    data_out["ok"]=str(mean<2 and mean>-4)
    data_out["mean"]=mean
    data_out["standardDeviation"]=stdDeviation
    data_out["slope"]=slope
    data_out["peakFrequency"]=peakSpectrum
    
    output = json.dumps(data_out)

    return output


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
