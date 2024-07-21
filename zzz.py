import os
import requests
from bs4 import BeautifulSoup
import base64

def download_favicon(url, save_path='favicon.ico'):
    try:
        # Send a request to get the webpage content
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the favicon link
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        
        if icon_link and 'href' in icon_link.attrs:
            favicon_href = icon_link['href']
            
            if favicon_href.startswith('data:image'):
                # The favicon is encoded as a base64 data URI
                header, encoded = favicon_href.split(',', 1)
                data = base64.b64decode(encoded)
                
                # Determine the file extension
                if 'image/png' in header:
                    ext = 'png'
                elif 'image/jpeg' in header:
                    ext = 'jpg'
                elif 'image/x-icon' in header or 'image/vnd.microsoft.icon' in header:
                    ext = 'ico'
                else:
                    ext = 'ico'  # Default to .ico if unknown
                
                # Save the decoded image data to a file
                save_path = f'favicon.{ext}'
                with open(save_path, 'wb') as file:
                    file.write(data)
                
                print(f"Favicon downloaded successfully and saved to {save_path}")
            else:
                # The favicon is a regular URL, download it
                favicon_url = urljoin(url, favicon_href)
                
                # Download the favicon
                icon_response = requests.get(favicon_url, stream=True)
                icon_response.raise_for_status()
                
                # Save the favicon to the specified path
                with open(save_path, 'wb') as file:
                    for chunk in icon_response.iter_content(1024):
                        file.write(chunk)
                
                print(f"Favicon downloaded successfully and saved to {save_path}")
        else:
            print("Favicon link not found in the webpage.")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download favicon: {e}")

# Example usage
download_favicon('hhttps://www.baidu.com/')

