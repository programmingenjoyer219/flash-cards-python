from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_word = ""
# ----------------Button Functionality------------#
try:
    french_words = open(file="data/words_to_learn.csv", mode="r")
except FileNotFoundError:
    french_words = open(file="data/french_words.csv", mode="r")
data = pandas.read_csv(french_words)
data_list = data.to_dict(orient="records")
french_words_list = [word['French'] for word in data_list]
english_word_list = [word['English'] for word in data_list]
french_words.close()


def change_word():
    card_canvas.itemconfig(canvas_image, image=card_front_image)
    card_canvas.itemconfig(canvas_heading, text="French", fill="black")
    global current_word
    chosen_word = random.choice(french_words_list)
    current_word = chosen_word
    card_canvas.itemconfig(canvas_word, text=chosen_word, fill="black")
    window.after(3000, translate_word)


words_to_learn = data_list.copy()


def remove_word():
    print(f"Before: {len(words_to_learn)}")
    for word in words_to_learn:
        if word['French'] == current_word:
            words_to_learn.remove(word)
    print(f"After: {len(words_to_learn)}\n")
    pandas.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)
    change_word()


def translate_word():
    card_canvas.itemconfig(canvas_image, image=card_back_image)
    card_canvas.itemconfig(canvas_heading, text="English", fill="white")
    card_canvas.itemconfig(canvas_word, text=f"{english_word_list[french_words_list.index(current_word)]}",
                           fill="white")


# --------------------UI------------------#
window = Tk()
window.title("Widget Examples")
window.config(bg=BACKGROUND_COLOR)

window.after(3000, translate_word)

card_canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = card_canvas.create_image(400, 263, image=card_front_image)
canvas_heading = card_canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
canvas_word = card_canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2, padx=30, pady=30)

right_image = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=remove_word)
wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=change_word)
wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)

change_word()

window.mainloop()
