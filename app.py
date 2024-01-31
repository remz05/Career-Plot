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
    active_tab = st.sidebar.radio("", ["Salary 💰", "Career Trajectory" , "Machine Learning behind Career Plot", "Know more about Career Plot"])
    st.sidebar.write("""
            ## About
            
            Career Plot aims to empower job seekers and employees by providing accurate and reliable information on salaries for different professions and industries. By leveraging the latest data analysis techniques and machine learning algorithms, we can help users make informed decisions about their career paths.
            
            Contact me [here](mailto:ramyalather@gmail.com) or consider contributing to the [GitHub](https://github.com/remz05/Career-Plot) repository with any suggestions or questions. 
        """)
    if active_tab == "Salary 💰":
        
        st.write(f'**:gray[Type in your job title and get a prediction of its salary as per market]**')
        job_title = st.text_input('Job Title  (eg: Analyst)')
        search_button = st.button("Search")
        if job_title:
            try:
                salary = int(df[df['clean_jobtitle'] == job_title.lower()]['jobSalary'].values)
                #st.write(f'')
                message = f"<span style='font-size: 24px; color: #ADD8E6;'>The salary for {job_title} is ${salary}</span>"
                st.write(message, unsafe_allow_html=True)
                #st.write(f'')
                #st.write(f'')
                st.write(f'Beyond salary the site provides user-friendly interface that allows users to input their personal and professional information to explore different career paths. Go to the **:blue[Career Trajectory]** page in the left sidebar for more.')
                
            except TypeError:
                st.write(f'Sorry, the job title provided is very specific, request you to type a more general title.')  
        

            
           
        
    if active_tab == "Career Trajectory":
        user_input = ({'industry_category': 'finance', 'ug_school': 'the ohio state university', 'ug_degree': 'science', 'ug_grad_year': '2009', 'mba_school': 'georgia state university', 'grad_year':'2012', 'experience': '3', 'gender': 'male'})
        plot_peer_salary_path(df_graph, user_input)
    #     st.write(f'**:gray[Curious about career trajectories of professionals with the same profile as you? Tell us more.]**')
    #     #st.write(f'')
    #     st.write(f'The career graph changes as you type in more information about a profile. It is highly recommended to fill **:blue[Industry]** and **:blue[UG Specialization]** fields')
    #     industry_category = st.selectbox('Industry',( 'Select one', 'Computers', 'Entertainment', 'Retail', 'Finance', 'Management',
    #            'Engineering', 'Science', 'Healthcare', 'Legal', 'Electronics',
    #            'Art', 'Operations', 'Military', 'Analytics', 'Other'))
    #     #st.write(f'')
    #     st.write(f'Undergraduate Education')
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         ug_school = st.text_input('UG School', placeholder= 'Type your response')
         
    #     with col2:
    #         ug_degree = st.selectbox('Specialisation',('Select one','Science', 'Arts', 'Business', 'Other'))
        
    #     with col3:
    #         ug_grad_year = st.text_input('Completion Year  (Format: YYYY)', key='grad_year_input', placeholder= 'Type your response')
    #     #st.write(f'') 
    #     st.write(f'Postgraduate Education')
    #     col1, col2 = st.columns([2,1])   
    #     with col1:
    #         mba_school = st.text_input('PG School  (eg: Harvard Business School)', placeholder= 'Type your response')
    #     with col2:
    #         grad_year = st.text_input('Completion Year (Format: YYYY)', key='post_grad_year_input', placeholder= 'Type your response')
            
            
            
    #     #st.write(f'')
    #     experience = st.text_input('Years of work experience since your post-graduation  (Format: Integer)', placeholder= 'Type your response')
    #     #st.write(f'')
    #     gender = st.selectbox('Gender',('Select one', 'Male', 'Female', 'Non-Binary'))

    #     user_input = ({'industry_category': industry_category.lower(), 'ug_school': ug_school.lower(), 'ug_degree': ug_degree.lower(), 'ug_grad_year': ug_grad_year, 'mba_school': mba_school.lower(), 'grad_year':grad_year, 'experience': experience, 'gender' : gender})


    #     if user_input:
    #         try:
    #             plot_peer_salary_path(df_graph, user_input)
                
    #         except TypeError:
    #             st.write(f'Fill in all details')
      
    if active_tab == "Machine Learning behind Career Plot":
        
        st.subheader("Methodology")
        st.write(f'Career plot is drawn on profile data collected from LinkedIn and salary data collected from Glassdoor. The data consists of professionals across various industries and educational backgrounds, Masters in Business Administration being the commonality for all.') 
        st.write('Its methodology consists of three steps: feature extraction, random forest model training, and career trajectory analysis. The feature extraction step involves extracting semantic and order information from the job title text. The semantic information is captured using Google Word2Vec, which maps the job title text into a 300-dimensional vector space that captures the meaning of the text. The order information is captured using PageRank on observed job switches, which assigns relative importance ranks to 1000 most common jobs.Then KNN (K nearest neighbor) model is used to extrapolate rank to all jobs.') 
        #st.write(f'')
        #image = Image.open('images/job_rank.png')
        #st.image(image)
        #st.write(f'')
        image = Image.open('images/Word_plot.png')
        st.image(image)
        #st.write(f'')
        st.write(f"The next step involves training a random forest model using the feature matrix that combines semantic and order information. The model predicts the salary for the user's job role by leveraging a database of over 100,000 unique job titles.")
        st.write(f"Finally, Career Plot builds a career trajectory based on the user's profile. This trajectory analysis can provide insights into career advancement opportunities and potential salary growth. ")
        #st.write(f'')
        st.subheader("Metrics")
        st.write(f"To evaluate the performance of Career Plot, we conducted experiments on a dataset of 6500 unique  job titles. The dataset was split into 80% training data and 20% testing data. We measured the accuracy of the random forest model by calculating the mean absolute error percentage (MAPE) and the R-squared score (R2). The MAPE and R2 values for the training and testing data were 28% , 0.49 and 35% , 0.39 , respectively. The graph below plots the actual and predicted salaries of the test data and shows a correlation between the two. ")
        #st.write(f'')
        image = Image.open('images/ML_graph.png')
        st.image(image)
        #st.write(f'')
        st.write(f'The tool has also accurately predicted career advancement opportunities for users, identifying job titles that are relevant to their career goals and providing insights into potential salary growth opportunities.')   
        
     
    if active_tab == "Know more about Career Plot":
        
        st.subheader("Introduction")
        st.write ("In today's job market, individuals need to make informed career decisions to achieve their career goals. Career Plot is a machine learning tool that predicts salaries and builds career trajectories based on job title semantics and order information. The tool is designed to help individuals make informed career decisions by providing insights into salary growth opportunities and career advancement paths.")
        st.write('Career Plot is a valuable tool for individuals and organizations looking to make informed career decisions. With the ability to predict salaries for over 100,000 unique job titles, Career Plot can be a powerful resource for job seekers and employers alike.')
        #st.write(f'')
        st.subheader("Recommendations")
        st.write('1. Use Career Plot to research potential career paths and identify job titles that align with your career goals.')
        st.write('2. Use Career Plot to negotiate salaries and understand the market value of your job title.')
        st.write('3. Use Career Plot to develop career paths for your employees and promote professional development within your organization.')
        #st.write(f'')
        st.write(f'To walk you through the process behind the hood, here is the ML architecture on which Career Plot is built. Click on the **:blue[Machine Learning behind Career PLot]** section to get into the details')
        image = Image.open('images/ml_architecture.jpeg')
        st.image(image)
    
if __name__ == '__main__':
    df = pd.read_csv('data/job_salary.csv')
    with zipfile.ZipFile('data/graph_data.csv.zip', 'r') as zip_ref:
        zip_ref.extractall('data/')
        
    df_graph = pd.read_csv('data/graph_data.csv')
    app()
