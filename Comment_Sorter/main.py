import streamlit as st

# Use a pipeline as a high-level helper
from transformers import pipeline

if 'all_comments' not in st.session_state:
    st.session_state.all_comments = []

model_path = "Models/models--distilbert--distilbert-base-uncased-finetuned-sst-2-english/snapshots/714eb0fa89d2f80546fda750413ed43d93601a13"
classifier = pipeline("text-classification", model=model_path)
st.title("Comments Analyzer")
st.video("https://www.youtube.com/watch?v=jSgdL1zX4h8&t=27640s")
comment = st.text_input("Enter Your Prompt", value="Amazing Video")

def classify_comment(classifier, comment):
    result = classifier(comment)[0]['label']
    return result

def display_comments(comments):
    for idx, comment in enumerate(comments):
        # Determine background color based on sentiment
        if comment['classification'] == 'POSITIVE':
            background_color = 'lightgreen'  # Light green
        elif comment['classification'] == 'NEGATIVE':
            background_color = 'lightcoral'  # Light red
        else:
            background_color = 'white'  # Default white

        # HTML template for comment display
        comment_html = f"""
        <div style="margin: 10px; padding: 10px; 
        border-radius: 5px; box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.1);
         background-color: {background_color}; padding-left:25px; padding-top:20px; padding-bottom:20px">
            <div style="font-weight: bold;">{comment['username']}</div>
            <div>{comment['comment']}</div>
        </div>
        """
         # Display comment using st.write with unsafe_allow_html=True
        st.write(comment_html, unsafe_allow_html=True)

# Streamlit app setup
st.title('Comment Display')

# Add a select box for sorting comments
sort_options = ['None', 'Positive', 'Negative']
sort_option = st.selectbox('Sort Comments By:', sort_options)

def sort_comments(comments, sort_option):
    if sort_option == 'Positive':
        positive_comments = [comment for comment in comments if comment['classification'] == 'POSITIVE']
        display_comments(positive_comments)
    elif sort_option == 'Negative':
        negative_comments = [comment for comment in comments if comment['classification'] == 'NEGATIVE']
        display_comments(negative_comments)
    else:
        display_comments(comments)

if st.button("Add Comment"):
    comment_dic = {'comment': comment, 'classification': classify_comment(classifier, comment), 'username': 'User'}
    st.session_state['all_comments'].append(comment_dic)

sort_comments(st.session_state['all_comments'], sort_option)
