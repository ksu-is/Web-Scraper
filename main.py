import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import json
import pandas as pd

st.title("Web Scraper & Parser")
url = st.text_input("🔗 Enter the URL to scrape")

# Background image
bg_choice = st.selectbox("🎨 Choose a background theme:", [ "Lite", "Python", "Wall-E"])

# URL Map for Each Theme
bg_map = {
    "Wall-E": "https://images.unsplash.com/photo-1563207153-f403bf289096?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Lite": "https://images.unsplash.com/photo-1612670940073-8aed2145ebc3?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Python": "https://images.unsplash.com/photo-1649180556628-9ba704115795?q=80&w=1162&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
}

# Selected URL
bg_url = bg_map[bg_choice]

# Inject CSS Background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
  header {{
        background: transparent !important;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)

# Scraping
if st.button("Scrape Site"):
    st.write("🔍 Scraping...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content
    st.session_state.pop("parsed_result", None)  # Reset previous result

    st.markdown("---")
    with st.expander("📄 View Raw DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Parsing
if st.session_state.get("dom_content"):
    parse_description = st.text_area("🧠 Describe what to parse:")

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("⚙️ Parsing content with Ollama..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)

            st.session_state.parsed_result = result  # Store in session

# Display + Downloads
if st.session_state.get("parsed_result"):
    st.markdown("---")
    with st.expander("✅ Parsed Results", expanded=True):
        st.code(st.session_state.parsed_result, language="markdown")

        # JSON download
        json_data = {"parsed_output": st.session_state.parsed_result}
        st.download_button(
            "⬇️ Download as JSON",
            data=json.dumps(json_data, indent=2),
            file_name="parsed_output.json",
            mime="application/json"
        )

        # CSV download (try to parse if table-like)
        try:
            rows = [line.split("|") for line in st.session_state.parsed_result.split("\n") if "|" in line]
            df = pd.DataFrame(rows)
            csv_data = df.to_csv(index=False)
            st.download_button(
                "⬇️ Download as CSV",
                data=csv_data,
                file_name="parsed_output.csv",
                mime="text/csv"
            )
        except Exception:
            st.info("⚠️ CSV not available: output is not structured as a table.")

st.markdown("----")
st.caption("Created for APP DEV IS3020 | © 2025")
