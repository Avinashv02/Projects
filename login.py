import streamlit as st
import streamlit_authenticator as stauth

# Configuring the authenticator
names = ["Avinash Verma"]
usernames = ["avinash"]
emails = ["avinash@example.com"]

# Hash your passwords using the Hasher
passwords = ['password123']
hashed_passwords = stauth.Hasher(passwords).generate()  # Correct usage

# Authenticator object
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "my_app_cookie",
    "random_key",
    cookie_expiry_days=1
)

def main():
    st.title("Login Page")
    
    # Login block
    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.success(f"Welcome {name}")
        # Redirect to `app.py` by setting a query parameter
        st.experimental_set_query_params(logged_in="true")
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=app.py">',
            unsafe_allow_html=True,
        )  # Redirect to app.py
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

if __name__ == "__main__":
    main()
