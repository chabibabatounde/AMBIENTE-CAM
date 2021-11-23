import glob
import os
base_pwd = "/media/rodolpho/438BE51024EDD520/Expe-Oursin/"
fps = 5
suite = "Camera1/Camera/Source/h264/"
fichiers = glob.glob(base_pwd+suite+"*")
i = 1
for fichier in fichiers:
    res = fichier.split("/")
    base_name = res[len(res)-1]
    base_name = base_name.split(".")
    base_name = base_name[0]
    commande = "MP4Box -add "+fichier+" -fps "+str(fps)+" "+base_pwd+"Camera1/Camera/Data/Videos/"+str(base_name)+".mp4"
    os.system(commande)
    i += 1