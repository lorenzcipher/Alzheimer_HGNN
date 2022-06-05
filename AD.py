# coding=utf-8
from doctest import master
import streamlit as st

import numpy as np
import pandas as pd


# Packages
from streamlit import caching
import time
import matplotlib.pyplot as plt

from simulate_data import simulate_data, simulate_labels
from sklearn import datasets
from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np

import pandas as pd
#from st_aggrid import AgGrid
import plotly.express as px
import io 
import warnings
warnings.filterwarnings("ignore")



def main():
    breast_cancer = datasets.load_breast_cancer(as_frame=True)
    breast_cancer_df = pd.concat((breast_cancer["data"], breast_cancer["target"]), axis=1)
    breast_cancer_df["target"] = [breast_cancer.target_names[val] for val in breast_cancer_df["target"]]
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
            data = pd.read_csv(uploaded_file)
            st.write(data)
        else:
            st.write('---') 
    elif selected == "Model":
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Alzheimer disease Dataset Analysis</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.", type=['csv'], key="2")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.write(data)
            ################# Scatter Chart Logic #################

            st.sidebar.markdown("### Scatter Chart: Explore Relationship Between Measurements :")

            measurements = breast_cancer_df.drop(labels=["target"], axis=1).columns.tolist()

            x_axis = st.sidebar.selectbox("X-Axis", measurements)
            y_axis = st.sidebar.selectbox("Y-Axis", measurements, index=1)

            if x_axis and y_axis:
                scatter_fig = plt.figure(figsize=(6,4))

                scatter_ax = scatter_fig.add_subplot(111)

                malignant_df = breast_cancer_df[breast_cancer_df["target"] == "malignant"]
                benign_df = breast_cancer_df[breast_cancer_df["target"] == "benign"]

                malignant_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="tomato", alpha=0.6, ax=scatter_ax, label="Malignant")
                benign_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="dodgerblue", alpha=0.6, ax=scatter_ax,
                                    title="{} vs {}".format(x_axis.capitalize(), y_axis.capitalize()), label="Benign");




            ########## Bar Chart Logic ##################

            st.sidebar.markdown("### Bar Chart: Average Measurements Per Tumor Type : ")

            avg_breast_cancer_df = breast_cancer_df.groupby("target").mean()
            bar_axis = st.sidebar.multiselect(label="Average Measures per Tumor Type Bar Chart",
                                            options=measurements,
                                            default=["mean radius","mean texture", "mean perimeter", "area error"])

            if bar_axis:
                bar_fig = plt.figure(figsize=(6,4))

                bar_ax = bar_fig.add_subplot(111)

                sub_avg_breast_cancer_df = avg_breast_cancer_df[bar_axis]

                sub_avg_breast_cancer_df.plot.bar(alpha=0.8, ax=bar_ax, title="Average Measurements per Tumor Type");

            else:
                bar_fig = plt.figure(figsize=(6,4))

                bar_ax = bar_fig.add_subplot(111)

                sub_avg_breast_cancer_df = avg_breast_cancer_df[["mean radius", "mean texture", "mean perimeter", "area error"]]

                sub_avg_breast_cancer_df.plot.bar(alpha=0.8, ax=bar_ax, title="Average Measurements per Tumor Type");

            ################# Histogram Logic ########################

            st.sidebar.markdown("### Histogram: Explore Distribution of Measurements : ")

            hist_axis = st.sidebar.multiselect(label="Histogram Ingredient", options=measurements, default=["mean radius", "mean texture"])
            bins = st.sidebar.radio(label="Bins :", options=[10,20,30,40,50], index=4)

            if hist_axis:
                hist_fig = plt.figure(figsize=(6,4))

                hist_ax = hist_fig.add_subplot(111)

                sub_breast_cancer_df = breast_cancer_df[hist_axis]

                sub_breast_cancer_df.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements");
            else:
                hist_fig = plt.figure(figsize=(6,4))

                hist_ax = hist_fig.add_subplot(111)

                sub_breast_cancer_df = breast_cancer_df[["mean radius", "mean texture"]]

                sub_breast_cancer_df.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements");

            #################### Hexbin Chart Logic ##################################

            st.sidebar.markdown("### Hexbin Chart: Explore Concentration of Measurements :")

            hexbin_x_axis = st.sidebar.selectbox("Hexbin-X-Axis", measurements, index=0)
            hexbin_y_axis = st.sidebar.selectbox("Hexbin-Y-Axis", measurements, index=1)

            if hexbin_x_axis and hexbin_y_axis:
                hexbin_fig = plt.figure(figsize=(6,4))

                hexbin_ax = hexbin_fig.add_subplot(111)

                breast_cancer_df.plot.hexbin(x=hexbin_x_axis, y=hexbin_y_axis,
                                            reduce_C_function=np.mean,
                                            gridsize=25,
                                            #cmap="Greens",
                                            ax=hexbin_ax, title="Concentration of Measurements");

            ##################### Layout Application ##################

            container1 = st.container()
            col1, col2 = st.columns(2)

            with container1:
                with col1:
                    scatter_fig
                with col2:
                    bar_fig


            container2 = st.container()
            col3, col4 = st.columns(2)

            with container2:
                with col3:
                    hist_fig
                with col4:
                    hexbin_fig



            



    
        

        
       
           
        
   


if __name__ == "__main__":
    main()


