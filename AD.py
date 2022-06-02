# coding=utf-8
from doctest import master
import streamlit as st

import numpy as np
import pandas as pd


# Packages
from streamlit import caching
import time
pip install streamlit-option-menu

from simulate_data import simulate_data, simulate_labels

from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 



def main():
    with st.sidebar:
        selected = option_menu("Menu", ["Home",'Visualization fMRI','Morphological Data','Model','Statistics', 'Settings'], 
            icons=['house','eye','kanban','sliders','activity','gear'], default_index=0)

    
    logo = Image.open(r'C:\Users\FATEH\Downloads\HCAE-master\HCAE-master\Brain-Logo.png')
    profile = Image.open(r'C:\Users\FATEH\Downloads\HCAE-master\HCAE-master\image_bg.jpg')


    if selected == "Home":
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">About Our Project</p>', unsafe_allow_html=True)    
        with col2:               # To display brand log
            st.image(logo, width=130 )
        
        
        st.write('''Of all the medical data, images are the most important in terms of volume of data, information exploited and knowledge extracted. Medical imaging makes it possible to visualize the inside of a human (or animal) body without surgery. It is used for clinical purposes, i.e. in the search for a diagnosis or a treatment of certain pathologies, but also for scientific research in order to study the reactions of the body of the living being in front of diseases (Cancer, Autism, Alzheimer's, etc.) which have recently preoccupied doctors and researchers in the medical field.
        \n The systematic production of digitized medical data means that computer analysis and synthesis have developed very dramatically over the last twenty years, leading to the automation of the diagnosis of various diseases and numerous studies requiring multiple medical image processing. Thus, computer tools have become indispensable, even unavoidable, in the face of this data structure.
        \n Among the many challenges that imaging can exploit in medical research is Alzheimer's disease, the most common form of dementia.
        \n ''')
        st.image(profile, width=400) 
        st.write("Alzheimer's disease is a neurodegenerative brain disorder for which there is currently no cure. Early diagnosis of this disease by Deep Learning applied to functional magnetic resonance imaging (fMRI) of the brain and specifically by convolutional neural networks (CNN), is attracting increasing interest due to their high performance in classification, detection and segmentation in medical imaging.")   
        
    elif selected == "Visualization fMRI":
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Upload fMRI data...</p>', unsafe_allow_html=True)
            
        with col2:               # To display brand logo
            st.image(logo,  width=150)
        #Add file uploader to allow users to upload photos
        uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            #col1, col2 = st.columns( [0.5, 0.5])
            #with col1:
                #st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=500)  
    elif selected == "Morphological Data":
        #Add a file uploader to allow users to upload their project plan file
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Upload your project plan</p>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.", type=['csv'], key="2")
        if uploaded_file is not None:
            Tasks=pd.read_csv(uploaded_file)
            Tasks['Start'] = Tasks['Start'].astype('datetime64')
            Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
            
            grid_response = AgGrid(
                Tasks,
                editable=True, 
                height=300, 
                width='100%',
                )

            updated = grid_response['data']
            df = pd.DataFrame(updated) 
            
            if st.button('Generate Gantt Chart'): 
                fig = px.timeline(
                                df, 
                                x_start="Start", 
                                x_end="Finish", 
                                y="Task",
                                color='Completion Pct',
                                hover_name="Task Description"
                                )

                fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
                
                fig.update_layout(
                                title='Project Plan Gantt Chart',
                                hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                                bargap=0.2,
                                height=600,              
                                xaxis_title="", 
                                yaxis_title="",                   
                                title_x=0.5,                    #Make title centered                     
                                xaxis=dict(
                                        tickfont_size=15,
                                        tickangle = 0,
                                        rangeslider_visible=True,
                                        side ="top",            #Place the tick labels on the top of the chart
                                        showgrid = True,
                                        zeroline = True,
                                        showline = True,
                                        showticklabels = True,
                                        tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                        )
                            )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('---') 

            



    
        

        
       
           
        
   


if __name__ == "__main__":
    main()


