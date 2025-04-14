import streamlit as st
from scrape import (scrape_website,split_dom_content, clean_body_content,extract_body_content)

from parse import parse_with_ollama

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

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing content..")

            dom_chunks=split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks,parse_description)
            st.write(result)

    