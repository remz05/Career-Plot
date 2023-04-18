# Career-Plot
Career Plot aims to empower job seekers and employees by providing accurate and reliable information on salaries for different professions and industries. By leveraging the latest data analysis techniques and machine learning algorithms, we can help users make informed decisions about their career paths.

Career plot is drawn on profile data collected from LinkedIn and salary data collected from Glassdoor. The data consists of professionals across various industries and educational backgrounds, Masters in Business Administration being the commonality for all.

Its methodology consists of three steps: feature extraction, random forest model training, and career trajectory analysis. The feature extraction step involves extracting semantic and order information from the job title text. The semantic information is captured using Google Word2Vec, which maps the job title text into a 300-dimensional vector space that captures the meaning of the text. The order information is captured using PageRank on observed job switches, which assigns relative importance ranks to 1000 most common jobs.Then KNN (K nearest neighbor) model is used to extrapolate rank to all jobs.

The next step involves training a random forest model using the feature matrix that combines semantic and order information. The model predicts the salary for the user's job role by leveraging a database of over 100,000 unique job titles.

Finally, Career Plot builds a career trajectory based on the user's profile. This trajectory analysis can provide insights into career advancement opportunities and potential salary growth.

Here is the link to the website: https://career-plot.streamlit.app/
