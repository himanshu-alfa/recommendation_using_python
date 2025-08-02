# 🕷️ Web Scraper Tool

A powerful and user-friendly web scraping application built with Streamlit that allows you to extract content, links, images, and metadata from any webpage.

## Features

- **📝 Text Content Extraction**: Clean text extraction from web pages
- **🔗 Link Analysis**: Extract and categorize internal/external links
- **🖼️ Image Discovery**: Find and preview all images on a page
- **📊 Metadata Extraction**: Get page title, description, keywords, and author
- **📥 Export Capabilities**: Download results as text or CSV files
- **⚙️ Customizable Settings**: Adjust timeout, text length limits, and more
- **🎨 Beautiful UI**: Modern, responsive interface with tabbed organization

## Installation

1. **Clone or download the files**:
   ```bash
   # If you have git
   git clone <repository-url>
   cd web-scraper-tool
   
   # Or just download the files directly
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run web_scraper_app.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## How to Use

### Basic Usage

1. **Enter a URL** in the sidebar (must start with `http://` or `https://`)
2. **Select extraction options**:
   - ✅ Extract Text Content
   - ✅ Extract Links  
   - ✅ Extract Images
   - ✅ Extract Metadata
3. **Adjust settings** if needed (timeout, text length limit)
4. **Click "🚀 Start Scraping"** to begin

### Advanced Features

#### Scraping Options
- **Text Content**: Extracts clean, readable text from the webpage
- **Links**: Finds all hyperlinks and categorizes them as internal or external
- **Images**: Discovers all images and provides preview functionality
- **Metadata**: Extracts SEO and page information

#### Settings
- **Request Timeout**: Set how long to wait for page responses (5-30 seconds)
- **Max Text Length**: Limit extracted text length to avoid overwhelming output
- **Link Filtering**: Show/hide internal and external links separately

#### Export Options
- **Text Files**: Download extracted text content
- **CSV Files**: Export links and images data for further analysis

### Example URLs to Try

The application includes several example URLs perfect for testing:

- `https://httpbin.org/html` - Simple HTML test page
- `https://quotes.toscrape.com/` - Quotes website with various content
- `https://books.toscrape.com/` - Book catalog with images and links
- `https://example.com` - Basic example page

## Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **Requests**: HTTP library for fetching web pages
- **BeautifulSoup4**: HTML parsing and content extraction
- **Pandas**: Data manipulation and CSV export
- **lxml**: Fast XML/HTML parser

### Features Explained

#### Text Extraction
- Removes JavaScript and CSS content
- Cleans up whitespace and formatting
- Provides character count and truncation options

#### Link Analysis
- Resolves relative URLs to absolute URLs
- Categorizes links as internal or external
- Extracts link text for context

#### Image Discovery
- Finds all `<img>` tags
- Resolves relative image URLs
- Extracts alt text for accessibility
- Provides image preview functionality

#### Metadata Extraction
- Page title from `<title>` tag
- Meta description, keywords, and author
- JSON export of all metadata

### Error Handling

The application includes robust error handling for:
- Invalid URLs
- Network timeouts
- Blocked requests
- Missing content
- Image loading failures

## Limitations and Considerations

### Technical Limitations
- Some websites may block automated requests
- JavaScript-rendered content may not be captured
- Large pages may take longer to process
- Rate limiting may be enforced by target websites

### Ethical Usage
- Always respect `robots.txt` files
- Don't overwhelm servers with rapid requests
- Be mindful of website terms of service
- Use for educational and legitimate purposes only

### Performance Tips
- Use reasonable timeout values
- Limit text extraction length for large pages
- Some websites work better with longer timeout values
- Try different user agents if requests are blocked

## Troubleshooting

### Common Issues

1. **"Failed to fetch webpage"**
   - Check if the URL is accessible in your browser
   - Try increasing the timeout value
   - Some sites may block automated requests

2. **"No content found"**
   - The page might be JavaScript-heavy
   - Try a different URL to test functionality

3. **Images not loading**
   - Some images may have access restrictions
   - Image URLs might be relative and not resolve correctly

4. **Slow performance**
   - Increase timeout for slow websites
   - Reduce max text length for large pages
   - Some websites naturally take longer to respond

### Getting Help

If you encounter issues:
1. Check the error messages in the Streamlit interface
2. Verify your internet connection
3. Try the example URLs to confirm functionality
4. Check if the target website is accessible in your browser

## Future Enhancements

Potential improvements for future versions:
- JavaScript rendering support (using Selenium)
- Bulk URL processing
- Advanced filtering and search options
- API integration for automated workflows
- Custom extraction rules
- Scheduled scraping capabilities

---

**Note**: This tool is for educational and legitimate research purposes. Always respect website terms of service and robots.txt files. Use responsibly and ethically.