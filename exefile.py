

'''This File is mostly a Copy and Paste of Main.ipynb it is condence into a file py file so an exe file can be made no new code is writen here'''






from funct import * # imports my blackbox

from langchain_community.utilities import SQLDatabase

# ollama is the AI we used
import ollama

client = ollama.Client()


db = SQLDatabase.from_uri("sqlite:///Word_DB.sqlite")

# 🔹 Step 2: Run the Query to Get Words
query = "SELECT word FROM words WHERE fluency = 5;"
result = db.run(query)


model="gemma3:4b" 

def sentence_gen(word):
    '''creates a simple example sentnece using the word provided as well as words from ones libary based on your fluceny level of them
    - sort by word only above fluency level 3.    or something. 
    '''

    # frist attempt is basic and will just return any sentence with word in it.
    prompt = f"Only return a very basic example of a French sentence that includes this french word: '{word}'. if possible try to use a word from this list that follows but ONLY if it makes sense else do not use any words in list: {result}"

    return (client.generate(model=model, prompt=prompt).response)#.split("</think>")[1][2:]


def create_example(word):
    '''Creates a setnence with knowelge of previous messages for the user to decode the message will take in info for words knowen'''

    prompt = f"Generate an easy french sentence that uses this french word: {word}. Make sure to return **ONLY** a sentence in french. If you can feel free to use other word from this list: {result}"

    return (client.generate(model=model, prompt=prompt).response)#.split("</think>")[1][2:]  # needs some level of randomization


def test_translation(french, response):

    prompt = f"Is this: {response}. a good english translation of this french sentence {french}? Return *only* 1 sentence saying Correct/A bit off/Incorrect if a but off explain what is missing. if its close enough just say correct."

    return (client.generate(model=model, prompt=prompt).response)#.split("</think>")[1][2:]  # needs some level of randomization



# this needs to be in this directly else it won't work on newly added mp3
def mp3_play(word):
    mp3_path = f"Pronunciations\{word}.mp3"

    if not os.path.exists(mp3_path):  
       print("MP3 file not found.") 
       return
    
    pygame.mixer.init()
    pygame.mixer.music.load(f"Pronunciations\{word}.mp3")
    pygame.mixer.music.play()
    
    print(f"Playing: {word}")

    # this might be required later so i'll keep it open like this
    while pygame.mixer.music.get_busy():  # Keep script running while music plays
        continue
    else:
        pygame.mixer.quit()  # closes it so less of a problem for other functions



import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Lang-app V0.2")

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (36, 71, 119)
COLOR_1 = (225, 173, 100)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 122, 204)
BLACK = (0, 0, 0)

# Font
font_t = pygame.font.Font(None, 55)
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)

# Game state
current_screen = "main"

#for phrase input section
input_box = pygame.Rect(50, 300, 350, 50)
input_text = ""
active = False

button_checker = pygame.Rect(50, 375, 125, 50)
button_text_checker = "Check"
generation_button_next = pygame.Rect(300, 375, 125, 50)
generation_button_next_text = "Again"

result_text = '--'

current_phrase = "-1"


 
# Button properties
button1_rect = pygame.Rect(100, 350, 300, 50)
button2_rect = pygame.Rect(100, 420, 300, 50)
button3_rect = pygame.Rect(100, 490, 300, 50)
function_button_rect = pygame.Rect(50, 200, 120, 50)
print_button_rect = pygame.Rect(50, 500, 120, 50)
next_w_button_rect = pygame.Rect(300, 500, 120, 50)
p_button_word_react = pygame.Rect(50, 270, 120, 50)
p_button_sent_react = pygame.Rect(300, 270, 120, 50)

back_button_r = pygame.Rect(300, 600, 120, 50)
back_button_p = pygame.Rect(10, 10, 120, 50)



def draw_main_screen():
    screen.fill(BACKGROUND)
    title_text = font_t.render("Cadmus Demo ", True, COLOR_1)
    screen.blit(title_text, (110, 100))
    
    pygame.draw.rect(screen, BLUE, button1_rect)
    pygame.draw.rect(screen, BLUE, button2_rect)
    pygame.draw.rect(screen, BLUE, button3_rect)
    
    screen.blit(button_font.render("Study", True, WHITE), button1_rect.move(50, 15))
    screen.blit(button_font.render("DO **NOT** CLICK HERE", True, WHITE), button2_rect.move(20, 15))
    screen.blit(button_font.render("Complete Phrases", True, WHITE), button3_rect.move(50, 15))

word_index = 0
val = 0 
current_phrase = 'base phrase, with some words but not that many'

def get_current_word():
    #global word_index
    return words[word_index]

function_output = ""

def function_action():
    global function_output
    function_output = sentence_gen(words[word_index].lower())

def card_display():
    word = get_current_word()
    global val
    if val == 0:
        return word
    else: 
        return word + " | " + generate_def(word)

def next_word():
    global word_index
    global function_output
    word_index = (word_index + 1) % len(words)
    function_output = ""

def gen_phrase():
    global word_index
    global current_phrase
    current_phrase = create_example(get_current_word())
    word_index += 1

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_surface = font.render(test_line, True, BLACK)
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word  # Start a new line with the current word
    
    if current_line:  # Append the last line
        lines.append(current_line)
    
    return lines

def draw_phrases_screen():
    font_n = pygame.font.Font(None, 30)
    screen.fill(BACKGROUND)
    word_box_rect = pygame.Rect(50, 75, 400, 200)
    pygame.draw.rect(screen, DARK_GRAY, word_box_rect, border_radius=10)

    max_width = word_box_rect.width - 20  # Padding inside the box
    y_offset = word_box_rect.y + 10  # Start inside the box with padding

    lines = wrap_text(current_phrase, font, max_width)

    # Render and blit each wrapped line
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (word_box_rect.x + 10, y_offset))
        y_offset += font.get_height()  # Move down for the next line

        # Draw input box
    pygame.draw.rect(screen, LIGHT_GRAY if active else DARK_GRAY, input_box, border_radius=5)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

    # Draw button 
    pygame.draw.rect(screen, BLUE, button_checker, border_radius=5)
    button_surface = font.render(button_text_checker, True, WHITE) 
    screen.blit(button_surface, (button_checker.x + 10, button_checker.y + 10)) 

    pygame.draw.rect(screen, BLUE, back_button_p, border_radius=5)
    button_surface = font.render("Home", True, WHITE) 
    screen.blit(button_surface, (back_button_p.x + 10, back_button_p.y + 10)) 

    pygame.draw.rect(screen, BLUE, generation_button_next, border_radius=5)
    button_surface = font.render(generation_button_next_text, True, WHITE) 
    screen.blit(button_surface, (generation_button_next.x + 10, generation_button_next.y + 10)) 

    # Draw result text
    #result_surface = font.render(result_text, True, BLACK)
    #screen.blit(result_surface, (50, 450))

    lines_2 = wrap_text(result_text, font_n, 400)
    y_offset = 450
    # Render and blit each wrapped line
    for line in lines_2:
        result_surface = font_n.render(line, True, COLOR_1)
        screen.blit(result_surface, (50, y_offset))
        y_offset += 35  # Move down for the next line   

def draw_review_screen():

    screen.fill(BACKGROUND)
    word_box_rect = pygame.Rect(100, 50, 300, 60)
    pygame.draw.rect(screen, DARK_GRAY, word_box_rect, border_radius=10)


  # Draw the word in the center of the box
    text_surface = font.render(card_display(), True, BLACK)
    text_rect = text_surface.get_rect(center=word_box_rect.center)
    screen.blit(text_surface, text_rect)

    
    
    pygame.draw.rect(screen, BLUE, function_button_rect)
    pygame.draw.rect(screen, BLUE, print_button_rect)
    pygame.draw.rect(screen, BLUE, next_w_button_rect)
    pygame.draw.rect(screen, BLUE, p_button_word_react)
    pygame.draw.rect(screen, BLUE, p_button_sent_react)
    pygame.draw.rect(screen, BLUE, back_button_r)
    
    screen.blit(button_font.render("Example", True, WHITE), function_button_rect.move(20, 15))
    screen.blit(button_font.render("English", True, WHITE), print_button_rect.move(35, 15))
    screen.blit(button_font.render("Next", True, WHITE), next_w_button_rect.move(35, 15))
    screen.blit(button_font.render("P_Word", True, WHITE), p_button_word_react.move(20, 15))
    screen.blit(button_font.render("P_Sen", True, WHITE), p_button_sent_react.move(20, 15))
    screen.blit(button_font.render("Home", True, WHITE), back_button_r.move(20, 15))

    output_surface = button_font.render((function_output.split(".")[0]).split("?")[0], True, BLACK)
    screen.blit(output_surface, (180, 215))

def generate_new_phrase():
    global word_index
    global current_phrase
    current_phrase = create_example(get_current_word())
    word_index += 1



def main():
    global current_phrase
    global current_screen
    global val
    global result_text
    global input_text
    running = True
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "main":
                    if button1_rect.collidepoint(event.pos):
                        current_screen = "review"
                    elif button2_rect.collidepoint(event.pos): # the "Do not press button"
                        pass  
                    elif button3_rect.collidepoint(event.pos):
                        gen_phrase()
                        current_screen = "phrases"
                if current_screen == "review":
                    active = False
                    if function_button_rect.collidepoint(event.pos):
                        function_action()
                    elif p_button_word_react.collidepoint(event.pos):
                        mp3_play(get_current_word())
                    elif p_button_sent_react.collidepoint(event.pos):
                        create_pronunciation(function_output.split(".")[0])
                        mp3_play(function_output.split(".")[0])
                    elif print_button_rect.collidepoint(event.pos):
                        val = 1
                    elif next_w_button_rect.collidepoint(event.pos):
                        val = 0
                        next_word()
                    elif back_button_r.collidepoint(event.pos):
                        current_screen = "main"
                if current_screen == "phrases":
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    if button_checker.collidepoint(event.pos): 
                        result_text = test_translation(current_phrase, (input_text.lower().strip()))
                        # if input_text.lower().strip() == "please":
                        #     result_text = "You Pass-- will change to global var from func call"
                        # else:
                        #     result_text = "i guess call again but will leave to test"
                    if generation_button_next.collidepoint(event.pos): 
                        generate_new_phrase()
                    if back_button_p.collidepoint(event.pos):
                        current_screen = "main"

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        result_text = test_translation(current_phrase, (input_text.lower().strip()))
                        #else:
                        #    result_text = "Not the magic word"
                        input_text = ""  # Clear input
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Remove last character
                    else:
                        input_text += event.unicode  # Add new character
                                
                        

                        
                
        if current_screen == "main":
            draw_main_screen()
        elif current_screen == "review":
            draw_review_screen()
        elif current_screen == "phrases":
            draw_phrases_screen()
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()