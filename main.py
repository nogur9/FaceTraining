from time import sleep

import streamlit as st
import os
import random
import pandas as pd


class PersonsImage:
    """Represents an image of a person with a name."""

    def __init__(self, image_path, person_name):
        self.image_path = image_path
        self.person_name = person_name


class Game:
    """Handles the logic of loading images and selecting people for the game."""

    INFO_FILE_PATH = "info.csv"

    def __init__(self, folder_path: str, num_people: int, random_seed: int, past_people=None, people=None):
        random.seed(random_seed)
        self.folder_path = folder_path
        self.past_people = past_people or []
        self.images = self._load_images()
        self.people = people or self._select_people(num_people)

    def _load_images(self):
        """Loads images from the folder and organizes them by person name."""
        images = {}
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".jpg"):
                person_name = filename.split("_")[0]
                if person_name in self.past_people:
                    continue
                images.setdefault(person_name, []).append(filename)
        return images

    def _select_people(self, num_people: int):
        """Selects a random person and valid matches for the game."""
        first_person = random.choice(list(self.images.keys()))
        valid_choices = self._get_valid_people(first_person)
        other_people = random.sample(valid_choices, num_people - 1)
        return [first_person] + other_people

    def _get_valid_people(self, first_person: str):
        """Finds people with matching attributes for the game."""
        info = pd.read_csv(self.INFO_FILE_PATH)
        person_info = info[info.name == first_person].iloc[0]
        valid_people = info[
            (info.color == person_info['color']) &
            (info.gender == person_info['gender']) &
            (info.hair == person_info['hair'])
            ]['name'].tolist()
        valid_people.remove(first_person)
        return valid_people

    def get_random_images(self):
        """Returns two random images for the game."""
        images = [
            PersonsImage(os.path.join(self.folder_path, img), person)
            for person in self.people
            for img in self.images[person]
        ]
        return random.sample(images, 2)


def initialize_game_state():
    """Initializes game-related variables in session state."""
    if 'random_seed' not in st.session_state:
        st.session_state.random_seed = 67
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game' not in st.session_state:
        st.session_state.game = Game('images', 2, st.session_state.random_seed)
        st.session_state.people = st.session_state.game.people
    if 'current_images' not in st.session_state:
        st.session_state.current_images = st.session_state.game.get_random_images()
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'total_steps' not in st.session_state:
        st.session_state.total_steps = 0


def display_images():
    """Displays two images side by side for the user to compare."""
    col1, col2 = st.columns(2)
    images = [img.image_path for img in st.session_state.current_images]

    with col1:
        st.image(images[0], width=200)
    with col2:
        st.image(images[1], width=200)


def update_score(user_choice: str):
    """Updates the score based on the user's choice."""
    people_names = [img.person_name for img in st.session_state.current_images]
    correct_answer = "Yes" if people_names[0] == people_names[1] else "No"

    if user_choice == correct_answer:
        st.session_state.score += 1
        st.write("**:green[Correct!]** Score increased.  :smile:")
    else:
        st.write("**:red[Incorrect!]**   :confused:")


def reset_game():
    """Resets the game after 5 steps."""
    if st.session_state.step >= 5:
        st.session_state.step = 0
        st.session_state.score = 0
        st.session_state.random_seed = random.randint(10000, 100000)
        st.session_state.game = Game('images', 2, st.session_state.random_seed)
        st.session_state.people = st.session_state.game.people
        st.session_state.current_images = st.session_state.game.get_random_images()
        st.rerun()


def submit(user_choice: str):
    st.session_state.step += 1
    st.session_state.total_steps += 1
    print(f"{st.session_state.step = }")
    update_score(user_choice)

    reset_game()

    # Update game state
    st.session_state.random_seed = random.randint(0, 10000)
    st.session_state.game = Game('images', 2, st.session_state.random_seed, people=st.session_state.people)
    st.session_state.current_images = st.session_state.game.get_random_images()


def main():
    st.title("Face-Blindness Training")

    # Initialize session state
    initialize_game_state()
    if st.session_state.total_steps <= 20:
        # Display images and collect user input
        display_images()
        user_choice = st.radio("Are these images of the same person?", options=["Yes", "No"])
        if st.button("Submit"):
            submit(user_choice)
            sleep(2)
            st.rerun()

    else:
        st.write(f"Done :smiley: :heart:")

    st.write(f"Score: {st.session_state.score} /\nout of {st.session_state.total_steps}")


if __name__ == "__main__":
    main()
