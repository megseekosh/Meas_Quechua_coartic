#!/usr/bin/env python
# -*- coding: utf-8 -*- #  

'''
# calculate spectral-envelope variability
# via 12 cepstrum coefficients
# à la Lee, Potamianos, & Narayanan (1999)
# walk directory of wav files and corresponding textgrids, option to specify single wav file 
# file output = filename.mfcc.csv
# Author: Meg Cychosz 2018, 
# with assistance from Geoff Bacon 
# also includes pieces hobbled together from various scripts 
# of Ronald Sprouse & Keith Johnson
# UC Berkeley
'''

import os, sys, fnmatch
import subprocess
import audiolabel
import librosa
import re
import pandas as pd
from collections import OrderedDict

# Regex to identify segments
segments = re.compile("a|i|u",re.IGNORECASE)

def processwav(wav, tg): # wav = path to the wav file in dir

	f, sr = librosa.load(wav, sr=44100) # load in file and the sampling rate you want
    
    #option to apply pre-emphasis 
    #emp_f = np.append(f[0], f[1:] - 0.97 * f[:-1])

	pm = audiolabel.LabelManager(from_file=os.path.join(dirpath,tg),from_type="praat") # open text grid 

	phonelist = []
	vectorlist = []
	followinglist = []
	prevlist = []
	wordlist = []
	t1list = []
	t2list = []
	durlist = []

    # loop through all of the labels on the "phone" tier that match the specified segments
	for v in pm.tier('phone').search(segments):
		word = pm.tier('word').label_at(v.center)
		previous = (pm.tier('phone').prev(v)).text
		following = (pm.tier('phone').next(v)).text

        # get spectrum
		s_lice = librosa.core.stft(librosa.resample(f, 44100, 44100, win_length=0.20)) # regardless of segment length,  same # of spectra sampled (n=168)
		mfcc = librosa.feature.mfcc(S=s_lice, n_mfcc=12) # each matrix has 12 rows, should have as many columns as the spectral slice does
		print(mfcc.shape)
		
		# for each spectrum matrix, get average MFCC vector
		vector = mfcc.mean(axis=1) # axis specifies to average over time (option to avg over MFCCs instead)
		phonelist.append(v.text), vectorlist.append(vector), followinglist.append(following), 
		prevlist.append(previous), wordlist.append(word.text), t1list.append(v.t1), t2list.append(v.t2), 
		durlist.append(v.t2-v.t1)

		# option to include a variability computation here
		# for ex. Euclidean distance between
		# two, or iteratively over multiple, vectors, 
		# but it depends on structure of the data

	df = pd.DataFrame( OrderedDict( (('Phone', pd.Series(phonelist)), ('Previous',  pd.Series(prevlist)), ('Following',  pd.Series(followinglist)), 
	('Word',  pd.Series(wordlist)), ('t1',  pd.Series(t1list)), ('t2',  pd.Series(t2list)), 
	('Duration',  pd.Series(durlist)), ('MFCC_vector',  pd.Series(vectorlist))) ) )

	df.to_csv(os.path.splitext(soundfile)[0]+'.mfcc.csv', encoding='utf-8') 





# Input wavfile 
filelist = [] # a tuple of wav & tg
if sys.argv[1] == 'walk': # if walk is specified in command line, walk over directory
  for dirpath, dirs, files in os.walk('.'): # walk over current directory
      for soundfile in fnmatch.filter(files, '*.wav'):
          #soundpath = os.path.join(dirpath, soundfile)
          filename = os.path.splitext(soundfile)[0]
          tg = filename+'.TextGrid'  # get the accompanying textgrid
          thing_to_add = (soundfile, tg)
          filelist.append(thing_to_add)
else: # option to run single wav file
  soundfile = sys.argv[1] 
  tg = os.path.splitext(soundfile)[0]+'.TextGrid'  # get the accompanying textgrid
  thing_to_add = (soundfile, tg)
  filelist.append(thing_to_add)
  dirpath = '.'


for wav, tg in filelist: 
      print(wav) # sanity check
      processwav(wav, tg)