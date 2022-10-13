from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
word = {}
to_learn = {}
# ----------------------------  DEFINE FUNCTIONS  ------------------------------- #


def rand_word():
    french = random.choice(french_dictionary)
    return french


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = rand_word()
    in_french_word = word['French']
    canvas.itemconfig(canvas_image, image=front_of_flashcard)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(french_word, text=in_french_word, fill='black')
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global word
    in_english_word = word['English']
    canvas.itemconfig(canvas_image, image=back_of_flashcard)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(french_word, text=in_english_word, fill='white')


def is_known():
    french_dictionary.remove(word)
    data = pd.DataFrame(french_dictionary)
    data.to_csv('data/words_to_learn.csv', index=False)
    print(len(french_dictionary))
    next_card()



def right():
    next_card()


def wrong():
    next_card()


# ---------------------------- TURN TO DICTIONARY ------------------------------- #
try:
    data = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('./data/french_words.csv')
    french_dictionary = original_data.to_dict(orient='records')
else:
    french_dictionary = data.to_dict(orient='records')


# ---------------------------- UI ------------------------------- #

# Window
window = Tk()
window.title('Flashy')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

# Flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_of_flashcard = PhotoImage(file='./images/card_front.png')
back_of_flashcard = PhotoImage(file='./images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=front_of_flashcard)
card_title = canvas.create_text(400, 150, text='French', fill='black', font=('Ariel', 40, 'italic'))
french_word = canvas.create_text(400, 263, text='', fill='black', font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

# X Button
x_image = PhotoImage(file='./images/wrong.png')
x_button = Button(image=x_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=wrong)
x_button.grid(column=0, row=1)

# Y Button
y_image = PhotoImage(file='./images/right.png')
y_button = Button(image=y_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=is_known)
y_button.grid(column=1, row=1)

flip_timer = window.after(3000, flip_card)
next_card()


window.mainloop()
