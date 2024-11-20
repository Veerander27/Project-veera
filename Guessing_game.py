import streamlit as st
import random
import math

def initialize_game():
    """Initialize or reset the game state."""
    st.session_state.machine_low = 1
    st.session_state.machine_high = 100
    st.session_state.machine_guess = None
    st.session_state.machine_number = random.randint(1, 100)
    st.session_state.user_number = None
    st.session_state.user_attempts = 0
    st.session_state.machine_attempts = 0
    st.session_state.game_over = False

def user_guess_machine():
    if not st.session_state.game_over:
        user_guess = st.number_input("Enter your guess (1-100):", min_value=1, max_value=100, step=1, key="user_guess")
        if st.button("Submit Your Guess", key="user_submit"):
            st.session_state.user_attempts += 1
            if user_guess == st.session_state.machine_number:
                st.success(f"🎉 You guessed the machine's number in {st.session_state.user_attempts} attempts!")
                st.session_state.game_over = True
            elif user_guess < st.session_state.machine_number:
                st.info("The machine's number is higher!")
            else:
                st.info("The machine's number is lower!")

def machine_guess_user():
    if st.session_state.user_number is None:
        st.session_state.user_number = st.number_input(
            "Pick a number for the machine to guess (hidden after confirmation):",
            min_value=1,
            max_value=100,
            step=1,
            key="pick_number",
        )
    confirm = st.button("Confirm Number", key="confirm_button")
    if confirm and not st.session_state.game_over:
        st.session_state.machine_guess = random.randint(
            st.session_state.machine_low, st.session_state.machine_high
        )
        st.subheader("Machine's Turn to Guess")
        if st.session_state.machine_guess is not None:
            st.write(f"The machine guesses: {st.session_state.machine_guess}")
            feedback = st.radio(
                "Provide feedback on the machine's guess:",
                ("Correct", "Too Low", "Too High"),
                key="feedback",
            )
            if feedback == "Correct":
                st.success(
                    f"🎉 The machine guessed your number in {st.session_state.machine_attempts + 1} attempts!"
                )
                st.session_state.game_over = True
            elif feedback == "Too Low":
                st.session_state.machine_low = st.session_state.machine_guess + 1
            elif feedback == "Too High":
                st.session_state.machine_high = st.session_state.machine_guess - 1
            st.session_state.machine_guess = math.floor(
                (st.session_state.machine_low + st.session_state.machine_high) / 2
            )
            st.session_state.machine_attempts += 1

st.title("Guessing Game: User vs. Machine")
st.write("Try to guess the machine's number while the machine guesses yours!")

if "machine_low" not in st.session_state:
    initialize_game()

st.subheader("Your Turn to Guess")
user_guess_machine()

st.subheader("Machine's Turn to Guess")
machine_guess_user()

if st.session_state.game_over:
    if st.button("Restart Game"):
        initialize_game()
