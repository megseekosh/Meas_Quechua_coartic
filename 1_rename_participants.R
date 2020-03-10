# tiny script to anonymize participants
# separate from results script because names
# cannot be shared publicly

data <- read.csv('Box Sync/Dissertation/Experiment_2/analysis/2019/analysis_scripts/thirds_CV.mel_spectrum.csv')

# remove filename with participant's name
data$Filename <- NULL
data$X <- NULL
data$speaker_anon <- data$Speaker
data$speaker_anon <- plyr::mapvalues(
  data$speaker_anon,
  from =
    c('Adriana', 
      'Alberto', 
      'Ana', 
      'AnaValeria', 
      'Ayelin', 
      'Betsy', 
      'Bryan',
      'Christian',
      'Cristina',
      'Daisi',
      'Daniela',
      'David',
      'Diego',
      'Elise',
      'Elsa',
      'Erik10',
      'Erik4',
      'Ezekiel',
      'Fabiana',
      'Fabiola',
      'Gladys',
      'Gladysadult',
      'Gliber4',
      'Gliber7',
      'Graciela',
      'Gwalberto',
      'James',
      'Janet',
      'Jhackson',
      'Jhamil',
      'JhamilB',
      'Jhanet',
      'Jhason',
      'Jhoel4',
      'Jhoel7',
      'Jhoel8',
      'Johan',
      'Josefina',
      'Joselin',
      'JoseLuis',
      'Juan',
      'JuanaChino',
      'JuanaR',
      'Justina',
      'Karina',
      'Katarin',
      'Lesli',
      'LimberDaylong',
      'LimberSchool',
      'Liset5',
      'Liset7',
      'LuisFernando',
      'Marco',
      'Marcos',
      'Maria',
      'Marina',
      'Mario',
      'Martha',
      'Nestor',
      'Noe',
      'Ronald7',
      'Ronald9',
      'Saida',
      'Sidle',
      'Suleika',
      'Sulma',
      'Sulmaadult',
      'Vladimir',
      'Wilber',
      'Yolanda'
      ),
  to = c("c1", 
         "c2", 
         "c3", 
         "c4",
         "c5", 
         "c6", 
         "c7",
         'c8',
         'c9',
         'c10',
         'c11',
         'c12',
         'c13',
         'c14',
         'a1',
         'c15',
         'c16',
         'c17',
         'a2',
         'c18',
         'c19',
         'a3',
         'c20',
         'c21',
         'c22',
         'c23',
         'c24',
         'c25',
         'c26',
         'c27',
         'c28',
         'c29',
         'c30',
         'c31',
         'c32',
         'c33',
         'c34',
         'a4',
         'c35',
         'c36',
         'c37',
         'a5',
         'a6',
         'c38',
         'c39',
         'c40',
         'c41',
         'c42',
         'c43',
         'c44',
         'c45',
         'c46',
         'c47',
         'c48',
         'c49',
         'a7',
         'c50',
         'a8',
         'c51',
         'c52',
         'c53',
         'c54',
         'c55',
         'c56',
         'c57',
         'c58',
         'a9',
         'c59',
         'c60',
         'c61'
         )
)

unq_data<- data[!duplicated(data$Speaker), ] # sanity check

# now remove any mention of specific names
data$Speaker <- NULL
data$Speaker <- data$speaker_anon
data$speaker_anon <- NULL


# write it out
write_csv(data, 'Box Sync/Dissertation/Experiment_2/analysis/2019/analysis_scripts/thirds_CV.anonymized.csv')








