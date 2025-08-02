#!/usr/bin/env python3
"""
Web Scraper Application using Streamlit
A simple web scraping tool with a user-friendly interface.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Web Scraper Tool",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_page_content(url, timeout=10):
    """Fetch webpage content with error handling."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        return None, str(e)

def extract_text_content(html_content):
    """Extract clean text from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text and clean it
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def extract_links(html_content, base_url):
    """Extract all links from the webpage."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        link_text = link.get_text().strip()
        links.append({
            'text': link_text,
            'url': full_url,
            'is_external': urlparse(full_url).netloc != urlparse(base_url).netloc
        })
    
    return links

def extract_images(html_content, base_url):
    """Extract all images from the webpage."""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    
    for img in soup.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt', '')
        if src:
            full_url = urljoin(base_url, src)
            images.append({
                'alt_text': alt,
                'src': full_url
            })
    
    return images

def extract_metadata(html_content):
    """Extract page metadata."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    metadata = {
        'title': '',
        'description': '',
        'keywords': '',
        'author': ''
    }
    
    # Title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text().strip()
    
    # Meta tags
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        name = tag.get('name', '').lower()
        content = tag.get('content', '')
        
        if name == 'description':
            metadata['description'] = content
        elif name == 'keywords':
            metadata['keywords'] = content
        elif name == 'author':
            metadata['author'] = content
    
    return metadata

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🕷️ Web Scraper Tool")
    st.markdown("Extract content, links, images, and metadata from any webpage!")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # URL input
    url = st.sidebar.text_input(
        "Enter URL to scrape:",
        placeholder="https://example.com",
        help="Enter a valid URL starting with http:// or https://"
    )
    
    # Scraping options
    st.sidebar.subheader("Scraping Options")
    extract_text = st.sidebar.checkbox("Extract Text Content", value=True)
    extract_links_option = st.sidebar.checkbox("Extract Links", value=True)
    extract_images_option = st.sidebar.checkbox("Extract Images", value=True)
    extract_metadata_option = st.sidebar.checkbox("Extract Metadata", value=True)
    
    # Advanced options
    st.sidebar.subheader("Advanced Options")
    timeout = st.sidebar.slider("Request Timeout (seconds)", 5, 30, 10)
    max_text_length = st.sidebar.slider("Max Text Length", 1000, 50000, 10000)
    
    # Scrape button
    scrape_button = st.sidebar.button("🚀 Start Scraping", type="primary")
    
    # Main content area
    if scrape_button:
        if not url:
            st.error("Please enter a URL to scrape!")
            return
        
        if not is_valid_url(url):
            st.error("Please enter a valid URL (must start with http:// or https://)")
            return
        
        # Show progress
        with st.spinner("Scraping webpage..."):
            html_content, status = get_page_content(url, timeout)
        
        if html_content is None:
            st.error(f"Failed to fetch webpage: {status}")
            return
        
        st.success(f"✅ Successfully scraped webpage! (Status: {status})")
        
        # Create tabs for different content types
        tabs = []
        if extract_metadata_option:
            tabs.append("📊 Metadata")
        if extract_text:
            tabs.append("📝 Text Content")
        if extract_links_option:
            tabs.append("🔗 Links")
        if extract_images_option:
            tabs.append("🖼️ Images")
        
        if tabs:
            tab_objects = st.tabs(tabs)
            tab_index = 0
            
            # Metadata tab
            if extract_metadata_option:
                with tab_objects[tab_index]:
                    st.subheader("Page Metadata")
                    metadata = extract_metadata(html_content)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Title:**", metadata['title'] or "Not found")
                        st.write("**Author:**", metadata['author'] or "Not found")
                    with col2:
                        st.write("**Description:**", metadata['description'] or "Not found")
                        st.write("**Keywords:**", metadata['keywords'] or "Not found")
                    
                    # Display as JSON
                    with st.expander("View Raw Metadata"):
                        st.json(metadata)
                
                tab_index += 1
            
            # Text content tab
            if extract_text:
                with tab_objects[tab_index]:
                    st.subheader("Extracted Text Content")
                    text_content = extract_text_content(html_content)
                    
                    if text_content:
                        # Truncate if too long
                        if len(text_content) > max_text_length:
                            text_content = text_content[:max_text_length] + "... (truncated)"
                        
                        st.text_area(
                            "Page Text:",
                            text_content,
                            height=400,
                            help=f"Extracted {len(text_content)} characters"
                        )
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Text",
                            data=text_content,
                            file_name=f"scraped_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("No text content found on this page.")
                
                tab_index += 1
            
            # Links tab
            if extract_links_option:
                with tab_objects[tab_index]:
                    st.subheader("Extracted Links")
                    links = extract_links(html_content, url)
                    
                    if links:
                        # Filter options
                        col1, col2 = st.columns(2)
                        with col1:
                            show_external = st.checkbox("Show External Links", value=True)
                        with col2:
                            show_internal = st.checkbox("Show Internal Links", value=True)
                        
                        # Filter links
                        filtered_links = []
                        for link in links:
                            if (link['is_external'] and show_external) or (not link['is_external'] and show_internal):
                                filtered_links.append(link)
                        
                        if filtered_links:
                            # Create DataFrame
                            df_links = pd.DataFrame(filtered_links)
                            st.dataframe(
                                df_links,
                                use_container_width=True,
                                column_config={
                                    "url": st.column_config.LinkColumn("URL"),
                                    "is_external": st.column_config.CheckboxColumn("External")
                                }
                            )
                            
                            st.info(f"Found {len(filtered_links)} links ({len([l for l in filtered_links if l['is_external']])} external, {len([l for l in filtered_links if not l['is_external']])} internal)")
                            
                            # Download button
                            csv_data = df_links.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Links CSV",
                                data=csv_data,
                                file_name=f"scraped_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        else:
                            st.warning("No links match the current filter criteria.")
                    else:
                        st.warning("No links found on this page.")
                
                tab_index += 1
            
            # Images tab
            if extract_images_option:
                with tab_objects[tab_index]:
                    st.subheader("Extracted Images")
                    images = extract_images(html_content, url)
                    
                    if images:
                        st.info(f"Found {len(images)} images")
                        
                        # Display images in a grid
                        cols = st.columns(3)
                        for i, img in enumerate(images[:12]):  # Limit to first 12 images
                            with cols[i % 3]:
                                try:
                                    st.image(img['src'], caption=img['alt_text'] or "No alt text", use_column_width=True)
                                    st.caption(f"[View Full Size]({img['src']})")
                                except:
                                    st.error(f"Could not load image: {img['src']}")
                        
                        if len(images) > 12:
                            st.info(f"Showing first 12 images out of {len(images)} total.")
                        
                        # Download button for image URLs
                        df_images = pd.DataFrame(images)
                        csv_data = df_images.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Image URLs CSV",
                            data=csv_data,
                            file_name=f"scraped_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No images found on this page.")
    
    else:
        # Show instructions when no scraping is happening
        st.markdown("""
        ## How to use this Web Scraper:
        
        1. **Enter a URL** in the sidebar (must start with http:// or https://)
        2. **Select what to extract** using the checkboxes
        3. **Adjust settings** if needed (timeout, text length limit)
        4. **Click "Start Scraping"** to begin
        
        ### Features:
        - 📝 **Text Content**: Extract clean text from the webpage
        - 🔗 **Links**: Get all internal and external links
        - 🖼️ **Images**: View and download image URLs
        - 📊 **Metadata**: Page title, description, keywords, and author
        - 📥 **Export**: Download results as text or CSV files
        
        ### Tips:
        - Use reasonable timeout values for slow websites
        - Large pages may take longer to process
        - Some websites may block automated requests
        """)
        
        # Example URLs
        st.markdown("### Try these example URLs:")
        example_urls = [
            "https://httpbin.org/html",
            "https://quotes.toscrape.com/",
            "https://books.toscrape.com/",
            "https://example.com"
        ]
        
        for example_url in example_urls:
            if st.button(f"📋 {example_url}", key=example_url):
                st.sidebar.text_input("Enter URL to scrape:", value=example_url)

if __name__ == "__main__":
    main()