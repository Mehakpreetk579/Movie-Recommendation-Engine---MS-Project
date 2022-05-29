import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["User1", "User2"]
usernames = ["u1", "u2"]
passwords = ["abc123", "def456"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
    