from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import os
import random

class ABC:

    def __init__(self, image_directory, num_people=4, num_turns=10):
        self.image_directory = image_directory
        self.num_people = num_people
        self.num_turns = num_turns
        self.people = {}
        self.current_turn = 0
        self.correct_answers = 0
        self.root = Tk()
        canvas = Canvas(self.root, width=800, height=500)
        canvas.pack()
        self.canvas = canvas

        self.root.title("Face-Blindness Game")

        self.label = tk.Label(self.root, text="Are these images of the same person?")
        self.label.pack()

        self.yes_button = tk.Button(self.root, text="Yes")#, command=self.check_answer(True))
        self.yes_button.pack(side=tk.LEFT)
        self.no_button = tk.Button(self.root, text="No")##, command=self.check_answer(False))
        self.no_button.pack(side=tk.RIGHT)

        self.load_images()
        self.meow()

    def check_answer(self, is_same):
        # Determine if the answer is correct
        people_to_show = random.sample(list(self.people.keys()), 2)
        is_correct = people_to_show[0] == people_to_show[1]
        if is_same == is_correct:
            self.correct_answers += 1

        # Provide feedback and move to the next turn
        if self.current_turn < self.num_turns - 1:
            self.current_turn += 1
            self.meow()
        else:
            self.end_game()

    def end_game(self):
        # Display final score and exit
        self.label.config(text=f"Game over! You got {self.correct_answers} out of {self.num_turns} correct.")
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

    def load_images(self):
        for filename in os.listdir(self.image_directory):
            person_name, index = filename.split('_')
            if person_name not in self.people:
                self.people[person_name] = []
            self.people[person_name].append(os.path.join(self.image_directory, filename))


    def meow(self):
        people_to_show = random.sample(list(self.people.keys()), 2)
        image1 = random.choice(self.people[people_to_show[0]])
        image2 = random.choice(self.people[people_to_show[0]])
        newsize = (300, 300)
        im1 = Image.open(image1)
        im1 = im1.resize(newsize)
        img = ImageTk.PhotoImage(im1)

        self.canvas.create_image(200, 200,  image=img)

        im2 = Image.open(image2)
        im2 = im2.resize(newsize)
        img2 = ImageTk.PhotoImage(im2)
        self.canvas.create_image(600, 200, image=img2)
        self.root.mainloop()


abc = ABC('images')
