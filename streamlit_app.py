import streamlit as st
import time
import math

def calculate_reading_speed(start_time, end_time, word_count=300):
    reading_time = end_time - start_time
    words_per_minute = word_count / (reading_time / 60)
    return words_per_minute

def estimate_book_reading_time(pages, words_per_page, reading_speed):
    total_words = pages * words_per_page
    reading_time_minutes = total_words / reading_speed
    return reading_time_minutes

def calculate_finish_time(total_reading_time, minutes_per_session, days_per_week):
    minutes_per_week = minutes_per_session * days_per_week
    weeks_to_finish = total_reading_time / minutes_per_week
    return weeks_to_finish

def main():
    st.title("Let's calculate your reading speed")

    sample_text = """The rain pelted the narrow windows of the old apartment, the sound muffled by layers of grime that had long forgotten the touch of a rag. Camille sat at the small, worn-out kitchen table, her fingers tracing the edge of her coffee cup, now cold. Her thoughts churned with a familiar weight, the kind that crept up silently, coiling itself around her chest until breathing became an effort.
    She glanced at the clock. Nearly midnight. The ticking sound filled the room like a countdown, though she wasn't sure to what. Perhaps to the moment she'd finally allow herself to unravel, to admit that the silence in this room wasn't peaceful—it was suffocating.
    Across from her, the chair sat empty, a stark reminder of his absence. It had been weeks since he left, taking with him the scent of cigarette smoke and promises she once believed in. Yet, the memory of him lingered, like a shadow cast by a flame long extinguished. She hated herself for missing him, for feeling that hollow ache in her chest where his laugh used to echo.
    With a slow exhale, she pushed herself up from the chair and moved to the window, pressing her forehead against the cool glass. The city below, blurred by rain, seemed almost surreal, as if she were gazing at a painting of her life—distant, untouchable.
    "Why do I keep doing this to myself?" she whispered, her breath fogging the window. The question hung in the air, unanswered.
    The sky outside had darkened to a deep, impenetrable black, and the streetlights flickered in rhythm with the rain. Each drop on the glass felt like a tiny tap, a reminder of time slipping through her fingers, unnoticed. She closed her eyes, wondering when she had lost control of everything. Wondering if she'd ever get it back."""

    if 'reading' not in st.session_state:
        st.session_state.reading = False

    if not st.session_state.reading:
        if st.button("Start Reading"):
            st.session_state.reading = True
            st.session_state.start_time = time.time()
            st.rerun()

    if st.session_state.reading:
        st.write(sample_text)
        if st.button("I'm done"):
            end_time = time.time()
            reading_speed = calculate_reading_speed(st.session_state.start_time, end_time)
            st.session_state.reading = False
            st.session_state.reading_speed = reading_speed
            st.success(f"Your reading speed is approximately {reading_speed:.2f} words per minute.")
            st.rerun()

    if 'reading_speed' in st.session_state:
        st.subheader("Estimate reading time for your next book")
        pages = st.number_input("How many pages is your next book?", min_value=1, value=200)
        words_per_page = st.number_input("Estimated words per page", min_value=1, value=300)
        minutes_per_session = st.number_input("How many minutes do you want to read per session?", min_value=1, value=30)
        days_per_week = st.number_input("How many days per week do you want to read?", min_value=1, max_value=7, value=5)
        
        if st.button("Calculate Reading Time"):
            total_reading_time = estimate_book_reading_time(pages, words_per_page, st.session_state.reading_speed)
            weeks_to_finish = calculate_finish_time(total_reading_time, minutes_per_session, days_per_week)
            
            total_reading_hours = total_reading_time / 60  # Convert minutes to hours
            total_days = math.ceil(weeks_to_finish * 7)
            
            st.success(f"Based on your reading speed and schedule:")
            st.write(f"- It will take approximately {total_reading_hours:.1f} hours to read the entire book.")
            st.write(f"- Reading {minutes_per_session} minutes per session, {days_per_week} days per week:")
            
            if total_days <= 7:
                st.write(f"  You will finish the book in about {total_days} days.")
            else:
                weeks = int(weeks_to_finish)
                remaining_days = math.ceil((weeks_to_finish - weeks) * 7)
                st.write(f"  You will finish the book in about {weeks} weeks and {remaining_days} days.")
            
            st.write(f"  (Total of {total_days} days)")

if __name__ == "__main__":
    main()
