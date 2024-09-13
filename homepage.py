import streamlit as st
from app import app

def homepage():
    st.set_page_config(layout="wide", page_title="SignWave")
    st.markdown(
        '''
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .top-bar {
                background-color: #a76ee9;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: white;
            }
            .top-bar svg {
                width: 30px;
                height: 30px;
                fill: white;
            }
            .top-bar div {
                display: flex;
                align-items: center;
            }
            .top-bar a {
                color: white;
                text-decoration: none;
                margin-right: 15px;
                font-size: 18px;
            }
            .top-bar a i {
                margin-right: 5px;
            }
        </style>
        <div class="top-bar">
            <div style="font-size: 50px;text-align: center;font-weight: bold">Sign Wave</div>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802" />
            </svg>
        </div>
        ''', unsafe_allow_html=True
    )
    with st.columns(3)[1]:
     st.image("topimg.png", width=175)

    st.markdown(
        '''
        <style>
        .fade-in
        {
        opacity: 0;
        animation: fadeIn 6s forwards;
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
            }
        }

        </style>
        <div>
            <h1 class="fade-in" style="text-align: center;">Welcome To Signwave</h1>
            <p style="color:#b58de4;align:center;font-size:35px">Please click here for Video to ISL:</p>
        </div>
        ''', unsafe_allow_html=True
    )
    # st.image("logo_signwave.jpg", width=100)
    if st.button(":rainbow[Click Me]"):
        app()


homepage()
