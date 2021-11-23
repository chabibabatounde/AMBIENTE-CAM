# coding: utf-8
import time
from time import sleep
import datetime
import os
import json
from picamera import PiCamera
import sys
import threading

tick = 0;
default_config = {'video':{'run':False, 'fps':3, 'duration':'10', 'wait':'15', 'base_name':'cam_video_'}, 'image':{'run':False, 'wait':'10', 'base_name':'cam_image_'}, 'programme_name' :'test'}
configuration = None
#Fonction de Log
def log(message):
	try:
		objet = dict()
		objet['message'] = message
		laDate = datetime.datetime.now()
		objet['timestamp'] = str(laDate.hour) + ":" +str(laDate.minute) + ":" +str(laDate.second)+" "+str(laDate.year) + "-" +str(laDate.month) + "-" +str(laDate.day)
		donnees = json.dumps(objet)
		trace = open("/home/pi/Camera/Data/log.json","a")
		trace.write(donnees+",\n")
		trace.close()
	except:
		pass
			
log("Demarrage du programme")

#=== Lecture du fichier de configuration ===#
log("Lecture du fichier de configuration")
try:
	f = open("/home/pi/Camera/config.txt", "r")
	configuration=json.loads(f.read())
	log("Fichier de configuration lue avec succes")
except:
	configuration =  default_config
	log("Echec de la lecture du fichier de configuration. Chargement du fichier par défaut")
finally:
	f.close()

#=== Test de la camera ===#
try:
	camera = PiCamera()
	camera.resolution = (1920,1080)
	camera.rotation = 180
	sleep(0.25)
	camera.capture("/home/pi/Camera/Data/image-test.jpeg")
	#Eteindre led ROUGE
	image_tick = 1
	video_tick = 1
	camera.close()
	
	video_time = time.time()
	image_time = time.time()
	
	while (1):
		#Bloc Photo
		if configuration['image']['run'] :
			if(time.time()>= image_time):
				print("Prise de photo en cours...")
				camera = PiCamera()
				camera.resolution = (1920,1080)
				camera.rotation = 180
				sleep(0.25)
				camera.capture("/home/pi/Camera/Data/Images/"+configuration['image']['base_name']+str(image_tick)+".jpeg")
				log("Image N "+str(image_tick)+" capturée")
				log("attente de la prochaine prise d'image")
				image_time = time.time()+int(configuration['image']['wait'])
				image_tick = image_tick+1
				print("Prise de photo Terminée")
				print("Prochaine prise dans "+str(configuration['image']['wait'])+"s")
				camera.close()
		
		#Bloc Video
		if configuration['video']['run'] :
			if(time.time()>= video_time):
				print("Enregistrement vidéo en cours...")
				log("Enregistrement brut de la video")
				camera.close()
				commande  = "sudo raspivid --nopreview -rot 180 -fps "+str(configuration['video']['fps'])+" -o /home/pi/Camera/Source/h264/"+configuration['video']['base_name']+str(video_tick)+".h264 -t "+str(configuration['video']['duration']*1000)
				os.system(commande)
				log("Enregistrement brut termine")
				sleep(5)
				log("Traitement du fichier brut")
				os.system("sudo rm /home/pi/Camera/Data/Videos/"+configuration['video']['base_name']+str(video_tick)+".mp4")
				#os.system("sudo MP4Box -add /home/pi/Camera/Source/h264/"+configuration['video']['base_name']+str(video_tick)+".h264 -fps "+str(configuration['video']['fps'])+" /home/pi/Camera/Data/Videos/"+configuration['video']['base_name']+str(video_tick)+".mp4")
				#os.system("sudo rm /home/pi/Camera/Source/h264/"+configuration['video']['base_name']+str(video_tick)+".h264")
				log("Video N "+str(video_tick)+" traite et enregistre")
				video_time = time.time()+int(configuration['video']['wait'])
				video_tick = video_tick+1
				print("Enregistrement vidéo Terminé")
		
except:
	#Allumer led ROUGE
	camera.close()
