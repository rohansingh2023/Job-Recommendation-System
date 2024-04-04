import streamlit as st
import pandas as pd
import pickle
import recommender

### Job Recommender
df = pickle.load(open('job_list.pkl','rb'))
cosine_sim = pickle.load(open('similarity_new.pkl','rb'))
indices = pd.Series(df.index, index= df['jobtitle']).drop_duplicates()

toon_list = df['jobtitle'].values

def get_recommendation(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda X: X[1], reverse=True)
    sim_scores = sim_scores[1:10]
    tech_indices = [i[0] for i in sim_scores]
    return df['jobtitle'].iloc[tech_indices]
# web app
if 'user_rec' not in st.session_state:
    st.session_state['user_rec'] = []

st.title('Job Recommendation system')
sel_toon = st.selectbox('search job',toon_list)

if st.button("Show Recommendation"):
    recommend_names = get_recommendation(sel_toon)
    for i in recommend_names:
        st.subheader(i)

st.text("")
st.text("")
st.text("")

### Profile Recommender
st.title("Profile Matches based on Skill-set")

html = st.number_input("HTML", step=1)
python = st.number_input("Python", step=1)
java = st.number_input("Java", step=1)
c = st.number_input("C", step=1)
javascript = st.number_input("Javascript", step=1)
candidates = st.number_input("No of Candidates", step=1)

def recommend_users():
    # global user_rec
    requirement = {"REQUIREMENT": {
                "HTML": html,
                "Python": python,
                "Java": java,
                "C": c,
                "JavaScript": javascript}}
    result = recommender.topMatches(requirement, recommender.dataFrame, "REQUIREMENT", candidates)
    st.session_state['user_rec'].extend(result)

st.button("Recommend", on_click=recommend_users)

if st.session_state['user_rec']:
    # st.write(st.session_state['user_rec'])
    for sim, name in st.session_state['user_rec']:
        st.write(f"{name}: {sim}")
