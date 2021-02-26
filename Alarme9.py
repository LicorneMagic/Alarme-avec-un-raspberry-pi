import threading
import RPi.GPIO as GPIO
import time
from pirc522 import RFID
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Ne pas changer
interval=0
temps_initial=0
temps_4min=0
debut_temps = time.time()
I=1
U=0
Z=0
x=0

#Varialbles
Lumière=38
LED_Rouge=10
LED_Verte=8
LED_Orange=12
Secteur_240V=36
Detecteur=11
Couloir=37
Cuisine=35
Guirlande1=5
Guirlande2=7
Relais_guirlande=3
Contacteur=40
Alarme_ouverte=33
nbr_lecture_88=2
nom_fichier_état_alarme = 'état alarme.txt'
nom_fichier_log = 'Fichier log.txt'


#Definitions composants
GPIO.setup(Lumière, GPIO.OUT)
GPIO.setup(LED_Rouge, GPIO.OUT)
GPIO.setup(LED_Verte, GPIO.OUT)
GPIO.setup(LED_Orange, GPIO.OUT)
GPIO.setup(Detecteur, GPIO.IN)
GPIO.setup(Guirlande1, GPIO.OUT)
GPIO.setup(Guirlande2, GPIO.OUT)
GPIO.setup(Relais_guirlande, GPIO.OUT)
GPIO.setup(Cuisine, GPIO.IN)
GPIO.setup(Couloir, GPIO.IN)
GPIO.setup(Secteur_240V, GPIO.IN)
GPIO.setup(Contacteur, GPIO.OUT)
GPIO.setup(Alarme_ouverte, GPIO.IN)

#Definition des cartes
RFID_UID0 = [X, X, X, X, X]  #Déclaration des diférentes cartes RFID
RFID_UID1 = [X, X, X, X, X]   
RFID_UID2 = [X ,X ,X ,X ,X] 
RFID_UID3 = [X ,X ,X ,X ,X]   
RFID_UID4 = [X ,X ,X ,X ,X] 
RFID_UID5 = [X ,X ,X ,X ,X]   
RFID_UID6 = [X ,X ,X ,X ,X] 
rc522 = RFID() #On instancie la lecture du badge a une variable


def LEDOFF(): # On déclare un programe pour éteindre toutes les leds
    GPIO.output(LED_Orange, GPIO.LOW)
    GPIO.output(LED_Rouge, GPIO.LOW)
    GPIO.output(Lumière, GPIO.LOW)
    GPIO.output(LED_Verte, GPIO.LOW)

def Activé(): # On déclare un programe pour allumer toutes les leds
    GPIO.output(LED_Orange, GPIO.HIGH)
    GPIO.output(LED_Rouge, GPIO.LOW)


def Désactivé(): # On déclare un programe pour Désactiver les leds du mode alarme 
    GPIO.output(LED_Orange, GPIO.LOW)
    GPIO.output(LED_Rouge, GPIO.LOW)
    GPIO.output(LED_Verte, GPIO.HIGH)

def Détection(): # On déclare un programe pour allumer les leds en cas d'activation de l'alarme  
    GPIO.output(LED_Orange, GPIO.HIGH)
    GPIO.output(LED_Rouge, GPIO.HIGH)
    GPIO.output(LED_Verte, GPIO.LOW)



def email_send_alarme_déclanché(): # On déclare un programe pour envoyer un email en cas d'activation de l'alarme 
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText('L`alarme a été Déclanché via un capteur infrarouge, veuillez-vous rendre sur ce site via le VPN afin de vérifier: http://192.168.1.40:1945/ ou http://192.168.1.40:1880/ui pour la désactivé')
    message['Subject'] = 'Alarme Maison Déclanché'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()



def email_send_alarme_déclanché2(): # On déclare un programe pour envoyer un email en cas d'activation de l'alarme si la sirène vien a etre démonté sans avoir passer le badge de maintenance
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText("La Sirène à été démonté et c'est donc déclanchée, veuillez-vous rendre sur ce site via le VPN afin de vérifier: http://192.168.1.40:1945/ ou http://192.168.1.40:1880/ui pour la désactivé")

    message['Subject'] = 'Alarme Maison Déclanché système démonté'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()



def email_send_Alarme_Désactivé(): # On déclare un programe pour envoyer un email en cas de désactivation de l'alarme 
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText('L`alarme à été désactivée, vous pouvez vous rendre sur ce site via le VPN afin de vérifier: http://192.168.1.40:1945/ et http://192.168.1.40:1880/ui pour l`activée')
    message['Subject'] = 'Alarme Désactivée'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()



def email_send_Persone_Tiers(): # On déclare un programe pour envoyer un email en cas de désactivation de l'alarme par une personne tiers
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText('L`alarme à été désactivée via une personne tier à la maison, vous pouvez vous rendre sur ce site via le VPN afin de vérifier: http://192.168.1.40:1945/ et http://192.168.1.40:1880/ui pour l`activée')
    message['Subject'] = 'Alarme Désactivée via une personne tier'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()



def Coupure_de_courant_soudaine(): # On déclare un programe pour envoyer un email en cas de coupure de courrant
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText("L'alimentation a été coupé, le système est maintenant passé en mode économie d'énergie et fonctionne sur batterie. Son autonomie est estimée à 8H30 maximum")
    message['Subject'] = "Alimentation coupée, passage en mode économie d'énergie sur batterie"
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()   



def Coupure_de_courant_depuis_4H(): # # On déclare un programe pour envoyer un email en cas de coupure de courrant depuis 4H
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText("L'alimentation est coupé depuis maintenant plus de 4 Heures, le système deverait encore pouvoir être Alimenté durant 4H de plus")
    message['Subject'] = 'Déja 4 Heure de coupure de courant'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()   




def Coupure_de_courant_depuis_7H(): # On déclare un programe pour envoyer un email en cas de coupure de courrant depuis 7H
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText("L'alimentation est coupé depuis maintenant plus de 7 Heures, le système va progressivement commencer s'éteindre et la sirène va s'activé. Il vous reste au mieux 1H30")
    message['Subject'] = 'Urgence ! 7 Heure de coupure de courant'
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()   



def remise_sous_tention(): # On déclare un programe pour envoyer un email en cas de remise en route du courrant
    emails = "email a envoyer , email a envoyer, email a envoyer, email a envoyer"

    message = MIMEText("L'alimentation de l'alarme a été rétablie. La batterie se recharge d'ores et déja")
    message['Subject'] = "L'alimentation de l'alarme rétablie"
    message['From'] = 'email qui sert a envoyer'
    message['To'] = emails

    server = smtplib.SMTP('smtp.gmail.com:587') # a changer si on utilise pas une adresse email google
    server.starttls()
    server.login('email qui sert a envoyer','mot de passe')
    server.send_message(message)
    server.quit()   



def Activation_alarme(): # boucle qui verifie si il faut activer l'alarme
  y=1
  x=0
  f=0
  s=1
  q=0
  m=0
  while True:
    nom_fichier_état_alarme = 'état alarme.txt'                       #in lit un fichier 
    mon_fichier = open(nom_fichier_état_alarme, "r")
    contenu = mon_fichier.read()
    mon_fichier.close()
    etat = int(contenu)
    time.sleep(.45)
    if GPIO.input(Secteur_240V) == 0 and etat != 36:  # si dans ce fichier il n'y a pas le nombre 36 qui est le mode maintenance et que il y a une couppure d'éléctricité alors envoyer les différents emails.
        f+=1
        s=0 
        if f == 1 :
            r= time.time()
            threading.Thread(target=Coupure_de_courant_soudaine).start()
        e=time.time()
        o = e - r
        if o > 14400 :
            q+=1
            if q == 1:
                threading.Thread(target=Coupure_de_courant_depuis_4H).start()
        if o > 25200 :
            m+=1
            if m == 1:
               threading.Thread(target=Coupure_de_courant_depuis_7H).start()
    else: # Sinon on restore tout par défault
        s+=1
        f=0
        q=0
        m=0
        if s == 1 :
            threading.Thread(target=remise_sous_tention).start()
    if etat == 90 and x == 0:  # si on recoit la comande d'activer l'alarme on verifie si elle vien d'une intrusion ou d'un démontage de l'alarme et on envoie le mail adéquoi
        GPIO.output(Contacteur, GPIO.LOW)
        if GPIO.input(Alarme_ouverte) == 0 : 
           threading.Thread(target=email_send_alarme_déclanché2).start()
        else :
           threading.Thread(target=email_send_alarme_déclanché).start()
        print("alarme Déclanché")
        x+=1
    heure_actuelle = time.strftime("%H")
    x = int(heure_actuelle)
    if etat == 90 and x > 17 or etat == 90 and x < 8:  # ici on active l'alarme et on prend l'heure car si cela ce passse la nuit, alors toutes les lumières extérieur vont clignoté en plus de la sirène
        GPIO.output(Lumière, GPIO.LOW)
        GPIO.output(LED_Rouge, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(Lumière, GPIO.HIGH)
        GPIO.output(LED_Rouge, GPIO.LOW)
    else:
        if etat == 90:
             GPIO.output(LED_Rouge, GPIO.HIGH)
             time.sleep(.5)
             GPIO.output(LED_Rouge, GPIO.LOW)
        if etat != 90:
            x=0
            GPIO.output(LED_Rouge, GPIO.LOW)



def Lumière_Dehors():    # Ici on gère les lumières extèrieur
  nom_fichier_état_alarme = 'état alarme.txt'                       #4
  heure_actuelle=0
  x=0
  y=0
  état_alarme=0
  r=time.time()+90
  fichier = 22
  interval=0
  while True :
    mon_fichier = open(nom_fichier_état_alarme, "r")
    lolita = mon_fichier.read()
    mon_fichier.close()
    fichier = int(lolita)
    heure_actuelle = time.strftime("%H")
    x = int(heure_actuelle)
    time.sleep(.45)
    t=time.time() 
    if fichier != 90 and x > 17 or fichier != 90 and x < 8: # Si une personne est détecter alors la lumière s'allume 1,5 minute sauf si l'alarme est activer au quel cas il cette boucle se désactive et se remet en route lors de sa désactivation
    y=0
        if GPIO.input(Detecteur) == 1:
            GPIO.output(Lumière, GPIO.HIGH)
            r=time.time()
        interval = t-r
        if interval > 90:
           GPIO.output(Lumière, GPIO.LOW)
    else:
        y=y+1
        if y == 1:
           GPIO.output(Lumière, GPIO.LOW)


def RFID():  #Ici on lit les différents badges et on les assosie analyse
  uid = 0
  bbc = 22
  d = 0
  while True:
    rc522.wait_for_tag()  #tant que le système a pas lu de carte alors il attan
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

    if not error : #Si on a pas d'erreur
        (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps

    if RFID_UID1 == uid and bbc == 22 or RFID_UID2 == uid and bbc == 22 or RFID_UID3 == uid and bbc == 22 or RFID_UID4 == uid and bbc == 22 or RFID_UID5 == uid and bbc == 22 or RFID_UID6 == uid and bbc == 22: # icic on met les cartes qui peuveunt désactiver le système
        Temps_actuelle = time.asctime()
        mon_fichier = open(nom_fichier_état_alarme, "r")
        contenu = mon_fichier.read()
        mon_fichier.close()
        contenu_int = int(contenu)
        tuid = str(uid)
        if contenu_int == 22:  # si l'alarme n'était pas armer alors elle s'arme maintenan
            GPIO.output(LED_Verte, GPIO.HIGH)
            GPIO.output(LED_Orange, GPIO.HIGH)
            GPIO.output(LED_Rouge, GPIO.LOW)
            print("activation de l'alarme dans 15 secondes ...")
            time.sleep(15)
            mon_fichier = open(nom_fichier_état_alarme, "w")
            mon_fichier.write("88")  #ici on remet le fichier a jour pour informer les autres programme que l'alarme est armé
            mon_fichier.close()
            GPIO.output(LED_Verte, GPIO.LOW)
            GPIO.output(LED_Orange, GPIO.HIGH)
            GPIO.output(LED_Rouge, GPIO.LOW)
            GPIO.output(Lumière, GPIO.LOW)
            print("alarme armée")
        else :  # Sinon on la désactive
            print("Sirène Désactivé") 
            GPIO.output(Contacteur, GPIO.HIGH)
            while GPIO.input (Alarme_ouverte) == 0 :  #tant que la sirène est démonté on fait clignoter les led a l'entrer et on refuse toute autre action 
                mon_fichier = open(nom_fichier_état_alarme, "w")
                mon_fichier.write("36")
                mon_fichier.close()
                GPIO.output(LED_Verte, GPIO.HIGH)
                GPIO.output(LED_Orange, GPIO.HIGH)
                GPIO.output(LED_Rouge, GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(LED_Verte, GPIO.LOW)
                GPIO.output(LED_Orange, GPIO.LOW)
                GPIO.output(LED_Rouge, GPIO.LOW)
                time.sleep(.2)
            if contenu_int == 90 : # si l'alarme était activer on envoie un mail comme quoi elle ne l'est plus
                threading.Thread(target=email_send_Alarme_Désactivé).start()
                print("Email d'alarme désactivé envoyer")
            print("Alarme Désactivé")
            mon_fichier = open(nom_fichier_état_alarme, "w") #ici on remet le fichier a jour pour informer les autres programme que l'alarme est plus armé
            mon_fichier.write("22")
            mon_fichier.close()
            GPIO.output(LED_Verte, GPIO.HIGH)
            GPIO.output(LED_Orange, GPIO.LOW)
            GPIO.output(LED_Rouge, GPIO.LOW)
            heure_actuelle=time.strftime("%H")
            x = int(heure_actuelle)

            if x < 17 and x > 8 : # Ici on écrit sur un fichier outes les personnes qui on touché a l'alarme ansi que la date et l'heure précise
                time.sleep(5)
                GPIO.output(Lumière, GPIO.LOW)
            mon_fichier = open(nom_fichier_log, "a")
            mon_fichier.write(tuid+" "+Temps_actuelle+"\n")
            mon_fichier.close()

            if RFID_UID6 == uid or RFID_UID3 == uid or RFID_UID1 == uid : # Si l'alarme est désarmer via une personne tier alors on imforme les propriétaires
                threading.Thread(target=email_send_Persone_Tiers).start()
                print("Email Personne Tiers envoyer")
    else:   #ici on a le esle du cas ou le badge n'est pas autorisé a déramer l'alarme cela paut aussi arriver si le badge est mal lue ou en cas d'interférence
        GPIO.output(LED_Rouge, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_Rouge, GPIO.LOW)

    if RFID_UID0 == uid : # ici on dit que en plus si on a passer le badge spécial de maintenance alors on doi désactiver toutes les sécurité et ne n'activer l'alarme dans aucune sirconstance 
        if d == 1 :
                mon_fichier = open(nom_fichier_état_alarme, "w")
                mon_fichier.write("22")
                mon_fichier.close()
                GPIO.output(LED_Verte, GPIO.HIGH)
                GPIO.output(LED_Orange, GPIO.LOW)
                print("Mode installateur désactivé")
                bbc = 22
                d = 0
        else : # quand on le repasse on remet le sistème en route
                mon_fichier = open(nom_fichier_état_alarme, "w")
                mon_fichier.write("36")
                mon_fichier.close()
                GPIO.output(LED_Verte, GPIO.HIGH)
                GPIO.output(LED_Orange, GPIO.HIGH)
                print("Mode installateur activé")
                bbc = 36
                d = 1
    uid = 0
    time.sleep(1.5)

mon_fichier = open(nom_fichier_état_alarme, "w") #ici a chaque rédémarage l'alarme se remet en position armé mais cela n'est pas obligatoire 
contenu = mon_fichier.write("88")
mon_fichier.close()


print("Programme lancée") # ici commence le programe et on démare ses sous parties
LEDOFF()
GPIO.output(Contacteur, GPIO.HIGH)
GPIO.output(LED_Orange, GPIO.HIGH)
threading.Thread(target=Guirlande).start()
threading.Thread(target=Lumière_Dehors).start()
threading.Thread(target=Activation_alarme).start()
threading.Thread(target=RFID).start()


mon_fichier = open(nom_fichier_état_alarme, "r") # ici on lit la valeur du fichier contenan l'éta de l'alarme
contenu = mon_fichier.read()
mon_fichier.close()
contenu_int = int(contenu)

#if contenu_int != 100:   # Ici on peut faire en sorte que si une personne réussi a courcircuiter le raspberry alor que l'alarme était activer, alors si il redémare tout de meme on active tout de suite l'alarme 
    #GPIO.output(Contacteur, GPIO.HIGH)
    #mon_fichier = open(nom_fichier_état_alarme, "w")
    #contenu = mon_fichier.write("88")
    #mon_fichier.close()


while True : # ici on regarde si les capteurs son activer ou non et on écrit dans le fichier en fonction de cela
   mon_fichier = open(nom_fichier_état_alarme, "r")
   contenu = mon_fichier.read()
   mon_fichier.close()
   contenu_int = int(contenu)
   time.sleep(.15)

   if GPIO.input(Couloir) == 0  and contenu_int == 88 or GPIO.input(Cuisine) == 0 and contenu_int == 88 or GPIO.input(Alarme_ouverte) == 0 and contenu_int != 36 and contenu_int != 90:
      Détection()
      mon_fichier = open(nom_fichier_état_alarme, "w")
      mon_fichier.write("90")
      mon_fichier.close()
      GPIO.output(LED_Rouge, GPIO.HIGH)

print("Erreur, fin de Programme")
