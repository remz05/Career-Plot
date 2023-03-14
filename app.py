import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
import plotly.graph_objs as go
import zipfile

def makePanel(df):
    """this function creates a row for each year a person has been on a job and creates a new column 't' which calculates the number of years it took to reach that job after mba graduation"""
    temp = pd.DataFrame({'T':range(1990,2018)})
    temp['joinCol'] = 1
    df['joinCol'] = 1
    D = pd.merge(df, temp, how='inner',on = 'joinCol')
    D = D[(D['T'] >= D['start']) & ((D['T'] <= D['end']) | (D['end'] == 0))]
    D['t'] = D['T'] - D['grad_year']
    D = D.sort_values(['id','t'])
    return D


def plot_peer_salary_path(dataframe ,user_input):
    # This function takes in as input characteristics of a person.
    # Then it filters the peer group.
    # Then plots the peer groups avg. performance over time.
    
    df = makePanel(dataframe)
    df = df[df['t'] <= 15]
    backup_df = df
    for k,v in user_input.items():
        if k != 'jobtitle' and v not in [None, "", 'select one', 'NaN','Type your response', 'type your response', 'Select one' ]:
            df = df[df[k] == v] 
    size = len(df)
    # Group by Data
    if len(df) < 10:
        print('Our training sample does not have enough values your specific profile but here is the most common career trajectory in the corporate world')
        df = pd.DataFrame(backup_df.groupby('t').agg({'jobSalary':['mean','std'],'jobtitle':lambda x: x.value_counts().index[0]}).reset_index()) 
        df.columns = ['t', 'js_mean', 'js_std', 'jobtitle_common']
    else:
        df = pd.DataFrame(df.groupby('t').agg({'jobSalary':['mean','std'],'jobtitle':lambda x: x.value_counts().index[0]}).reset_index())
        df.columns = ['t', 'js_mean', 'js_std', 'jobtitle_common']
    
    fig = go.Figure()

    # Add the mean line to the figure
    fig.add_trace(go.Scatter(x=df['t'], y=df['js_mean'], mode='lines', line=dict(color='#B6E880', dash='dash'), name='Mean Salary'))

    # Add the standard deviation fill to the figure
    fig.add_trace(go.Scatter(x=df['t'], y=df['js_mean'] - df['js_std'] * 0.5, mode='lines', line=dict(color='#FFA15A'), name='Standard Deviation'))
    fig.add_trace(go.Scatter(x=df['t'], y=df['js_mean'] + df['js_std'] * 0.5, mode='lines', line=dict(color='#FFA15A'), name='', showlegend=False, fill='tonexty'))

    for i, title in enumerate(df['jobtitle_common']):
        if (i % 3) == 0:
            fig.add_annotation(x= df['t'][i], y=df['js_mean'][i], text=title, font=dict(size=12), yshift=-6000, showarrow=False)

    # Add labels on the graph line at every third data point
    n = 3 # interval of labels
    for i in range(0, len(df), n):
        fig.add_annotation(x=df['t'][i], y=df['js_mean'][i], text=df['jobtitle_common'][i], font=dict(size=12), yshift=10, showarrow=False)

    # Add the "training sample does not have enough values" text as an annotation to the figure
    if size < 10:
        st.write(f':orange[Our training sample does not have enough values for your specific profile but here is the most common career trajectory across all profiles]')
        
    # Set the axis labels and title
    fig.update_layout(xaxis_title='Years from Graduation', yaxis_title='Salary')

    # Show the plotly figure in Streamlit
    st.plotly_chart(fig)
    
def app():
    st.set_page_config(layout="centered")
    
    image = Image.open('images/logo.jpeg')
    st.image(image)
    st.sidebar.title("CAREER PLOT")
    st.sidebar.markdown("Created by [Ramya Lather](https://www.linkedin.com/in/ramya-lather/)")
    active_tab = st.sidebar.radio("", ["Salary 💰", "Career Trajectory" , "Machine Learning behind Career Plot"])

    if active_tab == "Salary 💰":
        
        st.write(f'**:gray[Type in your job title and get a prediction of its salary as per market]**')
        job_title = st.text_input('Job Title  (eg: Analyst)')
        search_button = st.button("Search")
        if job_title:
            try:
                salary = int(df[df['clean_jobtitle'] == job_title.lower()]['jobSalary'].values)
                st.write(f'')
                message = f"<span style='font-size: 24px; color: #ADD8E6;'>The salary for {job_title} is ${salary}</span>"
                st.write(message, unsafe_allow_html=True)
                st.write(f'')
                st.write(f'')
                
            except TypeError:
                st.write(f'Sorry, the job title provided is very specific, request you to type a more general title.')  
         st.write(f'Career Plot aims to empower job seekers and employees by providing accurate and reliable information on salaries and compensation for different professions and industries. By leveraging the latest data analysis techniques and machine learning algorithms, we can help users make informed decisions about their career paths and negotiate fair compensation packages with their current or prospective employers.')
         st.write(f'Beyond salary the site provides user-friendly interface that allows users to input their personal and professional information to explore different career paths. Go to the **:blue[Career Trajectory]** page for more.')
         st.write(f'Ultimately, our goal is to help job seekers and employees make informed decisions about their careers and maximize their earning potential. We believe that by providing accurate and reliable salary information, we can help to level the playing field and promote greater transparency in the job market.')
         st.write(f'')      
            
           
        
    if active_tab == "Career Trajectory":
        st.write(f'**:gray[Curious about career trajectories of professionals with the same profile as you? Tell us more.]**')
        st.write(f'')
        st.write(f'The career graph changes as you type in more information about a profile. It is highly recommended to fill **:blue[Industry]** and **:blue[UG Specialization]** fields')
        industry_category = st.selectbox('Industry',( 'Select one', 'Computers', 'Entertainment', 'Retail', 'Finance', 'Management',
               'Engineering', 'Science', 'Healthcare', 'Legal', 'Electronics',
               'Art', 'Operations', 'Military', 'Analytics', 'Other'))
        st.write(f'')
        st.write(f'Undergraduate Education')
        col1, col2, col3 = st.columns(3)
        with col1:
            ug_school = st.text_input('UG School', placeholder= 'Type your response')
         
        with col2:
            ug_degree = st.selectbox('Specialisation',('Select one','Science', 'Arts', 'Business', 'Other'))
        
        with col3:
            ug_grad_year = st.text_input('Completion Year  (Format: YYYY)', placeholder= 'Type your response')
        st.write(f'') 
        st.write(f'Postgraduate Education')
        col1, col2 = st.columns([2,1])   
        with col1:
            mba_school = st.text_input('PG School  (eg: Harvard Business School)', placeholder= 'Type your response')
        with col2:
            grad_year = st.text_input('Completion Year  (Format: YYYY)', placeholder= 'Type your response')
            
            
            
        st.write(f'')
        experience = st.text_input('Years of work experience since your post-graduation  (Format: Integer)', placeholder= 'Type your response')
        st.write(f'')
        gender = st.selectbox('Gender',('Select one', 'Male', 'Female', 'Non-Binary'))

        user_input = ({'industry_category': industry_category.lower(), 'ug_school': ug_school.lower(), 'ug_degree': ug_degree.lower(), 'ug_grad_year': ug_grad_year, 'mba_school': mba_school.lower(), 'grad_year':grad_year, 'experience': experience, 'gender' : gender})


        if user_input:
            try:
                plot_peer_salary_path(df_graph, user_input)
                
            except TypeError:
                st.write(f'Fill in all details')
      
    if active_tab == "Machine Learning behind Career Plot":
        #st.markdown("The Machine Learning behind Career Plot")
        st.write("Below is the architecture behind Career Plot. Consider the job title text - “Associate ” entered by the user. Two set of features are extracted from this text. First, Google word to vec is used to derive 300 dimensional vector representation that captures semantic meaning of the job title text. Second, Page Rank on observed job switches is used to assign relative importance ranks to 1000 most common jobs. Then we use k nearest neighbour to extrapolate rank to all jobs.")
        st.write(f'')
        st.write("A combination of the semantic information in 300 dimensional vectors and order information in job rank will form the feature matrix of the ML random forest model. This predicts the salary for the user’s job role. Our database consists of salaries for more than 100,000 unique job titles. In addition to predicting salary for a job title, the tool also builds a career trajectory based on your profile.") 
        st.write(f'')
        image = Image.open('images/ml_architecture.jpeg')
        st.image(image)
       
    
    
    
if __name__ == '__main__':
    df = pd.read_csv('data/job_salary.csv')
    with zipfile.ZipFile('data/graph_data.csv.zip', 'r') as zip_ref:
        zip_ref.extractall('data/')
        
    df_graph = pd.read_csv('data/graph_data.csv')
    app()
