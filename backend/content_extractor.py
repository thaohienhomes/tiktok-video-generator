#!/usr/bin/env python3
"""
Content Extractor for PDF files and web URLs
Extracts text content for AI processing
"""

import os
import requests
from pathlib import Path
import PyPDF2
import pdfplumber
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from typing import Dict, Any, Optional

class ContentExtractor:
    """Extract content from various sources"""
    
    def __init__(self):
        self.max_content_length = 10000  # Limit content for AI processing
        
    async def extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF file"""
        try:
            content = ""
            metadata = {
                "pages": 0,
                "title": "",
                "author": "",
                "subject": ""
            }
            
            # Try pdfplumber first (better for text extraction)
            try:
                with pdfplumber.open(file_path) as pdf:
                    metadata["pages"] = len(pdf.pages)
                    
                    # Extract metadata if available
                    if pdf.metadata:
                        metadata["title"] = pdf.metadata.get("Title", "")
                        metadata["author"] = pdf.metadata.get("Author", "")
                        metadata["subject"] = pdf.metadata.get("Subject", "")
                    
                    # Extract text from all pages
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n\n"
                            
                        # Stop if content is too long
                        if len(content) > self.max_content_length:
                            content = content[:self.max_content_length]
                            break
                            
            except Exception as e:
                print(f"pdfplumber failed, trying PyPDF2: {e}")
                
                # Fallback to PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata["pages"] = len(pdf_reader.pages)
                    
                    # Extract metadata
                    if pdf_reader.metadata:
                        metadata["title"] = pdf_reader.metadata.get("/Title", "")
                        metadata["author"] = pdf_reader.metadata.get("/Author", "")
                        metadata["subject"] = pdf_reader.metadata.get("/Subject", "")
                    
                    # Extract text
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n\n"
                            
                        if len(content) > self.max_content_length:
                            content = content[:self.max_content_length]
                            break
            
            # Clean up content
            content = self._clean_text(content)
            
            if not content.strip():
                raise ValueError("No readable text found in PDF")
                
            return {
                "content": content,
                "metadata": metadata,
                "source_type": "pdf",
                "source_path": file_path,
                "length": len(content)
            }
            
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    async def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract content from web URL"""
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # Set headers to mimic browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch content
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            metadata = {
                "title": "",
                "description": "",
                "author": "",
                "url": url,
                "domain": parsed_url.netloc
            }
            
            # Get title
            title_tag = soup.find('title')
            if title_tag:
                metadata["title"] = title_tag.get_text().strip()
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata["description"] = meta_desc.get('content', '').strip()
            
            # Get author
            meta_author = soup.find('meta', attrs={'name': 'author'})
            if meta_author:
                metadata["author"] = meta_author.get('content', '').strip()
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            # Clean up content
            content = self._clean_text(content)
            
            # Limit content length
            if len(content) > self.max_content_length:
                content = content[:self.max_content_length]
            
            if not content.strip():
                raise ValueError("No readable content found on webpage")
                
            return {
                "content": content,
                "metadata": metadata,
                "source_type": "url",
                "source_url": url,
                "length": len(content)
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            raise Exception(f"URL extraction failed: {str(e)}")
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from HTML, removing navigation, ads, etc."""
        
        # Remove unwanted elements
        unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'ad', 'advertisement']
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove elements with unwanted classes/ids
        unwanted_selectors = [
            '[class*="nav"]', '[class*="menu"]', '[class*="sidebar"]',
            '[class*="ad"]', '[class*="advertisement"]', '[class*="footer"]',
            '[class*="header"]', '[id*="nav"]', '[id*="menu"]',
            '[id*="sidebar"]', '[id*="ad"]', '[id*="footer"]'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Try to find main content areas
        main_content_selectors = [
            'main', 'article', '[role="main"]', '.content', '.post-content',
            '.entry-content', '.article-content', '#content', '#main'
        ]
        
        content = ""
        
        # Look for main content areas first
        for selector in main_content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    content += element.get_text() + "\n\n"
                break
        
        # If no main content found, extract from body
        if not content.strip():
            body = soup.find('body')
            if body:
                # Focus on paragraph and heading content
                for tag in body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                    text = tag.get_text().strip()
                    if text and len(text) > 20:  # Only include substantial text
                        content += text + "\n\n"
        
        return content
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Vietnamese
        text = re.sub(r'[^\w\s\u00C0-\u024F\u1E00-\u1EFF.,!?;:()\-\"\']', ' ', text)
        
        # Remove repeated punctuation
        text = re.sub(r'[.,!?;]{2,}', '.', text)
        
        # Remove very short lines (likely not content)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 10:  # Only keep lines with substantial content
                cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        return text.strip()
    
    async def extract_content(self, source_type: str, source_path: str) -> Dict[str, Any]:
        """Main method to extract content from any source"""
        try:
            if source_type == "pdf":
                return await self.extract_from_pdf(source_path)
            elif source_type == "url":
                return await self.extract_from_url(source_path)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
                
        except Exception as e:
            print(f"❌ Content extraction failed: {e}")
            # Return fallback content
            return {
                "content": f"Sample content from {source_type}: {source_path}",
                "metadata": {
                    "title": f"Sample {source_type.upper()} Content",
                    "source": source_path
                },
                "source_type": source_type,
                "length": 50,
                "error": str(e)
            }

# Initialize extractor
content_extractor = ContentExtractor()

# Export for easy import
__all__ = ['content_extractor'] 