# Meas_Quechua_coartic
Measure and analyze child and adult coarticulatory patterns via mel frequency spectra

## Acoustic measures

**get_mel_spec_bythirds.py** - option to compute coarticulation spectrally (spectral distance) by taking spectra from middle third of two adjacent phones and computing average spectrum from each phone; generates filename+`mel_spectrum.csv` which can be read into R for post-processing

To execute this script:

1. move inside of corpus directory that contains .wav and .TextGrid files _with the same name_  

  code here
  
2. run script over entire directory

  python3 get_mel_spec_bythirds.py walk

## Data analysis

**1_rename_participants.R** - gives participants anonymous IDs; not included in repo as it contains deanonymized participant information

**2.R** - selects word environments; calculates Euclidean distance between spectral vectors; modified version that does not include deanonymized participant information is included in repo 




Option to measure spectrally (spectral distance)
or temporally (more dynamic) 

## Additional code in this repo

**coartic_as_transition.py** - option to compute coarticulation temporally (more dynamic); one technique used to measure coarticulation in Cychosz et al. (2019)

**get_mel_spec.py** - option to compute coarticulation spectrally (spectral distance); one technique used to measure coarticulation in Cychosz et al. (2019)

## Papers

Cychosz, M. (_submitted_). [Word structure in early Quechua speech: Coarticulation and inflectional morphology.] (https://psyarxiv.com/26uyb) 

Cychosz, M., Edwards, J., Munson, B., & Johnson, K. (2019). [Spectral and temporal measures of coarticulation in child speech.](http://linguistics.berkeley.edu/~mcychosz/Cychosz_JASA-EL_2019.pdf) _Journal of the Acoustical Society of America-Express Letters, 146_(6), EL516-EL522. 

