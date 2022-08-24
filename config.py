from datetime import date
from time import sleep
#tts_ : temps de pause entre chaque actions sur l'application nécessitant un chargement de la page
tts_accueil = 1.3 #Limite testé 1.2
tts_pageload = 0.6 #Limite testé 0.5
tts_notpageload = 0.25 #Limite testé 0.2
dict_month = {1:'//*[@id="tab-janvier"]/div/div/div/div/div', 2:'//*[@id="tab-février"]/div/div/div/div/div'
, 3:'//*[@id="tab-mars"]/div/div/div/div/div', 4:'//*[@id="tab-avril"]/div/div/div/div/div', 5:'//*[@id="tab-mai"]/div/div/div/div/div'
,  6:'//*[@id="tab-juin"]/div/div/div/div/div', 7:'//*[@id="tab-juillet"]/div/div/div/div/div', 8:'//*[@id="tab-août"]/div/div/div/div/div'
, 9:'//*[@id="tab-septembre"]/div/div/div/div/div', 10:'//*[@id="tab-octobre"]/div/div/div/div/div', 11:'//*[@id="tab-novembre"]/div/div/div/div/div'
, 12:'//*[@id="tab-décembre"]/div/div/div/div/div'}
l_month = list(dict_month.values())
l_month_keys = list(dict_month.keys())
month = int(date.today().month) #mois actuel du système
l_month = l_month[month-1:month+3] #liste des xpath de tous les mois réservables

log_link = 'https://beta.interieur.gouv.fr/candilib/candidat?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxZjZkZjM1OTIyYjVkMDAyOWIyMWExMSIsImxldmVsIjowLCJjYW5kaWRhdFN0YXR1cyI6IjMiLCJub21OYWlzc2FuY2UiOiJDQVVDSFkiLCJjb2RlTmVwaCI6IjE5MDQ5MzEwMTk1OCIsImhvbWVEZXBhcnRlbWVudCI6IjkzIiwiZGVwYXJ0ZW1lbnQiOiI5MyIsImVtYWlsIjoibWF4aW1lLmNhdWNoeTkzQGdtYWlsLmNvbSIsImlzRXZhbHVhdGlvbkRvbmUiOnRydWUsInBvcnRhYmxlIjoiMDc4MzgwOTEzMyIsInByZW5vbSI6Im1heGltZSIsImZpcnN0Q29ubmVjdGlvbiI6dHJ1ZSwiZGF0ZUVURyI6IjIwMjUtMDYtMjMiLCJpc0luUmVjZW50bHlEZXB0IjpmYWxzZSwiaWF0IjoxNjYxMzMxODU2LCJleHAiOjE2NjEzODU1OTh9.G8_D7VZPXJi_ucVUd-noMh2lAzC-6_lstIKSr9WYbi'
email_link = 'https://beta.interieur.gouv.fr/candilib/qu-est-ce-que-candilib'
dict_dep = { 93:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[9]/div',
			94:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[10]/div',
			77:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[5]/div'}
list_keys_dep =list(dict_dep.keys())
matrix_dep_centre=[#93
					 {
					  'BOBIGNY'			:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div',
					  'ROSNY SOUS BOIS' :'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div',
					  'NOISY LE GRAND'	:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div',
					  'VILLEPINTE'		:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[5]/div/div'
					 },
					{
					 'CRETEIL'			:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div',
					 'RUNGIS'			:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div',
					 'MAISONS ALFORT'	:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div'
					},
					{
					#77
					 'MELUN':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[6]/div/div'
					 }
					#94
					]
list_dep_xpath = list(dict_dep.values())#dict_dep
CAPTCHA_IMAGES = {
	"L'avion": "airplane",
	"Les ballons": "balloons",
	"L'appareil photo": "camera",
	"L‘appareil photo": "camera",
	"La Voiture": "car",
	"Le chat": "cat",
	"La chaise": "chair",
	"Lachaise": "chair",
	"Le trombone": "clip",
	"L'horloge": "clock",
	"Le nuage": "cloud",
	"L'ordinateur": "computer",
	"‘ordinateur": "computer",
	"L'enveloppe": "envelope",
	"L'oeil": "eye",
	"Le drapeau": "flag",
	"Le dossier": "folder",
	"Le pied": "foot",
	"Le graphique": "graph",
	"La maison": "house",
	"La clef": "key",
	"Laclef":"key",
	"La feuille": "leaf",
	"L'ampoule": "light-bulb",
	"Le cadenas": "lock",
	"La loupe": "magnifying-glass",
	"L'homme": "man",
	"La note de musique": "music-note",
	"Le pantalon": "pants",
	"Le crayon": "pencil",
	"L'imprimante": "printer",
	"Le robot": "robot",
	"Les ciseaux": "scissors",
	"Les lunettes de soleil": "sunglasses",
	"L'étiquette": "tag",
	"L'ètiquette": "tag",
	"L'arbre": "tree",
	"Le camion": "truck",
	"Le T-Shirt": "t-shirt",
	"Le parapluie": "umbrella",
	"La femme": "woman",
	"La planète": "world",
	"La planéte": "world",
}
