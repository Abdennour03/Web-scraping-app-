import streamlit as st
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import  parse_with_ollama



st.title("AI web Scraper") # Set the app title
url = st.text_input("Enter a Website URL: ") # Input field for website URL

if st.button("Scraper Site"): # Button to start scraping the website
    st.write("Screping the website") 
    result = scrape_website(url) # Scrape the website HTML
    body_content = extract_body_content(result) # Extract <body> from HTML
    cleaned_content = clean_body_content(body_content) # Clean body content

    # Store cleaned content in session state
    st.session_state.dom_content = cleaned_content

    # Show the cleaned DOM content in an expandable section
    with st.expander("view DOM content"):
         st.text_area("DOM content", cleaned_content, height = 300)

# If DOM content is available, allow user to describe what to parse
if "dom_content" in st.session_state:
    parse_description = st.text_area("Descrive wath you want to parse?")
    
    # Button to start parsing the content
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")
            dom_chunks = split_dom_content(st.session_state.dom_content) # Split DOM content into chunks
            result = parse_with_ollama(dom_chunks, parse_description) # Parse content using LLM
            st.write(result) # Display the parsed result
