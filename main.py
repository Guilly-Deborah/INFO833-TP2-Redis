import redis
import pandas as pd
from geopy.distance import geodesic

def data_villes():
    #lecture du fichier csv des villes
    fichier= pd.read_csv("villes.csv")
    villes=[]
    for i in range(fichier.shape[0]):
        ville=fichier.loc[i][0].split(";")
        villes+=[{"ville":ville[0],'latitude':ville[1],'longitude':ville[2]}]
    return(villes)

def data_offres():
    #lecture du fichier csv des offres d'emplois
    fichier=pd.read_csv("offres.csv", sep=';')
    offres=[]
    for o in range(fichier.shape[0]):
        offre=fichier.loc[o]
        offres+=[{'offre':offre[0],'ville':offre[1]}]
    return(offres)


def trente_cinq_km(villes):
    #Recherche des villes à 35km ou moins d'Amiens
    ville_trentre_cinq =[]
    for ville in villes:
        if ville['ville'] == 'Amiens':
            ville_ref = ville
    vr_gps = (float(ville_ref['latitude']),float(ville_ref['longitude']))
    for v in villes :
        if v['ville'] != 'Amiens' :
            v1_gps=(float(v['latitude']),float(v['longitude']))
            kms=geodesic(vr_gps,v1_gps).kilometers
            if kms <= 35 :
                ville_trentre_cinq+=[v]
    return ville_trentre_cinq

if __name__ == "__main__":
    v =redis.Redis()
    villes=data_villes()
    for ville in villes:
        v.hset(ville['ville'], 'latitude', ville['latitude'])
        v.hset(ville['ville'], 'longitude', ville['longitude'])

    o = redis.Redis()
    offres=data_offres()
    cpt=1
    for offre in offres:
        o.hset(str(cpt), 'offre', offre['offre'])
        o.hset(str(cpt), 'ville', offre['ville'])
        cpt+=1

    liste_villes = trente_cinq_km(villes)
    print(liste_villes)