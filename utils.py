import pandas as pd
import random
from datetime import datetime
from dades import connexio


def df_profes():
    """DataFrame amb les dades dels professors actius"""
    ct = connexio()
    query = ("SELECT Dni,Nom,Cognom,CodiHorari FROM Professor WHERE Actiu=1;")
    with ct.cursor() as cursor:
        cursor.execute(query)
        profes = pd.DataFrame(cursor.fetchall(), columns=['Dni', 'Nom', 'Cognom', 'CodiHorari'])
    ct.close()
    return profes.sort_values(by='CodiHorari')


def llista_dni_actius():
    """Llista de tot els DNI de professors actius"""
    ct = connexio()
    query = ("SELECT Dni FROM Professor WHERE Actiu=1;")
    with ct.cursor() as cursor:
        cursor.execute(query)
        llista_dni = []
        for row in cursor.fetchall():
            llista_dni.append(row[0])
    ct.close()
    return llista_dni


def llista_dni_presents():
    """Llista de DNIs dels professors presents al centre"""
    llista_presents = []
    current_day = datetime.today().strftime("%Y-%m-%d")

    ct = connexio()
    query = ("SELECT Dni FROM Registre WHERE Data='" + current_day + "' AND HoraSortida IS NULL;")
    with ct.cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            llista_presents.append(row[0])
    ct.close()
    return llista_presents


def llista_dni_absents():
    """Llista de DNIs dels professors fora del centre"""
    dni = llista_dni_actius()
    presents = llista_dni_presents()
    for i in presents:
        dni.remove(i)
    return dni


def missatge_entrada(nom, hora):
    missatges = ["Bon dia", "Hola", "Salutacions", "Benvingut"]
    text = random.choice(missatges)
    text += " " + nom + "!\n"
    text += "Entrada registrada a les " + hora + " "
    text +=  u"\U000027A1"
    return text


def missatge_sortida(nom, hora):
    missatges = ["Adéu", "Que vagi bé", "Fins aviat", "Fins la propera"]
    text = random.choice(missatges)
    text += " " + nom + "!\n"
    text += "Sortida registrada a les " + hora + " "
    text += u"\U00002705"
    return text


def hora_lectiva_actual():
    """Torna un enter amb l'hora lectiva actual segons l'horari del centre"""
    current_time = datetime.now()
    hora = current_time.hour
    minuts= current_time.minute
    hora_lectiva = 0
    if hora == 8 and minuts>10:
        hora_lectiva=1
    elif hora == 9:
        if minuts<5: hora_lectiva=1
        else: hora_lectiva=2
    elif hora==10:
        if minuts<55: hora_lectiva=3
        else: hora_lectiva=4
    elif hora==11:
        if minuts<25: hora_lectiva=4
        elif minuts<55: hora_lectiva=5
        else: hora_lectiva=6
    elif hora==12:
        if minuts<50: hora_lectiva=6
        else: hora_lectiva=7
    elif hora==13:
        if minuts<45: hora_lectiva=7
        else: hora_lectiva=8
    elif hora==14 and minuts<40:
        hora_lectiva=8
    return hora_lectiva


def dia_lectiu_actual():
    """Torna un enter amb el dia de la setmana"""
    current_time = datetime.now()
    dia = current_time.weekday()
    return dia + 1
