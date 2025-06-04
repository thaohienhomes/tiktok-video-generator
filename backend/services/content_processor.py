import os
import io
import aiofiles
import requests
from bs4 import BeautifulSoup
import PyPDF2
import pdfplumber
from typing import Optional
from fastapi import UploadFile, HTTPException
import validators

class ContentProcessor:
    """Service để xử lý và trích xuất nội dung từ PDF hoặc URL"""
    
    def __init__(self):
        self.max_content_length = 50000  # Giới hạn độ dài nội dung
    
    async def extract_from_file(self, file: UploadFile) -> str:
        """Trích xuất nội dung từ file upload"""
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="Tên file không hợp lệ")
        
        file_extension = file.filename.split('.')[-1].lower()
        
        # Read file content
        content = await file.read()
        
        if file_extension == 'pdf':
            return await self._extract_from_pdf(content)
        elif file_extension == 'txt':
            return content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Định dạng file không được hỗ trợ: {file_extension}"
            )
    
    async def extract_from_url(self, url: str) -> str:
        """Trích xuất nội dung từ URL"""
        
        if not validators.url(url):
            raise HTTPException(status_code=400, detail="URL không hợp lệ")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extract text from main content areas
            content_selectors = [
                'article',
                '.content',
                '.post-content',
                '.entry-content',
                'main',
                '.main-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True, separator=' ')
                    break
            
            # Fallback to body if no main content found
            if not content:
                content = soup.get_text(strip=True, separator=' ')
            
            # Clean and limit content
            content = self._clean_text(content)
            
            if len(content) < 100:
                raise HTTPException(
                    status_code=400, 
                    detail="Nội dung từ URL quá ngắn hoặc không thể trích xuất"
                )
            
            return content[:self.max_content_length]
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Không thể truy cập URL: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Lỗi khi xử lý URL: {str(e)}"
            )
    
    async def _extract_from_pdf(self, pdf_content: bytes) -> str:
        """Trích xuất text từ PDF"""
        
        try:
            # Try with pdfplumber first (better for complex layouts)
            with io.BytesIO(pdf_content) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    text = ""
                    for page in pdf.pages[:50]:  # Limit to first 50 pages
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    
                    if text.strip():
                        return self._clean_text(text)[:self.max_content_length]
        
        except Exception:
            # Fallback to PyPDF2
            try:
                with io.BytesIO(pdf_content) as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    
                    for page_num in range(min(50, len(pdf_reader.pages))):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text() + "\n"
                    
                    if text.strip():
                        return self._clean_text(text)[:self.max_content_length]
                        
            except Exception as e:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Không thể đọc file PDF: {str(e)}"
                )
        
        raise HTTPException(
            status_code=400, 
            detail="File PDF trống hoặc không thể trích xuất text"
        )
    
    def _clean_text(self, text: str) -> str:
        """Làm sạch và chuẩn hóa text"""
        
        # Remove extra whitespace and newlines
        import re
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove special characters but keep Vietnamese
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\'\"\n\u00C0-\u1EF9]', '', text)
        
        return text.strip()
    
    def get_content_preview(self, content: str, max_length: int = 500) -> str:
        """Lấy preview của nội dung"""
        if len(content) <= max_length:
            return content
        
        # Find good break point near max_length
        break_point = content.rfind('.', 0, max_length)
        if break_point == -1:
            break_point = content.rfind(' ', 0, max_length)
        
        if break_point == -1:
            break_point = max_length
        
        return content[:break_point] + "..." 