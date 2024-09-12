import os
import random
import tkinter as tk
from PIL import Image, ImageTk


def load_image(image_path):
    image = Image.open(image_path)
    return ImageTk.PhotoImage(image)


def display_image(image, canvas, x, y):
    canvas.create_image(x, y, anchor=tk.CENTER, image=image)



class FaceBlindnessGame:
    def __init__(self, image_directory, num_people=4, num_turns=10):
        self.image_directory = image_directory
        self.num_people = num_people
        self.num_turns = num_turns
        self.people = {}
        self.current_turn = 0
        self.correct_answers = 0

        self.load_images()
        self.create_game_window()

    def load_images(self):
        for filename in os.listdir(self.image_directory):
            person_name, index = filename.split('_')
            if person_name not in self.people:
                self.people[person_name] = []
            self.people[person_name].append(os.path.join(self.image_directory, filename))

    def create_game_window(self):
        self.root = tk.Tk()
        self.root.title("Face-Blindness Game")

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.label = tk.Label(self.root, text="Are these images of the same person?")
        self.label.pack()

        self.yes_button = tk.Button(self.root, text="Yes", command=self.check_answer(True))
        self.yes_button.pack(side=tk.LEFT)
        self.no_button = tk.Button(self.root, text="No", command=self.check_answer(False))
        self.no_button.pack(side=tk.RIGHT)

    def start_game(self):
        self.current_turn = 0
        self.correct_answers = 0
        self.show_images()

    def show_images(self):
        # Select two random images from different people
        people_to_show = random.sample(list(self.people.keys()), 2)
        image1 = random.choice(self.people[people_to_show[0]])
        image2 = random.choice(self.people[people_to_show[1]])

        # Load and display the images
        image1_tk = load_image(image1)
        image2_tk = load_image(image2)
        display_image(image1_tk, self.canvas, 200, 200)
        display_image(image2_tk, self.canvas, 600, 200)

    def check_answer(self, is_same):
        # Determine if the answer is correct
        people_to_show = random.sample(list(self.people.keys()), 2)
        is_correct = people_to_show[0] == people_to_show[1]
        if is_same == is_correct:
            self.correct_answers += 1

        # Provide feedback and move to the next turn
        if self.current_turn < self.num_turns - 1:
            self.current_turn += 1
            self.show_images()
        else:
            self.end_game()

    def end_game(self):
        # Display final score and exit
        self.label.config(text=f"Game over! You got {self.correct_answers} out of {self.num_turns} correct.")
        self.yes_button.pack_forget()
        self.no_button.pack_forget()


game = FaceBlindnessGame("images")
game.start_game()
game.root.mainloop()

