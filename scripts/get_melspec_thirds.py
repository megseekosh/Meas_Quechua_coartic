#!/usr/bin/env python
# -*- coding: utf-8 -*- #  

'''
# calculate spectral-envelope variability
# via mel spectral coefficients
# à la Lee, Potamianos, & Narayanan (1999)
# walk directory of wav files and corresponding textgrids, option to specify single wav file 
# file output = filename.mel_spectrum.csv
# calculates over three distinct timepts in each phone, instead of all averaged spectra
# Authors: Meg Cychosz & Keith Johnson 2018, 
# also includes pieces hobbled together from various scripts 
# of Ronald Sprouse 
# UC Berkeley
'''

import os, sys, fnmatch
import subprocess
import audiolabel
import librosa
import numpy as np
import re
import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
from sys import argv



# Regex to identify segments
segments = re.compile("ch|a|qh|p|k|t|r|m|w|kh|s",re.IGNORECASE)
words = re.compile("api-pi|chaki-pi|katari-pi|llama-pi|maki-pi|papa-pi|waka-pi|wasi-pi|wawa-pi|imilla-pi|juk'ucha-pi|sunkha-pi|t'ika-pi|uhut'a-pi|wallpa-pi|warmi-pi|wallpa|t'ika|sunkha|wawa|wasi|waka|papa|maki|llama|katari|chaki|api|qhari|qhari-pi|warmi|",re.IGNORECASE)

speakerlist = []
phonelist = []
int_1_list = []
int_2_list = []
int_3_list = []
followinglist = []
prevlist = []
wordlist = []
notelist = []
t1list = []
t2list = []
durlist = []
worddurlist = []
int_1_normlist = []
int_2_normlist = []
int_3_normlist = []
morphlist = []



def processwav(wav, tg): # wav = path to the wav file in dir

	f, sr = librosa.load(wav, sr=12000) # load in file and the sampling rate you want
	pm = audiolabel.LabelManager(from_file=os.path.join(dirpath,tg),from_type="praat") # open text grid 

	for word in pm.tier('Word').search(words): 

		t1_idx = np.floor((word.t1)*sr) # Convert time to integer index
		t2_idx = np.floor((word.t2)*sr)
		snippet = f[t1_idx:t2_idx]
		snippet_pm = pm.tier('Phone').tslice(word.t1, word.t2, lincl=False, rincl=False)
	
	    #option to apply pre-emphasis 
	    #emp_f = np.append(f[0], f[1:] - 0.97 * f[:-1])
		
		# get the spectrum
		FFT = librosa.stft(snippet, n_fft=n_fft, hop_length=hop, win_length=window) 

		# convolve the filterbank over the spectrum
		S = mel_f.dot(np.abs(FFT)) 

		def tpt_spectrum(S,t1,t2,step_size=step_size, plot=False,label='c'): 

			# redefine three equal tpts here instead of just start and end
			third = ((t2-t1) / 3)

			start_frame = np.int(t1/step_size)
			frame_two = np.int((third + t1)/step_size) 
			frame_three = np.int((third*2 + t1)/step_size) 
			end_frame = np.int(t2/step_size)

			# spectra averaged over three portions of segment 
			beg = np.mean(np.log(S[:,start_frame:frame_two]),axis=1)
			mid = np.mean(np.log(S[:,frame_two:frame_three]),axis=1)
			end = np.mean(np.log(S[:,frame_three:end_frame]),axis=1)

			return beg, mid, end 

		#loop through all of the (specified) labels on the "phone" tier of the current word
		for v in snippet_pm: 
			if re.match(segments, v.text):
				t1=v.t1-word.t1
				t2=v.t2-word.t1

				spectrum = tpt_spectrum(S, t1, t2,step_size=step_size)




				speakerlist.append(wav.split("_", 1)[0]) 
				phonelist.append(pm.tier('Phone').label_at(v.center).text)
				int_1_list.append(spectrum[0]) # index the correct array from tpt_spec function
				int_2_list.append(spectrum[1]) 
				int_3_list.append(spectrum[2])
				followinglist.append((pm.tier('Phone').next(v)).text)
				prevlist.append((pm.tier('Phone').prev(v)).text)
				wordlist.append(pm.tier('Word').label_at(v.center).text)
				notelist.append(pm.tier('Translation').label_at(v.center).text)
				t1list.append(v.t1)
				t2list.append(v.t2)
				durlist.append(v.t2-v.t1)
				morphlist.append((pm.tier('Morpheme').label_at(v.center)).text)
				worddurlist.append(word.t2-word.t1)
				# normalize by speaking rate
				int_1_normlist = [x / (word.t2-word.t1) for x in int_1_list]
				int_2_normlist = [x / (word.t2-word.t1) for x in int_2_list]
				int_3_normlist = [x / (word.t2-word.t1) for x in int_3_list]


	df = pd.DataFrame( OrderedDict( (('Speaker', pd.Series(speakerlist)),
	('Phone', pd.Series(phonelist)), ('Spectrum_int_1', pd.Series(int_1_list)),
	('Spectrum_int_2', pd.Series(int_2_list)), ('Spectrum_int_3', pd.Series(int_3_list)),
	('Previous',  pd.Series(prevlist)), ('Following',  pd.Series(followinglist)), 
	('Word',  pd.Series(wordlist)), ('Note',  pd.Series(notelist)), 
	('phone_t1',  pd.Series(t1list)), ('phone_t2',  pd.Series(t2list)),
	('Phone_duration',  pd.Series(durlist)), ('Word_duration', pd.Series(worddurlist)),
	('Normalized_int_1', pd.Series(int_1_normlist)), ('Normalized_int_2', pd.Series(int_2_normlist)), 
	('Normalized_int_3', pd.Series(int_3_normlist)), ('Morph_status', pd.Series(morphlist)))))

	df.to_csv(os.path.splitext(soundfile)[0]+'.mel_spectrum.csv', encoding='utf-8') 





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

# define some parameters
sr = 12000 # option to specify desired sampling rate
step_size = 0.01   # 10 ms between spectra
frame_size = 0.0256  # 25.6 ms chunk
hop = np.int(step_size * sr)  
window = np.int(frame_size * sr) 
fmax = np.int(sr/2) # nyquist frequency
fmin = 100
n_fft = 2048 # # of FFT coefficients to compute
n_mels = 29  # # of Mel filter bands

# compute the mel frequency filter bank
mel_f = librosa.filters.mel(sr, n_fft=2048, n_mels=29, fmin=100.0, fmax=6000, htk=True, norm=1)

for wav, tg in filelist: 
      print(wav) # sanity check
      processwav(wav, tg)