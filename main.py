import streamlit as st
from scrape import (scrape_website,split_dom_content, clean_body_content,extract_body_content)

st.title("Web Scraper for APP DEV")  # Title of the web app
url = st.text_input("Enter the URL to scrape")  # Input field for the URL

if st.button("Scrape Site"):
    st.write("Scraping...")
    
    result = scrape_website(url) 
    body_content = extract_body_content(result)  # Extract body content from the HTML
    cleaned_content = clean_body_content(body_content)  # Clean the body content

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)
