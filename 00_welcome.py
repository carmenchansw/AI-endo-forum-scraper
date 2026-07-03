import streamlit as st
import os

st.title("Endometriosis Forum Insights, made for Malaysians")
st.header("How are you going to explore endometriosis?")

option_1, option_2, option_3, option_4 = st.columns(4)
if option_1.button("I want to self-diagnose endometriosis", width="stretch"): #include keyb shortcuts later
    st.write("You're not alone!")
if option_2.button("I want to support others by learning about endo myself.", width="stretch"):
    st.write("You're making a difference!")
if option_3.button("I am diagnosed with endometriosis but I want to navigate the Malaysian healthcare system. (Appointments, how to talk to doctors, etc.)", width="stretch"):
    st.write("Your voice matters!")
if option_4.button("I want to learn how to manage my endometriosis.", width="stretch"):
    st.write("You're not alone in this journey!")
