import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['Cameron Jones', 'Ben Simmonds']
usernames = ['cameron.jones', 'ben.simmonds']
passwords = ['password', 'password']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)