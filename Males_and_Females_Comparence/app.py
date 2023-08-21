import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


df= pd.read_csv("/content/student_data.csv")
st.title("COMPARENCE BETWEEN MALE AND FEMALE STUDENTS")

Analysis= st.checkbox("Show Analysis Of Whole Data")
Comparance= st.checkbox("Comparance Between Males and Females")






if Analysis:

      st.title("COMPARENCE BETWEEN MALE AND FEMALE STUDENTS(FULL ANALYSIS)")
      st.write("**Head of Dataset:** ", df.head())
      st.write("**DESCRIPTION of Dataset:** ", df.describe())
      st.write("**CHECK NULL VALUES:** ", df.isnull().sum())
      st.write("**CHECK DUPLICATED VALUES:** ", df.duplicated().sum())
##################################################################################################################################################################
      for column in df.columns:
        unique_values = df[column].unique()
        if unique_values.size > 0:
            st.write(column, "**has**", unique_values.size, "**unique values**")
        else:
            st.write(column, "**doesn't have any unique values**")
      for column in df.columns:
        st.write("**For**", column, "**Feature**")
        st.write(df[column].value_counts())
        st.write(df[column].value_counts().sum())
##################################################################################################################################################################
# Calculate the correlation matrix
      corr_matrix = df.corr()
# Create a heatmap of the correlation matrix
      fig = px.imshow(corr_matrix)
# Set the title and labels for the plot
      fig.update_layout(title="Correlation of Dataset")
# Show the plot
      st.plotly_chart(fig)
##################################################################################################################################################################
      for column in df.columns:
        unique_values = df[column].unique()
        if 0 < unique_values.size <= 5:
            counts = df[column].value_counts()

        # Create a pie chart with the counts
            fig1 = px.pie(counts, values=counts, names=counts.index, title=f"Pie chart of {column} feature")
        # Show the pie chart
            st.plotly_chart(fig1)

        # Create a bar chart with the counts
            fig2, ax2 = plt.subplots()
            ax2.bar(counts.index, counts)
            ax2.set_title(f"Bar chart of {column} feature")
            ax2.set_xlabel(column)
            ax2.set_ylabel("Counts")
        # Show the bar chart
            st.pyplot(fig2)
##################################################################################################################################################################
      df['Total_Grades'] = df['G1'] + df['G2'] + df['G3']

# Show the updated dataframe
      st.write("**After Adding Total Grades Column**")
      st.write(df)
##################################################################################################################################################################
# Create a histogram of the 'Total_Grades' column
      fig = px.histogram(df, x='Total_Grades', nbins=30, title="Distribution of Total Grades")

# Set the title and labels for the plot
      fig.update_layout(xaxis_title="Value", yaxis_title="Frequency")

# Show the plot
      st.plotly_chart(fig)
##################################################################################################################################################################
# Calculate the maximum, minimum, and average of the 'Total_Grades' column
      total_grades_max = df['Total_Grades'].max()
      total_grades_min = df['Total_Grades'].min()
      total_grades_mean = df['Total_Grades'].mean()

# Create a bar chart of the summary information
      fig = px.bar(x=['Maximum', 'Minimum', 'Average'], y=[total_grades_max, total_grades_min, total_grades_mean], labels={'x': 'Summary', 'y': 'Total Grades'}, title='Total Grades Summary')

# Show the chart
      st.plotly_chart(fig)
##################################################################################################################################################################
# Create an empty DataFrame to store the output
      output_df = pd.DataFrame(columns=['Student_ID', 'Number of Failures', 'Total Grades', 'Status'])

# Iterate over each row in the DataFrame and add rows to the output DataFrame based on the conditions
      for index, row in df.iterrows():
        if row['Total_Grades'] < df['Total_Grades'].mean() and row["failures"] == 0:
            output_df = pd.concat([output_df, pd.DataFrame({'Student_ID': [index], 'Number of Failures': [row['failures']],'Total Grades': row['Total_Grades'], 'Status': ["Fail but has second chance "]})],ignore_index=True)

        elif row['Total_Grades'] < df['Total_Grades'].mean() and row["failures"] == 1:
            output_df = pd.concat([output_df, pd.DataFrame({'Student_ID': [index], 'Number of Failures': [row['failures']],'Total Grades': row['Total_Grades'], 'Status': ["Fail for second time "]})], ignore_index=True)

        elif row['Total_Grades'] < df['Total_Grades'].mean() and row["failures"] == 2:
            output_df = pd.concat([output_df, pd.DataFrame({'Student_ID': [index], 'Number of Failures': [row['failures']],'Total Grades': row['Total_Grades'], 'Status': ["Fail for third time "]})], ignore_index=True)

        elif row['Total_Grades'] < df['Total_Grades'].mean() and row["failures"] == 3:
            output_df = pd.concat([output_df, pd.DataFrame({'Student_ID': [index], 'Number of Failures': [row['failures']],'Total Grades': row['Total_Grades'], 'Status': ["Fail and has no chance "]})], ignore_index=True)

        else:
            output_df = pd.concat([output_df, pd.DataFrame({'Student_ID': [index], 'Number of Failures': [row['failures']],'Total Grades': row['Total_Grades'], 'Status': ['Successful']})], ignore_index=True)

# Show the output DataFrame
      st.write(output_df.head(10))

#########################################################################################################################################################################################

# Count the number of male and female students who attended nursery school
      MN_counter = 0
      FN_counter=0

      for index, row in df.iterrows():
        if row['nursery'] == "yes" and row["sex"] == "M":
            MN_counter += 1
        elif row['nursery'] == "yes" and row["sex"] == "F":
            FN_counter += 1

      st.write("Number of male students who attended nursery school:", (MN_counter))
      st.write("Number of female students who attended nursery school:", (FN_counter))

# Create a DataFrame to store the counts
      data = pd.DataFrame({
        "nursery": ["Yes", "Yes"],
        "sex": ["M", "F"],
        "count": [MN_counter, FN_counter]
      })

      nursery_counts = df.groupby(['nursery', 'sex']).size().reset_index(name='count')

# Create a bar chart to display the counts
      fig = px.bar(nursery_counts, x='nursery', y='count', color='sex', barmode='group')

# Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Nursery Attendance and Gender", xaxis_title="Nursery Attendance", yaxis_title="Number of Students")

# Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################

# Count the number of male and female students who used or didn't use the internet
      MI_counter = 0
      FI_counter=0
      MNI_counter=0
      FNI_counter=0

      for index, row in df.iterrows():
          if row['internet'] == "yes" and row["sex"] == "M":
              MI_counter += 1
          elif row['internet'] == "yes" and row["sex"] == "F":
              FI_counter += 1
          elif row['internet'] == "no" and row["sex"] == "M":
              MNI_counter += 1
          elif row['internet'] == "no" and row["sex"] == "F":
              FNI_counter += 1

      st.write("Number of male students who used internet:", (MI_counter))
      st.write("Number of female students who used internet:", (FI_counter))
      st.write("Number of male students who didn't use internet:", (MNI_counter))
      st.write("Number of female students who didn't use internet:", (FNI_counter))

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "internet": ["Yes", "Yes", "No", "No"],
          "sex": ["M", "F", "M", "F"],
          "count": [MI_counter, FI_counter, MNI_counter, FNI_counter]
      })

      internet_counts = df.groupby(['internet', 'sex']).size().reset_index(name='count')

      # Create a bar chart to display the counts
      fig = px.bar(internet_counts, x='internet', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Internet Usage and Gender", xaxis_title="Internet Usage", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      MSS_counter = 0
      NMSS_counter=0
      FSS_counter=0
      NFSS_counter=0


      for index, row in df.iterrows():
          if row['schoolsup'] == "yes" and row["sex"] == "M":
              MSS_counter += 1
          elif row['schoolsup'] == "yes" and row["sex"] == "F":
              FSS_counter += 1
          elif row['schoolsup'] == "no" and row["sex"] == "M":
              NMSS_counter += 1
          elif row['schoolsup'] == "no" and row["sex"] == "F":
              NFSS_counter += 1


      st.write("Number of male students who had School Suppourt:", (MSS_counter))
      st.write("Number of male students who hadn't School Suppourt:", (NMSS_counter))
      st.write("Number of female students who had School Suppourt:", (FSS_counter))
      st.write("Number of female students who hadn't School Suppourt:", (NFSS_counter))



      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "schoolsup": ["Yes", "Yes", "No", "No"],
          "sex": ["M", "F", "M", "F"],
          "count": [MSS_counter, FSS_counter, NMSS_counter, NFSS_counter]
      })
      # Count the number of male and female students who had or didn't have school support
      schoolsup_counts = df.groupby(['schoolsup', 'sex']).size().reset_index(name='count')

      # Create a bar chart to display the counts
      fig = px.bar(schoolsup_counts, x='schoolsup', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by School Support and Gender", xaxis_title="School Support", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      # Count the number of male and female students who had or didn't have a romantic relationship
      RM_counter = 0
      NRM_counter = 0
      RF_counter = 0
      NRF_counter = 0

      for index, row in df.iterrows():
          if row['romantic'] == "yes" and row["sex"] == "M":
              RM_counter += 1
          elif row['romantic'] == "yes" and row["sex"] == "F":
              RF_counter += 1
          elif row['romantic'] == "no" and row["sex"] == "M":
              NRM_counter += 1
          elif row['romantic'] == "no" and row["sex"] == "F":
              NRF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "romantic": ["Yes", "Yes", "No", "No"],
          "sex": ["M", "F", "M", "F"],
          "count": [RM_counter, RF_counter, NRM_counter, NRF_counter]
      })

      st.write("Number of Romantic male students :", (RM_counter))
      st.write("Number of Non Romantic male students :", (NRM_counter))
      st.write("Number of Romantic female students :", (RF_counter))
      st.write("Number of Non Romantic female students :", (NRF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='romantic', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Romantic Relationship and Gender", xaxis_title="Romantic Relationship", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      # Count the number of male and female students who live in urban or rural areas
      UM_counter = 0
      RM_counter = 0
      UF_counter = 0
      RF_counter = 0

      for index, row in df.iterrows():
          if row['address'] == "U" and row["sex"] == "M":
              UM_counter += 1
          elif row['address'] == "U" and row["sex"] == "F":
              UF_counter += 1
          elif row['address'] == "R" and row["sex"] == "M":
              RM_counter += 1
          elif row['address'] == "R" and row["sex"] == "F":
              RF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "address": ["U", "U", "R", "R"],
          "sex": ["M", "F", "M", "F"],
          "count": [UM_counter, UF_counter, RM_counter, RF_counter]
      })

      st.write("Number of male students lives in Urban:", (UM_counter))
      st.write("Number of male students lives in Rural:", (RM_counter))
      st.write("Number of female students lives in Urban:", (UF_counter))
      st.write("Number of female students lives in Rural:", (RF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='address', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Address and Gender", xaxis_title="Address", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      # Count the number of male and female students in families of different sizes
      GM_counter = 0
      LM_counter = 0
      GF_counter = 0
      LF_counter = 0

      for index, row in df.iterrows():
          if row['famsize'] == "GT3" and row["sex"] == "M":
              GM_counter += 1
          elif row['famsize'] == "GT3" and row["sex"] == "F":
              GF_counter += 1
          elif row['famsize'] == "LE3" and row["sex"] == "M":
              LM_counter += 1
          elif row['famsize'] == "LE3" and row["sex"] == "F":
              LF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "famsize": ["GT3", "GT3", "LE3", "LE3"],
          "sex": ["M", "F", "M", "F"],
          "count": [GM_counter, GF_counter, LM_counter, LF_counter]
      })

      st.write("Number of male students that family size greater than 3:", (GM_counter))
      st.write("Number of male students that family size less than 3:", (LM_counter))
      st.write("Number of female students that family size greater than 3:", (GF_counter))
      st.write("Number of female students that family size less than 3:", (LF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='famsize', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Family Size and Gender", xaxis_title="Family Size", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      # Count the number of male and female students who participate in activities or not
      AM_counter = 0
      NAM_counter = 0
      AF_counter = 0
      NAF_counter = 0

      for index, row in df.iterrows():
          if row['activities'] == "yes" and row["sex"] == "M":
              AM_counter += 1
          elif row['activities'] == "yes" and row["sex"] == "F":
              AF_counter += 1
          elif row['activities'] == "no" and row["sex"] == "M":
              NAM_counter += 1
          elif row['activities'] == "no" and row["sex"] == "F":
              NAF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "activities": ["Yes", "Yes", "No", "No"],
          "sex": ["M", "F", "M", "F"],
          "count": [AM_counter, AF_counter, NAM_counter, NAF_counter]
      })

      st.write("Number of activity male students :", (AM_counter))
      st.write("Number of Non activity male students :", (NAM_counter))
      st.write("Number of activity female students :", (AF_counter))
      st.write("Number of Non activity female students :", (NAF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='activities', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Activities and Gender", xaxis_title="Activities", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)

#########################################################################################################################################################################################
      # Count the number of male and female students who live with parents or not
      AM_counter = 0
      TM_counter = 0
      AF_counter = 0
      TF_counter = 0

      for index, row in df.iterrows():
          if row['Pstatus'] == "A" and row["sex"] == "M":
              AM_counter += 1
          elif row['Pstatus'] == "A" and row["sex"] == "F":
              AF_counter += 1
          elif row['Pstatus'] == "T" and row["sex"] == "M":
              TM_counter += 1
          elif row['Pstatus'] == "T" and row["sex"] == "F":
              TF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "Pstatus": ["T", "T", "A", "A"],
          "sex": ["M", "F", "M", "F"],
          "count": [TM_counter, TF_counter, AM_counter, AF_counter]
      })

      st.write("Number of male students lives with parents:", (TM_counter))
      st.write("Number of male students doesn't live with parents:", (AM_counter))
      st.write("Number of female students lives with parents:", (TF_counter))
      st.write("Number of female students doesn't live with parents:", (AF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='Pstatus', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Parental Status and Gender", xaxis_title="Parental Status", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)
#########################################################################################################################################################################################
      # Count the number of male and female students who have family support or not
      FM_counter = 0
      NFM_counter = 0
      FF_counter = 0
      NFF_counter = 0

      for index, row in df.iterrows():
          if row['famsup'] == "yes" and row["sex"] == "M":
              FM_counter += 1
          elif row['famsup'] == "yes" and row["sex"] == "F":
              FF_counter += 1
          elif row['famsup'] == "no" and row["sex"] == "M":
              NFM_counter += 1
          elif row['famsup'] == "no" and row["sex"] == "F":
              NFF_counter += 1

      # Create a DataFrame to store the counts
      data = pd.DataFrame({
          "famsup": ["Yes", "Yes", "No", "No"],
          "sex": ["M", "F", "M", "F"],
          "count": [FM_counter, FF_counter, NFM_counter, NFF_counter]
      })

      st.write("Number of male students with family support :", (FM_counter))
      st.write("Number of male students without family support :", (NFM_counter))
      st.write("Number of female students with family support:", (FF_counter))
      st.write("Number of female students without family support:", (NFF_counter))

      # Create a bar chart to display the counts
      fig = px.bar(data, x='famsup', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
      fig.update_layout(title="Distribution of Students by Family Support and Gender", xaxis_title="Family Support", yaxis_title="Number of Students")

      # Show the plot
      st.plotly_chart(fig)

#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################
if Comparance:
    st.title("COMPARENCE")
    Numerical= st.checkbox("Numerical Comparance Only")
    Plots= st.checkbox("Comparance With Plots Only")
    Full= st.checkbox("Numerical Comparance and Plots")


    if Numerical:
            st.title("NUMERICAL COMPARENCE")
      # Count the number of male and female students who attended nursery school
            MN_counter = 0
            FN_counter=0

            for index, row in df.iterrows():
              if row['nursery'] == "yes" and row["sex"] == "M":
                  MN_counter += 1
              elif row['nursery'] == "yes" and row["sex"] == "F":
                  FN_counter += 1

            st.write("Number of male students who attended nursery school:", (MN_counter))
            st.write("Number of female students who attended nursery school:", (FN_counter))

      #########################################################################################################################################################################################

      # Count the number of male and female students who used or didn't use the internet
            MI_counter = 0
            FI_counter=0
            MNI_counter=0
            FNI_counter=0

            for index, row in df.iterrows():
                if row['internet'] == "yes" and row["sex"] == "M":
                    MI_counter += 1
                elif row['internet'] == "yes" and row["sex"] == "F":
                    FI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "M":
                    MNI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "F":
                    FNI_counter += 1

            st.write("Number of male students who used internet:", (MI_counter))
            st.write("Number of female students who used internet:", (FI_counter))
            st.write("Number of male students who didn't use internet:", (MNI_counter))
            st.write("Number of female students who didn't use internet:", (FNI_counter))


      #########################################################################################################################################################################################
            MSS_counter = 0
            NMSS_counter=0
            FSS_counter=0
            NFSS_counter=0


            for index, row in df.iterrows():
                if row['schoolsup'] == "yes" and row["sex"] == "M":
                    MSS_counter += 1
                elif row['schoolsup'] == "yes" and row["sex"] == "F":
                    FSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "M":
                    NMSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "F":
                    NFSS_counter += 1


            st.write("Number of male students who had School Suppourt:", (MSS_counter))
            st.write("Number of male students who hadn't School Suppourt:", (NMSS_counter))
            st.write("Number of female students who had School Suppourt:", (FSS_counter))
            st.write("Number of female students who hadn't School Suppourt:", (NFSS_counter))
      #########################################################################################################################################################################################
            # Count the number of male and female students who had or didn't have a romantic relationship
            RM_counter = 0
            NRM_counter = 0
            RF_counter = 0
            NRF_counter = 0

            for index, row in df.iterrows():
                if row['romantic'] == "yes" and row["sex"] == "M":
                    RM_counter += 1
                elif row['romantic'] == "yes" and row["sex"] == "F":
                    RF_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "M":
                    NRM_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "F":
                    NRF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "romantic": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [RM_counter, RF_counter, NRM_counter, NRF_counter]
            })

            st.write("Number of Romantic male students :", (RM_counter))
            st.write("Number of Non Romantic male students :", (NRM_counter))
            st.write("Number of Romantic female students :", (RF_counter))
            st.write("Number of Non Romantic female students :", (NRF_counter))
      #########################################################################################################################################################################################
            # Count the number of male and female students who live in urban or rural areas
            UM_counter = 0
            RM_counter = 0
            UF_counter = 0
            RF_counter = 0

            for index, row in df.iterrows():
                if row['address'] == "U" and row["sex"] == "M":
                    UM_counter += 1
                elif row['address'] == "U" and row["sex"] == "F":
                    UF_counter += 1
                elif row['address'] == "R" and row["sex"] == "M":
                    RM_counter += 1
                elif row['address'] == "R" and row["sex"] == "F":
                    RF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "address": ["U", "U", "R", "R"],
                "sex": ["M", "F", "M", "F"],
                "count": [UM_counter, UF_counter, RM_counter, RF_counter]
            })

            st.write("Number of male students lives in Urban:", (UM_counter))
            st.write("Number of male students lives in Rural:", (RM_counter))
            st.write("Number of female students lives in Urban:", (UF_counter))
            st.write("Number of female students lives in Rural:", (RF_counter))
      #########################################################################################################################################################################################
            # Count the number of male and female students in families of different sizes
            GM_counter = 0
            LM_counter = 0
            GF_counter = 0
            LF_counter = 0

            for index, row in df.iterrows():
                if row['famsize'] == "GT3" and row["sex"] == "M":
                    GM_counter += 1
                elif row['famsize'] == "GT3" and row["sex"] == "F":
                    GF_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "M":
                    LM_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "F":
                    LF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsize": ["GT3", "GT3", "LE3", "LE3"],
                "sex": ["M", "F", "M", "F"],
                "count": [GM_counter, GF_counter, LM_counter, LF_counter]
            })

            st.write("Number of male students that family size greater than 3:", (GM_counter))
            st.write("Number of male students that family size less than 3:", (LM_counter))
            st.write("Number of female students that family size greater than 3:", (GF_counter))
            st.write("Number of female students that family size less than 3:", (LF_counter))
      #########################################################################################################################################################################################
            # Count the number of male and female students who participate in activities or not
            AM_counter = 0
            NAM_counter = 0
            AF_counter = 0
            NAF_counter = 0

            for index, row in df.iterrows():
                if row['activities'] == "yes" and row["sex"] == "M":
                    AM_counter += 1
                elif row['activities'] == "yes" and row["sex"] == "F":
                    AF_counter += 1
                elif row['activities'] == "no" and row["sex"] == "M":
                    NAM_counter += 1
                elif row['activities'] == "no" and row["sex"] == "F":
                    NAF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "activities": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [AM_counter, AF_counter, NAM_counter, NAF_counter]
            })

            st.write("Number of activity male students :", (AM_counter))
            st.write("Number of Non activity male students :", (NAM_counter))
            st.write("Number of activity female students :", (AF_counter))
            st.write("Number of Non activity female students :", (NAF_counter))
      #########################################################################################################################################################################################
            # Count the number of male and female students who live with parents or not
            AM_counter = 0
            TM_counter = 0
            AF_counter = 0
            TF_counter = 0

            for index, row in df.iterrows():
                if row['Pstatus'] == "A" and row["sex"] == "M":
                    AM_counter += 1
                elif row['Pstatus'] == "A" and row["sex"] == "F":
                    AF_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "M":
                    TM_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "F":
                    TF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "Pstatus": ["T", "T", "A", "A"],
                "sex": ["M", "F", "M", "F"],
                "count": [TM_counter, TF_counter, AM_counter, AF_counter]
            })

            st.write("Number of male students lives with parents:", (TM_counter))
            st.write("Number of male students doesn't live with parents:", (AM_counter))
            st.write("Number of female students lives with parents:", (TF_counter))
            st.write("Number of female students doesn't live with parents:", (AF_counter))

      #########################################################################################################################################################################################
            # Count the number of male and female students who have family support or not
            FM_counter = 0
            NFM_counter = 0
            FF_counter = 0
            NFF_counter = 0

            for index, row in df.iterrows():
                if row['famsup'] == "yes" and row["sex"] == "M":
                    FM_counter += 1
                elif row['famsup'] == "yes" and row["sex"] == "F":
                    FF_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "M":
                    NFM_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "F":
                    NFF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsup": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [FM_counter, FF_counter, NFM_counter, NFF_counter]
            })

            st.write("Number of male students with family support :", (FM_counter))
            st.write("Number of male students without family support :", (NFM_counter))
            st.write("Number of female students with family support:", (FF_counter))
            st.write("Number of female students without family support:", (NFF_counter))

#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################

    if Plots:
            st.title("PLOTS OF COMPARENCE")
      # Count the number of male and female students who attended nursery school
            MN_counter = 0
            FN_counter=0

            for index, row in df.iterrows():
              if row['nursery'] == "yes" and row["sex"] == "M":
                  MN_counter += 1
              elif row['nursery'] == "yes" and row["sex"] == "F":
                  FN_counter += 1


      # Create a DataFrame to store the counts
            data = pd.DataFrame({
              "nursery": ["Yes", "Yes"],
              "sex": ["M", "F"],
              "count": [MN_counter, FN_counter]
            })

            nursery_counts = df.groupby(['nursery', 'sex']).size().reset_index(name='count')

      # Create a bar chart to display the counts
            fig = px.bar(nursery_counts, x='nursery', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Nursery Attendance and Gender", xaxis_title="Nursery Attendance", yaxis_title="Number of Students")

      # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################

      # Count the number of male and female students who used or didn't use the internet
            MI_counter = 0
            FI_counter=0
            MNI_counter=0
            FNI_counter=0

            for index, row in df.iterrows():
                if row['internet'] == "yes" and row["sex"] == "M":
                    MI_counter += 1
                elif row['internet'] == "yes" and row["sex"] == "F":
                    FI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "M":
                    MNI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "F":
                    FNI_counter += 1


            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "internet": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [MI_counter, FI_counter, MNI_counter, FNI_counter]
            })

            internet_counts = df.groupby(['internet', 'sex']).size().reset_index(name='count')

            # Create a bar chart to display the counts
            fig = px.bar(internet_counts, x='internet', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Internet Usage and Gender", xaxis_title="Internet Usage", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            MSS_counter = 0
            NMSS_counter=0
            FSS_counter=0
            NFSS_counter=0


            for index, row in df.iterrows():
                if row['schoolsup'] == "yes" and row["sex"] == "M":
                    MSS_counter += 1
                elif row['schoolsup'] == "yes" and row["sex"] == "F":
                    FSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "M":
                    NMSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "F":
                    NFSS_counter += 1



            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "schoolsup": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [MSS_counter, FSS_counter, NMSS_counter, NFSS_counter]
            })
            # Count the number of male and female students who had or didn't have school support
            schoolsup_counts = df.groupby(['schoolsup', 'sex']).size().reset_index(name='count')

            # Create a bar chart to display the counts
            fig = px.bar(schoolsup_counts, x='schoolsup', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by School Support and Gender", xaxis_title="School Support", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who had or didn't have a romantic relationship
            RM_counter = 0
            NRM_counter = 0
            RF_counter = 0
            NRF_counter = 0

            for index, row in df.iterrows():
                if row['romantic'] == "yes" and row["sex"] == "M":
                    RM_counter += 1
                elif row['romantic'] == "yes" and row["sex"] == "F":
                    RF_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "M":
                    NRM_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "F":
                    NRF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "romantic": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [RM_counter, RF_counter, NRM_counter, NRF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='romantic', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Romantic Relationship and Gender", xaxis_title="Romantic Relationship", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who live in urban or rural areas
            UM_counter = 0
            RM_counter = 0
            UF_counter = 0
            RF_counter = 0

            for index, row in df.iterrows():
                if row['address'] == "U" and row["sex"] == "M":
                    UM_counter += 1
                elif row['address'] == "U" and row["sex"] == "F":
                    UF_counter += 1
                elif row['address'] == "R" and row["sex"] == "M":
                    RM_counter += 1
                elif row['address'] == "R" and row["sex"] == "F":
                    RF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "address": ["U", "U", "R", "R"],
                "sex": ["M", "F", "M", "F"],
                "count": [UM_counter, UF_counter, RM_counter, RF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='address', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Address and Gender", xaxis_title="Address", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students in families of different sizes
            GM_counter = 0
            LM_counter = 0
            GF_counter = 0
            LF_counter = 0

            for index, row in df.iterrows():
                if row['famsize'] == "GT3" and row["sex"] == "M":
                    GM_counter += 1
                elif row['famsize'] == "GT3" and row["sex"] == "F":
                    GF_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "M":
                    LM_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "F":
                    LF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsize": ["GT3", "GT3", "LE3", "LE3"],
                "sex": ["M", "F", "M", "F"],
                "count": [GM_counter, GF_counter, LM_counter, LF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='famsize', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Family Size and Gender", xaxis_title="Family Size", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who participate in activities or not
            AM_counter = 0
            NAM_counter = 0
            AF_counter = 0
            NAF_counter = 0

            for index, row in df.iterrows():
                if row['activities'] == "yes" and row["sex"] == "M":
                    AM_counter += 1
                elif row['activities'] == "yes" and row["sex"] == "F":
                    AF_counter += 1
                elif row['activities'] == "no" and row["sex"] == "M":
                    NAM_counter += 1
                elif row['activities'] == "no" and row["sex"] == "F":
                    NAF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "activities": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [AM_counter, AF_counter, NAM_counter, NAF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='activities', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Activities and Gender", xaxis_title="Activities", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)

      #########################################################################################################################################################################################
            # Count the number of male and female students who live with parents or not
            AM_counter = 0
            TM_counter = 0
            AF_counter = 0
            TF_counter = 0

            for index, row in df.iterrows():
                if row['Pstatus'] == "A" and row["sex"] == "M":
                    AM_counter += 1
                elif row['Pstatus'] == "A" and row["sex"] == "F":
                    AF_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "M":
                    TM_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "F":
                    TF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "Pstatus": ["T", "T", "A", "A"],
                "sex": ["M", "F", "M", "F"],
                "count": [TM_counter, TF_counter, AM_counter, AF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='Pstatus', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Parental Status and Gender", xaxis_title="Parental Status", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who have family support or not
            FM_counter = 0
            NFM_counter = 0
            FF_counter = 0
            NFF_counter = 0

            for index, row in df.iterrows():
                if row['famsup'] == "yes" and row["sex"] == "M":
                    FM_counter += 1
                elif row['famsup'] == "yes" and row["sex"] == "F":
                    FF_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "M":
                    NFM_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "F":
                    NFF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsup": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [FM_counter, FF_counter, NFM_counter, NFF_counter]
            })


            # Create a bar chart to display the counts
            fig = px.bar(data, x='famsup', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Family Support and Gender", xaxis_title="Family Support", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)

#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################

    if Full:
            st.title("NUMERICAL AND PLOTS OF COMPARENCE")


      # Count the number of male and female students who attended nursery school
            MN_counter = 0
            FN_counter=0

            for index, row in df.iterrows():
              if row['nursery'] == "yes" and row["sex"] == "M":
                  MN_counter += 1
              elif row['nursery'] == "yes" and row["sex"] == "F":
                  FN_counter += 1

            st.write("Number of male students who attended nursery school:", (MN_counter))
            st.write("Number of female students who attended nursery school:", (FN_counter))

      # Create a DataFrame to store the counts
            data = pd.DataFrame({
              "nursery": ["Yes", "Yes"],
              "sex": ["M", "F"],
              "count": [MN_counter, FN_counter]
            })

            nursery_counts = df.groupby(['nursery', 'sex']).size().reset_index(name='count')

      # Create a bar chart to display the counts
            fig = px.bar(nursery_counts, x='nursery', y='count', color='sex', barmode='group')

      # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Nursery Attendance and Gender", xaxis_title="Nursery Attendance", yaxis_title="Number of Students")

      # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################

      # Count the number of male and female students who used or didn't use the internet
            MI_counter = 0
            FI_counter=0
            MNI_counter=0
            FNI_counter=0

            for index, row in df.iterrows():
                if row['internet'] == "yes" and row["sex"] == "M":
                    MI_counter += 1
                elif row['internet'] == "yes" and row["sex"] == "F":
                    FI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "M":
                    MNI_counter += 1
                elif row['internet'] == "no" and row["sex"] == "F":
                    FNI_counter += 1

            st.write("Number of male students who used internet:", (MI_counter))
            st.write("Number of female students who used internet:", (FI_counter))
            st.write("Number of male students who didn't use internet:", (MNI_counter))
            st.write("Number of female students who didn't use internet:", (FNI_counter))

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "internet": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [MI_counter, FI_counter, MNI_counter, FNI_counter]
            })

            internet_counts = df.groupby(['internet', 'sex']).size().reset_index(name='count')

            # Create a bar chart to display the counts
            fig = px.bar(internet_counts, x='internet', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Internet Usage and Gender", xaxis_title="Internet Usage", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            MSS_counter = 0
            NMSS_counter=0
            FSS_counter=0
            NFSS_counter=0


            for index, row in df.iterrows():
                if row['schoolsup'] == "yes" and row["sex"] == "M":
                    MSS_counter += 1
                elif row['schoolsup'] == "yes" and row["sex"] == "F":
                    FSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "M":
                    NMSS_counter += 1
                elif row['schoolsup'] == "no" and row["sex"] == "F":
                    NFSS_counter += 1


            st.write("Number of male students who had School Suppourt:", (MSS_counter))
            st.write("Number of male students who hadn't School Suppourt:", (NMSS_counter))
            st.write("Number of female students who had School Suppourt:", (FSS_counter))
            st.write("Number of female students who hadn't School Suppourt:", (NFSS_counter))



            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "schoolsup": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [MSS_counter, FSS_counter, NMSS_counter, NFSS_counter]
            })
            # Count the number of male and female students who had or didn't have school support
            schoolsup_counts = df.groupby(['schoolsup', 'sex']).size().reset_index(name='count')

            # Create a bar chart to display the counts
            fig = px.bar(schoolsup_counts, x='schoolsup', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by School Support and Gender", xaxis_title="School Support", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who had or didn't have a romantic relationship
            RM_counter = 0
            NRM_counter = 0
            RF_counter = 0
            NRF_counter = 0

            for index, row in df.iterrows():
                if row['romantic'] == "yes" and row["sex"] == "M":
                    RM_counter += 1
                elif row['romantic'] == "yes" and row["sex"] == "F":
                    RF_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "M":
                    NRM_counter += 1
                elif row['romantic'] == "no" and row["sex"] == "F":
                    NRF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "romantic": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [RM_counter, RF_counter, NRM_counter, NRF_counter]
            })

            st.write("Number of Romantic male students :", (RM_counter))
            st.write("Number of Non Romantic male students :", (NRM_counter))
            st.write("Number of Romantic female students :", (RF_counter))
            st.write("Number of Non Romantic female students :", (NRF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='romantic', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Romantic Relationship and Gender", xaxis_title="Romantic Relationship", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who live in urban or rural areas
            UM_counter = 0
            RM_counter = 0
            UF_counter = 0
            RF_counter = 0

            for index, row in df.iterrows():
                if row['address'] == "U" and row["sex"] == "M":
                    UM_counter += 1
                elif row['address'] == "U" and row["sex"] == "F":
                    UF_counter += 1
                elif row['address'] == "R" and row["sex"] == "M":
                    RM_counter += 1
                elif row['address'] == "R" and row["sex"] == "F":
                    RF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "address": ["U", "U", "R", "R"],
                "sex": ["M", "F", "M", "F"],
                "count": [UM_counter, UF_counter, RM_counter, RF_counter]
            })

            st.write("Number of male students lives in Urban:", (UM_counter))
            st.write("Number of male students lives in Rural:", (RM_counter))
            st.write("Number of female students lives in Urban:", (UF_counter))
            st.write("Number of female students lives in Rural:", (RF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='address', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Address and Gender", xaxis_title="Address", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students in families of different sizes
            GM_counter = 0
            LM_counter = 0
            GF_counter = 0
            LF_counter = 0

            for index, row in df.iterrows():
                if row['famsize'] == "GT3" and row["sex"] == "M":
                    GM_counter += 1
                elif row['famsize'] == "GT3" and row["sex"] == "F":
                    GF_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "M":
                    LM_counter += 1
                elif row['famsize'] == "LE3" and row["sex"] == "F":
                    LF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsize": ["GT3", "GT3", "LE3", "LE3"],
                "sex": ["M", "F", "M", "F"],
                "count": [GM_counter, GF_counter, LM_counter, LF_counter]
            })

            st.write("Number of male students that family size greater than 3:", (GM_counter))
            st.write("Number of male students that family size less than 3:", (LM_counter))
            st.write("Number of female students that family size greater than 3:", (GF_counter))
            st.write("Number of female students that family size less than 3:", (LF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='famsize', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Family Size and Gender", xaxis_title="Family Size", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who participate in activities or not
            AM_counter = 0
            NAM_counter = 0
            AF_counter = 0
            NAF_counter = 0

            for index, row in df.iterrows():
                if row['activities'] == "yes" and row["sex"] == "M":
                    AM_counter += 1
                elif row['activities'] == "yes" and row["sex"] == "F":
                    AF_counter += 1
                elif row['activities'] == "no" and row["sex"] == "M":
                    NAM_counter += 1
                elif row['activities'] == "no" and row["sex"] == "F":
                    NAF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "activities": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [AM_counter, AF_counter, NAM_counter, NAF_counter]
            })

            st.write("Number of activity male students :", (AM_counter))
            st.write("Number of Non activity male students :", (NAM_counter))
            st.write("Number of activity female students :", (AF_counter))
            st.write("Number of Non activity female students :", (NAF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='activities', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Activities and Gender", xaxis_title="Activities", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)

      #########################################################################################################################################################################################
            # Count the number of male and female students who live with parents or not
            AM_counter = 0
            TM_counter = 0
            AF_counter = 0
            TF_counter = 0

            for index, row in df.iterrows():
                if row['Pstatus'] == "A" and row["sex"] == "M":
                    AM_counter += 1
                elif row['Pstatus'] == "A" and row["sex"] == "F":
                    AF_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "M":
                    TM_counter += 1
                elif row['Pstatus'] == "T" and row["sex"] == "F":
                    TF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "Pstatus": ["T", "T", "A", "A"],
                "sex": ["M", "F", "M", "F"],
                "count": [TM_counter, TF_counter, AM_counter, AF_counter]
            })

            st.write("Number of male students lives with parents:", (TM_counter))
            st.write("Number of male students doesn't live with parents:", (AM_counter))
            st.write("Number of female students lives with parents:", (TF_counter))
            st.write("Number of female students doesn't live with parents:", (AF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='Pstatus', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Parental Status and Gender", xaxis_title="Parental Status", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)
      #########################################################################################################################################################################################
            # Count the number of male and female students who have family support or not
            FM_counter = 0
            NFM_counter = 0
            FF_counter = 0
            NFF_counter = 0

            for index, row in df.iterrows():
                if row['famsup'] == "yes" and row["sex"] == "M":
                    FM_counter += 1
                elif row['famsup'] == "yes" and row["sex"] == "F":
                    FF_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "M":
                    NFM_counter += 1
                elif row['famsup'] == "no" and row["sex"] == "F":
                    NFF_counter += 1

            # Create a DataFrame to store the counts
            data = pd.DataFrame({
                "famsup": ["Yes", "Yes", "No", "No"],
                "sex": ["M", "F", "M", "F"],
                "count": [FM_counter, FF_counter, NFM_counter, NFF_counter]
            })

            st.write("Number of male students with family support :", (FM_counter))
            st.write("Number of male students without family support :", (NFM_counter))
            st.write("Number of female students with family support:", (FF_counter))
            st.write("Number of female students without family support:", (NFF_counter))

            # Create a bar chart to display the counts
            fig = px.bar(data, x='famsup', y='count', color='sex', barmode='group')

            # Set the title and labels for the plot
            fig.update_layout(title="Distribution of Students by Family Support and Gender", xaxis_title="Family Support", yaxis_title="Number of Students")

            # Show the plot
            st.plotly_chart(fig)

#########################################################################################################################################################################################
