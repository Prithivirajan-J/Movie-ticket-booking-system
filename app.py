import streamlit as st
import sqlite3
import string
from database import init_db, add_user, authenticate_user, add_booking, get_bookings

# Sample movie data
movies = {
    "Inception": ["10:00 AM", "2:00 PM", "6:00 PM"],
    "Avengers: Endgame": ["11:00 AM", "3:00 PM", "7:00 PM"],
    "Interstellar": ["9:00 AM", "1:00 PM", "5:00 PM"]
}

# Initialize DB
init_db()

st.set_page_config(page_title="Movie Booking", layout="centered")
st.title("🎬 Movie Ticket Booking System")

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Login/Signup
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        st.subheader("Signup")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Signup"):
            if add_user(new_user, new_pass):
                st.success("Account created. Please login.")
            else:
                st.error("Username already taken.")

else:
    st.success(f"Logged in as: {st.session_state.username}")

    # Booking Section
    st.header("🎟 Book a Ticket")
    movie = st.selectbox("Choose a movie", list(movies.keys()))
    showtime = st.selectbox("Choose showtime", movies[movie])

    # Fetch already booked seats
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT seat FROM bookings WHERE movie = ? AND showtime = ?", (movie, showtime))
    booked_seats = [row[0] for row in c.fetchall()]
    conn.close()

    st.subheader("🎯 Select a Seat")
    selected_seat = None

    # Column labels
    cols = st.columns(6)
    cols[0].markdown("**Row\\Col**")
    for col_num in range(1, 6):
        cols[col_num].markdown(f"**{col_num}**")

    # Seat grid A1–E5
    for row in string.ascii_uppercase[:5]:  # A–E
        row_cols = st.columns(6)
        row_cols[0].markdown(f"**{row}**")
        for col in range(1, 6):
            seat_id = f"{row}{col}"
            if seat_id in booked_seats:
                row_cols[col].button(seat_id, disabled=True)
            else:
                if row_cols[col].button(seat_id):
                    selected_seat = seat_id

    if selected_seat:
        st.success(f"Selected Seat: {selected_seat}")
        if st.button("✅ Confirm Booking"):
            add_booking(st.session_state.username, movie, showtime, selected_seat)
            st.success(f"🎉 Booking Confirmed: {movie} at {showtime}, Seat {selected_seat}")
            st.experimental_rerun()

    # Display User Bookings
    st.markdown("---")
    st.subheader("📄 Your Bookings")
    for m, s, t in get_bookings(st.session_state.username):
        st.write(f"🎬 {m} | 🕓 {s} | 🪑 Seat: {t}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
