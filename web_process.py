import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Configuration
SAVE_DIR = "data/web_articles"
IMAGE_DIR = os.path.join(SAVE_DIR, "images")
MAX_PAGES_PER_SITE = 50
REQUEST_DELAY = 1  # polite delay between requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Create directories
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def is_valid_url(url, base_domain):
    """Check if URL is valid for crawling."""
    parsed = urlparse(url)
    return (parsed.netloc == base_domain and 
            not parsed.path.startswith(('/logout', '/signout')) and
            not any(ext in parsed.path.lower() for ext in ['.pdf', '.zip']))

def sanitize_filename(url):
    """Create a filesystem-safe filename from a URL."""
    filename = re.sub(r'[^\w\-_.]', '_', url.split("//")[-1].split('?')[0])
    return filename[:150]

def scrape_clean_text(url):
    """Extract and clean text and image URLs from a webpage."""
    try:
        print(f"🔍 Scraping: {url}")
        headers = {'User-Agent': USER_AGENT}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        # Check for HTML content
        if 'text/html' not in res.headers.get('content-type', ''):
            print(f"⚠️ Skipping non-HTML content: {res.headers.get('content-type', '')}")
            return "", [], []

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove unnecessary tags (don't remove images now)
        for tag in soup(["script", "style", "footer", "nav", "form", "noscript", 
                         "iframe", "svg", "button", "input", "select"]):
            tag.decompose()

        # Extract meaningful text
        elements = soup.find_all(["p", "li", "pre", "code", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "article"])
        content = "\n".join(el.get_text(strip=True) for el in elements if el.get_text(strip=True))

        # Collect all valid internal links
        links = []
        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(url, link['href'])
            if is_valid_url(absolute_url, urlparse(url).netloc):
                links.append(absolute_url)

        # Collect image URLs
        img_urls = []
        for img_tag in soup.find_all("img", src=True):
            img_url = urljoin(url, img_tag['src'])
            if img_url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                img_urls.append(img_url)

        return content, links, img_urls

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {str(e)[:200]}")
    return "", [], []

def save_text(url, text, image_names=None):
    """Save text and image names to a .txt file."""
    if not text.strip():
        return False

    filename = sanitize_filename(url) + ".txt"
    path = os.path.join(SAVE_DIR, filename)

    # Append image names to text
    if image_names:
        text += "\n\n[Images saved with this article:]\n" + "\n".join(image_names)

    # Avoid redundant saves
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == text:
                print(f"⏩ Content unchanged, skipping: {path}")
                return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Saved: {path}")
    return True

def download_images(img_urls, page_url):
    """Download images and return local filenames."""
    saved_images = []
    for img_url in img_urls:
        try:
            # Create filename from URL
            img_filename = sanitize_filename(img_url)
            img_path = os.path.join(IMAGE_DIR, img_filename)
            
            # Skip if already exists
            if os.path.exists(img_path):
                saved_images.append(img_filename)
                continue

            # Download image
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(img_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Save image
            with open(img_path, 'wb') as f:
                f.write(response.content)
            saved_images.append(img_filename)
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"❌ Failed to download image {img_url}: {str(e)[:200]}")

    return saved_images

def process_websites():
    """Process websites and generate embeddings."""
    from utils.chunker import chunk_text
    from embeddings.embedder import embed_passages, save_embeddings

    all_texts = []
    processed_urls = set()

    # Process each .txt file in the web articles directory
    for filename in os.listdir(SAVE_DIR):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(SAVE_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                all_texts.append(text)
        except Exception as e:
            print(f"❌ Failed to read {filename}: {str(e)}")

    # Process texts into chunks and embeddings
    if all_texts:
        print(f"Processing {len(all_texts)} web articles...")
        all_chunks = []
        for text in all_texts:
            chunks = chunk_text(text)
            all_chunks.extend(chunks)

        print(f"Total chunks: {len(all_chunks)}")
        print("Generating embeddings...")
        embeddings = embed_passages(all_chunks)
        print("Saving index and passages...")
        save_embeddings(all_chunks, embeddings)
        print("✅ Done processing all web articles!")
    else:
        print("No web articles found to process.")

def scrape_site(start_url):
    """Crawl and save text and images from a site."""
    # Ensure URL starts with http:// or https://
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'https://' + start_url

    base_domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [start_url]
    pages_saved = 0

    while to_visit and pages_saved < MAX_PAGES_PER_SITE:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue
        visited.add(current_url)
        time.sleep(REQUEST_DELAY)

        text, links, img_urls = scrape_clean_text(current_url)
        image_names = download_images(img_urls, current_url)
        if text:
            if save_text(current_url, text, image_names):
                pages_saved += 1
                print(f"📄 Saved page {pages_saved}/{MAX_PAGES_PER_SITE} from {base_domain}")

        # Add new links to queue
        for link in links:
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    print(f"🌐 Finished scraping {base_domain}. Saved {pages_saved} pages.")


if __name__ == "__main__":
    # Define the websites to scrape
    websites = [
        "www.geeksforgeeks.org",
        "www.w3schools.com",
        "www.tutorialspoint.com",
        "www.analyticsvidhya.com",
        "www.wikipedia.com",
        "www.kaggle.com",
        "www.reddit.com",
        "www.python.org",
        "www.tensorflow.org",
        "www.pytorch.org",
        "www.scikit-learn.org",
        "www.opencv.org",
        "www.numpy.org",
        "www.pandas.pydata.org",
    ]
    
    # Scrape each website
    for website in websites:
        start_url = f"https://{website}"
        print(f"\n📚 Starting to scrape {website}...")
        scrape_site(start_url)
    
    # Process all scraped content
    print("\n🔄 Processing all web articles...")
    process_websites()
    print("\n✨ All done!")


