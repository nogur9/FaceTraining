import streamlit as st
import os
import random

def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            person_name = filename.split("_")[0]
            if person_name not in images:
                images[person_name] = []
            images[person_name].append(filename)
    return images

def choose_people(images, num_people, folder_path):
    people = random.sample(list(images.keys()), num_people)
    images = [os.path.join(folder_path, img) for person in people for img in images[person]]
    st.image(images, width=200)
    print("meow")


def main():
    st.title("Face-Blindness Training")

    folder_path = st.text_input("Enter the folder path containing the images:")
    num_people = st.number_input("Number of people to choose:", min_value=2, max_value=10)
    num_pairs = st.number_input("Number of image pairs to present:", min_value=1, max_value=10)

    images = load_images('images')
    choose_people(images, num_people, 'images')

if __name__ == "__main__":
    main()