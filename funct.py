# Fuctions and imports
import sqlite3
import pandas as pd
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import os
import os
import pygame

# I wrote this file as a Blackbox of functions so I can keep my main workspace programing much cleaner


# frist 250 frnehc list her -- got from GPT but is able to generate as well its just easy start for the presentation to start here

French_250 = "le, de, un, être, et, à, il, avoir, ne, je, son, que, se, qui, ce, dans, en, du, elle, au, vous, avec, pour, pas, sur, plus, me, faire, nous, comme, ou, mais, pouvoir, dire, aller, voir, leur, bien, où, sans, tout, homme, année, jour, même, prendre, aussi, quelque, mon, donner, temps, très, savoir, falloir, venir, mettre, autre, vouloir, déjà, trouver, personne, rendre, part, quelque, passer, peu, avant, parce, contre, place, grand, lui, notre, vie, encore, après, monde, petit, chose, maison, rien, tous, enfant, tenir, droit, travailler, maintenant, parler, pendant, comprendre, point, femme, dernier, devoir, main, arriver, certains, jeune, attendre, raison, heure, rester, appeler, après, longtemps, quelque, tête, porter, certain, père, vieux, nuit, ensemble, force, marcher, question, aimer, aider, répondre, heure, sembler, jouer, besoin, retrouver, chose, seul, perdre, cause, montrer, pays, moment, côté, certain, écrire, famille, groupe, commencer, souvenir, apprendre, partir, enfant, enfin, pouvoir, pied, voix, attendre, frère, minute, guerre, tomber, soleil, histoire, chercher, eau, matin, clair, suivre, libre, heureux, amour, route, semaine, mille, image, lettre, terre, ouvrir, papa, fille, possible, soleil, long, lieu, guerre, mourir, espoir, fenêtre, cœur, vent, dormir, ciel, salle, lumière, mur, marcher, forêt, ami, question, rue, chat, fermer, appel, route, pont, âge, ville, nombre, mur, hiver, peur, joie, ciel, saison, vide, corps, camp, feu, retour, face, île, été, pluie, hiver, mère, secret, nuit, animal, oiseau, ange, mer, dieu, silence, village, prison, bruit, fruit, vérité, ombre, pierre, enfant, étoile, jour, lune, roi, reine, pierre, soldat, neige, miroir, homme, femme, monde, rêve, plage, désert, arbre, chemin, eau, forêt, maison, nuit, rivière, secret, terre, vent, voyage, ange, bateau, ciel, couleur, diable, étoile, fleur, lumière, montagne, oiseau, ombre, prison, silence, soleil, tristesse, vérité, village, voix, amour, ciel, désert, étoile, fleur, forêt, lumière, mer, montagne, nuit, oiseau, pierre, rivière, soleil, terre, vent, voyage"

#converting to list
words = French_250.split(",")


# Functions below: ( all descriopn on them are in the doc strings)


def add_words(words, db):
    '''Adds the words with empty translations/(definitions) and examples fluency and visted set to 0'''
    with sqlite3.connect('Word_DB.sqlite') as conn:
        cursor = conn.cursor()
        definition = "--"
        example = "--"
        fluency = 0
        visited = 0

        # put the fr words into DB
        for word in words:
            #print(word)
            cursor.execute('''
            INSERT OR IGNORE INTO Words (word, definition, example, fluency, visited)
            VALUES (?, ?, ?, ?, ?)
            ''', (word, generate_def(word).lower(), example, fluency, visited))
        conn.commit()


def print_Words_db():
    '''Prints all the words currently in the DB'''
    conn = sqlite3.connect('Word_DB.sqlite')
    df = pd.read_sql('SELECT * FROM words', conn)
    print(df)
    conn.close()


def clear_Words_db():
    '''Deleted all the words currntly in the DB'''
    conn = sqlite3.connect("Word_DB.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM words")
    conn.commit()
    conn.close()

def generate_def(word): 
    '''Google translate generating a definition/ traslation for each word'''
    try:
        # set to fr for french and en for english
        translation = GoogleTranslator(source='fr', target='en').translate(word)
        return translation
    except Exception as e:
        return f"Translation error: {e}"



def create_pronunciation(sentence): 
    '''Creating the specifc pronunication for the word or sentence all are saved under their name in the pronucations folder
    - can change to just making the call each time (ex create, pronuncance, then delete on click each time)'''
    # audio is made with with gTTS -
    tts = gTTS(text=sentence, lang="fr", slow=False)
    filename = "Pronunciations/"+(sentence)+".mp3"
    tts.save(filename)



def play_mp3(sentence):
    '''A function to play to MP3 sounds generated previosuly'''
    mp3_path = f"Pronunciations\{sentence}.mp3"

    if not os.path.exists(mp3_path):  
       print("MP3 file not found.") 
       return
    
    pygame.mixer.init()
    pygame.mixer.music.load(f"Pronunciations\{sentence}.mp3")
    pygame.mixer.music.play()
    
    print(f"Playing: {sentence}")

    # this might be required later so i'll keep it open like this
    while pygame.mixer.music.get_busy():  # had some probllems needed this to help
        continue
    else:
        pygame.mixer.quit()  #Here we close it so it doesnt overlap and cause other probelms



def speak_new_sentence(sentence):
    '''Just a combination to creaing and playing at the same time'''
    create_pronunciation(sentence)
    play_mp3(sentence)



def clear_pronunciations_folder():
    '''clears all the Ps to the folder aptly called Pronunications -- altouhg i think the real one is spelt correctly. '''
    folder_path =  "Pronunciations"

    # just to stop pygame if still running else error same error mentioed in play_mp3 function
    pygame.mixer.music.stop()  
    pygame.mixer.quit() 
    

    deleted_files = 0
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            deleted_files += 1
            print(f"Deleted: {file}")

    if deleted_files == 0:
        print("all files deleted MP3 ")
    else:
        print(f"Deleted {deleted_files} MP3 file(s).")




def create_p_for_all(db_path):
    """Fetch and print all words under the 'word' category from the SQLite database."""
    db_path = "Word_DB.sqlite"
    # Connects to DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # gets all words here 
    query = "SELECT word FROM words"  
    cursor.execute(query)
    words = cursor.fetchall()
    for word in words:
        create_pronunciation(word[0], )
    conn.close()
