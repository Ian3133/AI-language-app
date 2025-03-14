# Fuctions and imports
import sqlite3
import pandas as pd
from deep_translator import GoogleTranslator


from gtts import gTTS
import playsound
import os

import os
import pygame


# frist 250 frnehc list her 

French_250 = "le, de, un, être, et, à, il, avoir, ne, je, son, que, se, qui, ce, dans, en, du, elle, au, vous, avec, pour, pas, sur, plus, me, faire, nous, comme, ou, mais, pouvoir, dire, aller, voir, leur, bien, où, sans, tout, homme, année, jour, même, prendre, aussi, quelque, mon, donner, temps, très, savoir, falloir, venir, mettre, autre, vouloir, déjà, trouver, personne, rendre, part, quelque, passer, peu, avant, parce, contre, place, grand, lui, notre, vie, encore, après, monde, petit, chose, maison, rien, tous, enfant, tenir, droit, travailler, maintenant, parler, pendant, comprendre, point, femme, dernier, devoir, main, arriver, certains, jeune, attendre, raison, heure, rester, appeler, après, longtemps, quelque, tête, porter, certain, père, vieux, nuit, ensemble, force, marcher, question, aimer, aider, répondre, heure, sembler, jouer, besoin, retrouver, chose, seul, perdre, cause, montrer, pays, moment, côté, certain, écrire, famille, groupe, commencer, souvenir, apprendre, partir, enfant, enfin, pouvoir, pied, voix, attendre, frère, minute, guerre, tomber, soleil, histoire, chercher, eau, matin, clair, suivre, libre, heureux, amour, route, semaine, mille, image, lettre, terre, ouvrir, papa, fille, possible, soleil, long, lieu, guerre, mourir, espoir, fenêtre, cœur, vent, dormir, ciel, salle, lumière, mur, marcher, forêt, ami, question, rue, chat, fermer, appel, route, pont, âge, ville, nombre, mur, hiver, peur, joie, ciel, saison, vide, corps, camp, feu, retour, face, île, été, pluie, hiver, mère, secret, nuit, animal, oiseau, ange, mer, dieu, silence, village, prison, bruit, fruit, vérité, ombre, pierre, enfant, étoile, jour, lune, roi, reine, pierre, soldat, neige, miroir, homme, femme, monde, rêve, plage, désert, arbre, chemin, eau, forêt, maison, nuit, rivière, secret, terre, vent, voyage, ange, bateau, ciel, couleur, diable, étoile, fleur, lumière, montagne, oiseau, ombre, prison, silence, soleil, tristesse, vérité, village, voix, amour, ciel, désert, étoile, fleur, forêt, lumière, mer, montagne, nuit, oiseau, pierre, rivière, soleil, terre, vent, voyage"

#converting to list
words = French_250.split(",")




# functions
def add_words(words, db):
    '''Adds the words with empty translations/(definitions) and examples fluency and visted set to 0'''
    with sqlite3.connect('Word_DB.sqlite') as conn:
        cursor = conn.cursor()

        definition = "--"
        example = "--"
        fluency = 0
        visited = 0

        # Bulk insert without locking the DB
        for word in words:
            #print(word)
            cursor.execute('''
            INSERT OR IGNORE INTO Words (word, definition, example, fluency, visited)
            VALUES (?, ?, ?, ?, ?)
            ''', (word, generate_def(word).lower(), example, fluency, visited))
        # Commit once at the end
        conn.commit()


def print_Words_db():
    conn = sqlite3.connect('Word_DB.sqlite')
    df = pd.read_sql('SELECT * FROM words', conn)
    print(df)
    conn.close()


def clear_Words_db():
    conn = sqlite3.connect("Word_DB.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM words")
    conn.commit()
    conn.close()

#google transalte definition/translation for each word
def generate_def(word): 
    try:
        # Use Google Translator to translate from French to English
        translation = GoogleTranslator(source='fr', target='en').translate(word)
        return translation
    except Exception as e:
        return f"Translation error: {e}"


def generate_exp():
    return 0


def create_pronunciation(sentence): 
    '''Creating the specifc pronunication for the word or sentence all are saved under their name in the pronucations folder
    - can change to just making the call each time (ex create, pronuncance, then delete on click each time)'''
    language = "fr"  # set to french
    # Generate audio with gTTS
    tts = gTTS(text=sentence, lang=language, slow=False)
    filename = "Pronunciations/"+(sentence)+".mp3"
    tts.save(filename)



def play_mp3(sentence):
    mp3_path = f"Pronunciations\{sentence}.mp3"

    if not os.path.exists(mp3_path):  
       print("MP3 file not found.") 
       return
    
    pygame.mixer.init()
    pygame.mixer.music.load(f"Pronunciations\{sentence}.mp3")
    pygame.mixer.music.play()
    
    print(f"Playing: {sentence}")

    # this might be required later so i'll keep it open like this
    while pygame.mixer.music.get_busy():  # Keep script running while music plays
        continue
    else:
        pygame.mixer.quit()  # closes it so less of a problem for other functions



def speak_new_sentence(sentence):
    create_pronunciation(sentence)
    play_mp3(sentence)
    #next to remove it from the file





# # Example usage:
# if __name__ == "__main__":
#     play_mp3("ami")

def clear_pronunciations_folder():
    folder_path =  "Pronunciations"

    # just to stop pygame if still running else error
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

# # Example usage:
# if __name__ == "__main__":
#     clear_pronunciations_folder()


def create_p_for_all(db_path):
    """Fetch and print all words under the 'word' category from the SQLite database."""
    db_path = "Word_DB.sqlite"
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to select all words
    query = "SELECT word FROM words"  # Adjust table name if different
    cursor.execute(query)

    # Fetch and print each word
    words = cursor.fetchall()
    for word in words:
        #print(word[0])  # Extract string from tuple
        create_pronunciation(word[0], )

    # Close the connection
    conn.close()

# # Example usage:
# if __name__ == "__main__":
#     create_p_for_all()  # Replace with the actual DB path