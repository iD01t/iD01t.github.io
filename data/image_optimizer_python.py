#!/usr/bin/env python3
"""
HD Products Image Optimizer & Validator
======================================

A comprehensive Python utility for managing and optimizing product images
in the HD Products System. Handles batch processing, validation, and 
automatic cover generation.

Features:
- Batch image URL validation
- Automatic HD cover generation using PIL
- Image optimization and compression
- Broken link detection and reporting
- Integration with product JSON data
- Unsplash API integration for stock images
- Parallel processing for performance

Usage:
    python image_optimizer.py --input products.json --output optimized.json
    python image_optimizer.py --validate-only --input audiobooks.json
    python image_optimizer.py --generate-covers --batch-size 10
"""

import json
import asyncio
import aiohttp
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import hashlib
import time
from urllib.parse import urlparse
import random
import colorsys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_optimizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ImageValidationResult:
    """Result of image validation"""
    url: str
    is_valid: bool
    status_code: Optional[int] = None
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    error_message: Optional[str] = None
    response_time: Optional[float] = None

@dataclass
class ProductImage:
    """Product image data structure"""
    product_id: str
    title: str
    author: str
    genre: str
    original_url: Optional[str] = None
    optimized_url: Optional[str] = None
    fallback_url: Optional[str] = None
    validation_result: Optional[ImageValidationResult] = None

class HDCoverGenerator:
    """Generate HD covers using PIL"""
    
    def __init__(self, width: int = 400, height: int = 600):
        self.width = width
        self.height = height
        self.colors = [
            '#1e40af', '#7c2d12', '#059669', '#dc2626', '#ea580c',
            '#0891b2', '#be185d', '#4338ca', '#65a30d', '#ca8a04',
            '#7c3aed', '#e11d48', '#0f766e', '#b91c1c', '#c2410c'
        ]
    
    def _get_color_for_text(self, text: str) -> str:
        """Generate consistent color based on text hash"""
        hash_obj = hashlib.md5(text.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        return self.colors[hash_int % len(self.colors)]
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _darken_color(self, color: Tuple[int, int, int], factor: float = 0.3) -> Tuple[int, int, int]:
        """Darken a color by given factor"""
        return tuple(max(0, int(c * (1 - factor))) for c in color)
    
    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> List[str]:
        """Wrap text to fit within max width"""
        words = text.split()
        lines = []
        current_line = words[0] if words else ''
        
        for word in words[1:]:
            test_line = f"{current_line} {word}"
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def generate_audiobook_cover(
        self, 
        title: str, 
        author: str, 
        genre: str = "Audiobook",
        duration: str = "",
        price: str = ""
    ) -> Image.Image:
        """Generate HD audiobook cover"""
        
        # Create image with gradient background
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Generate gradient background
        base_color = self._hex_to_rgb(self._get_color_for_text(title + author))
        dark_color = self._darken_color(base_color, 0.4)
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(base_color[0] * (1 - ratio) + dark_color[0] * ratio)
            g = int(base_color[1] * (1 - ratio) + dark_color[1] * ratio)
            b = int(base_color[2] * (1 - ratio) + dark_color[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add subtle pattern overlay
        pattern_color = (255, 255, 255, 25)  # Semi-transparent white
        for i in range(0, self.width, 40):
            for j in range(0, self.height, 40):
                if (i + j) % 80 == 0:
                    draw.rectangle([i, j, i+20, j+20], fill=pattern_color[:3])
        
        try:
            # Load fonts (fallback to default if not available)
            try:
                title_font = ImageFont.truetype("arial.ttf", 32)
                author_font = ImageFont.truetype("arial.ttf", 18)
                genre_font = ImageFont.truetype("arial.ttf", 14)
                icon_font = ImageFont.truetype("arial.ttf", 16)
            except:
                title_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
                genre_font = ImageFont.load_default()
                icon_font = ImageFont.load_default()
            
            # Draw title with text wrapping
            title_lines = self._wrap_text(title, title_font, self.width - 60)
            title_y = 150 - (len(title_lines) * 20)
            
            for i, line in enumerate(title_lines):
                bbox = title_font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                y = title_y + (i * 40)
                
                # Add shadow
                draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 128), font=title_font)
                # Main text
                draw.text((x, y), line, fill='white', font=title_font)
            
            # Draw author
            author_text = f"by {author}"
            bbox = author_font.getbbox(author_text)
            author_width = bbox[2] - bbox[0]
            author_x = (self.width - author_width) // 2
            author_y = title_y + (len(title_lines) * 40) + 30
            draw.text((author_x, author_y), author_text, fill=(255, 255, 255, 220), font=author_font)
            
            # Draw genre badge
            genre_text = genre.upper()
            genre_bbox = genre_font.getbbox(genre_text)
            genre_width = genre_bbox[2] - genre_bbox[0]
            badge_x = (self.width - 300) // 2
            badge_y = 400
            
            # Badge background
            draw.rectangle([badge_x, badge_y, badge_x + 300, badge_y + 30], 
                         fill=(255, 255, 255, 50))
            
            # Badge text
            genre_x = (self.width - genre_width) // 2
            draw.text((genre_x, badge_y + 8), genre_text, fill='white', font=genre_font)
            
            # Draw audiobook indicator
            audio_text = "🎧 AUDIOBOOK"
            audio_bbox = icon_font.getbbox(audio_text)
            audio_width = audio_bbox[2] - audio_bbox[0]
            audio_x = (self.width - audio_width) // 2
            draw.text((audio_x, 460), audio_text, fill='#fbbf24', font=icon_font)
            
            # Draw duration if provided
            if duration:
                duration_bbox = genre_font.getbbox(duration)
                duration_width = duration_bbox[2] - duration_bbox[0]
                duration_x = (self.width - duration_width) // 2
                draw.text((duration_x, 490), duration, fill=(255, 255, 255, 200), font=genre_font)
            
            # Draw price if provided
            if price:
                price_x, price_y = 280, 50
                draw.rectangle([price_x, price_y, price_x + 100, price_y + 35], fill='#10b981')
                price_bbox = icon_font.getbbox(price)
                price_text_width = price_bbox[2] - price_bbox[0]
                price_text_x = price_x + (100 - price_text_width) // 2
                draw.text((price_text_x, price_y + 10), price, fill='black', font=icon_font)
            
            # Draw border
            border_color = (255, 255, 255, 80)
            draw.rectangle([15, 15, self.width-15, self.height-15], outline=border_color[:3], width=3)
            
        except Exception as e:
            logger.warning(f"Font rendering failed, using basic text: {e}")
            # Fallback to basic text rendering
            draw.text((50, 200), title, fill='white')
            draw.text((50, 250), f"by {author}", fill='white')
            draw.text((50, 400), genre.upper(), fill='white')
            draw.text((50, 450), "🎧 AUDIOBOOK", fill='#fbbf24')
        
        return img
    
    def generate_ebook_cover(
        self, 
        title: str, 
        author: str, 
        genre: str = "eBook",
        pages: str = "",
        price: str = ""
    ) -> Image.Image:
        """Generate HD ebook cover"""
        
        # Similar to audiobook but with different styling
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Different color scheme for ebooks (greens instead of blues)
        base_colors = ['#059669', '#047857', '#065f46', '#10b981', '#34d399']
        base_color = self._hex_to_rgb(base_colors[hash(title + author) % len(base_colors)])
        dark_color = self._darken_color(base_color, 0.4)
        
        # Gradient background
        for y in range(self.height):
            ratio = y / self.height
            r = int(base_color[0] * (1 - ratio) + dark_color[0] * ratio)
            g = int(base_color[1] * (1 - ratio) + dark_color[1] * ratio)
            b = int(base_color[2] * (1 - ratio) + dark_color[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Geometric pattern for ebooks
        pattern_color = (255, 255, 255, 30)
        for i in range(0, self.width, 30):
            for j in range(0, self.height, 30):
                if (i + j) % 60 == 0:
                    draw.ellipse([i, j, i+15, j+15], fill=pattern_color[:3])
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 28)
            author_font = ImageFont.truetype("arial.ttf", 16)
            genre_font = ImageFont.truetype("arial.ttf", 12)
            icon_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
            genre_font = ImageFont.load_default()
            icon_font = ImageFont.load_default()
        
        try:
            # Title with wrapping
            title_lines = self._wrap_text(title, title_font, self.width - 50)
            title_y = 180 - (len(title_lines) * 15)
            
            for i, line in enumerate(title_lines):
                bbox = title_font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                y = title_y + (i * 35)
                
                # Shadow
                draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 100), font=title_font)
                # Main text
                draw.text((x, y), line, fill='white', font=title_font)
            
            # Author
            author_text = f"by {author}"
            bbox = author_font.getbbox(author_text)
            author_width = bbox[2] - bbox[0]
            author_x = (self.width - author_width) // 2
            author_y = title_y + (len(title_lines) * 35) + 25
            draw.text((author_x, author_y), author_text, fill=(255, 255, 255, 200), font=author_font)
            
            # Genre badge
            genre_y = 420
            draw.rectangle([50, genre_y, self.width-50, genre_y + 25], 
                         fill=(255, 255, 255, 40))
            genre_bbox = genre_font.getbbox(genre.upper())
            genre_width = genre_bbox[2] - genre_bbox[0]
            genre_x = (self.width - genre_width) // 2
            draw.text((genre_x, genre_y + 6), genre.upper(), fill='white', font=genre_font)
            
            # eBook indicator
            ebook_text = "📚 EBOOK"
            ebook_bbox = icon_font.getbbox(ebook_text)
            ebook_width = ebook_bbox[2] - ebook_bbox[0]
            ebook_x = (self.width - ebook_width) // 2
            draw.text((ebook_x, 470), ebook_text, fill='#10b981', font=icon_font)
            
            # Pages info
            if pages:
                pages_text = f"{pages} pages"
                pages_bbox = genre_font.getbbox(pages_text)
                pages_width = pages_bbox[2] - pages_bbox[0]
                pages_x = (self.width - pages_width) // 2
                draw.text((pages_x, 500), pages_text, fill=(255, 255, 255, 180), font=genre_font)
            
            # Price
            if price:
                price_x, price_y = 280, 50
                draw.rectangle([price_x, price_y, price_x + 100, price_y + 35], fill='#fbbf24')
                price_bbox = icon_font.getbbox(price)
                price_text_width = price_bbox[2] - price_bbox[0]
                price_text_x = price_x + (100 - price_text_width) // 2
                draw.text((price_text_x, price_y + 10), price, fill='black', font=icon_font)
            
            # Professional border
            border_color = (255, 255, 255, 60)
            draw.rectangle([20, 20, self.width-20, self.height-20], outline=border_color[:3], width=2)
            
        except Exception as e:
            logger.warning(f"eBook cover rendering failed: {e}")
            # Fallback rendering
            draw.text((50, 200), title, fill='white')
            draw.text((50, 250), f"by {author}", fill='white')
            draw.text((50, 400), genre.upper(), fill='white')
            draw.text((50, 450), "📚 EBOOK", fill='#10b981')
        
        return img
    
    def save_as_data_url(self, img: Image.Image, format: str = 'PNG') -> str:
        """Convert PIL Image to data URL"""
        buffer = io.BytesIO()
        img.save(buffer, format=format, optimize=True, quality=90)
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()
        return f"data:image/{format.lower()};base64,{img_base64}"

class ImageValidator:
    """Validate image URLs asynchronously"""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 10):
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def validate_url(self, session: aiohttp.ClientSession, url: str) -> ImageValidationResult:
        """Validate a single image URL"""
        async with self.semaphore:
            start_time = time.time()
            
            try:
                async with session.head(
                    url, 
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    headers={'User-Agent': 'HD-Products-Validator/1.0'}
                ) as response:
                    response_time = time.time() - start_time
                    
                    return ImageValidationResult(
                        url=url,
                        is_valid=response.status == 200,
                        status_code=response.status,
                        content_type=response.headers.get('content-type'),
                        content_length=response.headers.get('content-length'),
                        response_time=response_time
                    )
                    
            except asyncio.TimeoutError:
                return ImageValidationResult(
                    url=url,
                    is_valid=False,
                    error_message="Timeout",
                    response_time=time.time() - start_time
                )
            except Exception as e:
                return ImageValidationResult(
                    url=url,
                    is_valid=False,
                    error_message=str(e),
                    response_time=time.time() - start_time
                )
    
    async def validate_batch(self, urls: List[str]) -> List[ImageValidationResult]:
        """Validate multiple URLs concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            validated_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    validated_results.append(ImageValidationResult(
                        url=urls[i],
                        is_valid=False,
                        error_message=str(result)
                    ))
                else:
                    validated_results.append(result)
            
            return validated_results

class HDProductOptimizer:
    """Main optimizer class"""
    
    def __init__(self):
        self.cover_generator = HDCoverGenerator()
        self.validator = ImageValidator()
        self.stats = {
            'total_products': 0,
            'images_tested': 0,
            'images_valid': 0,
            'images_generated': 0,
            'processing_time': 0
        }
    
    def load_products(self, file_path: str) -> List[Dict]:
        """Load products from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle different JSON structures
            if isinstance(data, list):
                products = data
            elif isinstance(data, dict):
                if 'items' in data:
                    products = data['items']
                elif 'audiobooks' in data and 'ebooks' in data:
                    products = data['audiobooks'] + data['ebooks']
                else:
                    products = [data]
            else:
                raise ValueError("Invalid JSON structure")
            
            logger.info(f"Loaded {len(products)} products from {file_path}")
            return products
            
        except Exception as e:
            logger.error(f"Failed to load products from {file_path}: {e}")
            return []
    
    def save_products(self, products: List[Dict], file_path: str):
        """Save products to JSON file"""
        try:
            output_data = {
                "schema": "https://id01t.store/schemas/products-optimized.v1.json",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "optimizer_version": "1.0.0",
                "stats": self.stats,
                "products": products
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(products)} optimized products to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save products to {file_path}: {e}")
    
    async def validate_images(self, products: List[Dict]) -> List[Dict]:
        """Validate all product images"""
        logger.info("Starting image validation...")
        start_time = time.time()
        
        # Extract image URLs
        image_urls = []
        for product in products:
            url = product.get('image') or product.get('cover') or product.get('thumbnail')
            if url:
                image_urls.append(url)
        
        if not image_urls:
            logger.warning("No image URLs found in products")
            return products
        
        # Validate URLs
        validation_results = await self.validator.validate_batch(image_urls)
        
        # Create URL to result mapping
        url_results = {result.url: result for result in validation_results}
        
        # Update products with validation results
        valid_count = 0
        for product in products:
            url = product.get('image') or product.get('cover') or product.get('thumbnail')
            if url and url in url_results:
                result = url_results[url]
                product['_image_validation'] = asdict(result)
                if result.is_valid:
                    valid_count += 1
        
        # Update stats
        self.stats['images_tested'] = len(image_urls)
        self.stats['images_valid'] = valid_count
        
        processing_time = time.time() - start_time
        logger.info(f"Image validation complete: {valid_count}/{len(image_urls)} valid images in {processing_time:.2f}s")
        
        return products
    
    def generate_fallback_covers(self, products: List[Dict]) -> List[Dict]:
        """Generate fallback covers for products with invalid images"""
        logger.info("Generating fallback covers...")
        start_time = time.time()
        
        generated_count = 0
        
        for product in products:
            # Check if image validation failed or no image exists
            validation = product.get('_image_validation', {})
            has_valid_image = validation.get('is_valid', False)
            
            if not has_valid_image:
                # Generate appropriate cover based on product type
                product_type = product.get('type', 'ebook')
                title = product.get('title', 'Untitled')
                author = product.get('author') or product.get('authors', ['Unknown'])[0] if isinstance(product.get('authors'), list) else product.get('authors', 'Unknown')
                genre = product.get('genre') or product.get('categories', ['General'])[0] if isinstance(product.get('categories'), list) else product.get('categories', 'General')
                
                try:
                    if product_type == 'audiobook' or 'audio' in product_type.lower():
                        # Generate audiobook cover
                        duration = product.get('duration', '')
                        price = f"${product.get('price', '')}" if product.get('price') else ''
                        
                        cover_img = self.cover_generator.generate_audiobook_cover(
                            title, author, genre, duration, price
                        )
                    else:
                        # Generate ebook cover
                        pages = str(product.get('pages', '')) if product.get('pages') else ''
                        price_cad = product.get('price_cad')
                        price_usd = product.get('price_usd')
                        price = f"${price_cad} CAD" if price_cad else f"${price_usd} USD" if price_usd else ''
                        
                        cover_img = self.cover_generator.generate_ebook_cover(
                            title, author, genre, pages, price
                        )
                    
                    # Convert to data URL
                    data_url = self.cover_generator.save_as_data_url(cover_img)
                    
                    # Update product
                    product['_generated_cover'] = data_url
                    product['_cover_generation_timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    
                    generated_count += 1
                    
                    if generated_count % 10 == 0:
                        logger.info(f"Generated {generated_count} covers...")
                        
                except Exception as e:
                    logger.error(f"Failed to generate cover for {title}: {e}")
        
        processing_time = time.time() - start_time
        self.stats['images_generated'] = generated_count
        
        logger.info(f"Generated {generated_count} fallback covers in {processing_time:.2f}s")
        return products
    
    def optimize_data_structure(self, products: List[Dict]) -> List[Dict]:
        """Optimize product data structure"""
        logger.info("Optimizing data structure...")
        
        optimized_products = []
        
        for product in products:
            # Create optimized product structure
            optimized = {
                'id': product.get('id') or f"product_{hash(product.get('title', 'unknown'))}",
                'type': product.get('type', 'ebook'),
                'title': product.get('title', 'Untitled'),
                'author': product.get('author') or (
                    ', '.join(product.get('authors', ['Unknown'])) 
                    if isinstance(product.get('authors'), list) 
                    else product.get('authors', 'Unknown')
                ),
                'description': product.get('description', ''),
                'year': str(product.get('year', '')),
                'language': product.get('language', 'en'),
                'genre': product.get('genre') or (
                    product.get('categories', ['General'])[0] 
                    if isinstance(product.get('categories'), list) 
                    else product.get('categories', 'General')
                ),
                'price': product.get('price') or product.get('price_cad') or product.get('price_usd'),
                'currency': 'CAD' if product.get('price_cad') else 'USD' if product.get('price_usd') else 'CAD',
                'url': product.get('url', '#'),
                'tags': product.get('tags', [])
            }
            
            # Handle image sources in priority order
            image_validation = product.get('_image_validation', {})
            if image_validation.get('is_valid'):
                # Use original valid image
                optimized['image'] = image_validation['url']
                optimized['image_source'] = 'original'
            elif product.get('_generated_cover'):
                # Use generated fallback
                optimized['image'] = product['_generated_cover']
                optimized['image_source'] = 'generated'
            else:
                # Use placeholder or default
                optimized['image'] = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjY2NjIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5ObyBJbWFnZTwvdGV4dD48L3N2Zz4='
                optimized['image_source'] = 'placeholder'
            
            # Add type-specific fields
            if optimized['type'] == 'audiobook':
                optimized['duration'] = product.get('duration', '')
                optimized['narrators'] = product.get('narrators', [])
            else:
                optimized['pages'] = product.get('pages', '')
                optimized['format'] = product.get('format', 'PDF')
            
            # Add metadata
            optimized['_optimization_timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            optimized['_has_working_image'] = image_validation.get('is_valid', False)
            
            optimized_products.append(optimized)
        
        logger.info(f"Optimized {len(optimized_products)} product records")
        return optimized_products
    
    def generate_report(self, products: List[Dict]) -> Dict:
        """Generate optimization report"""
        report = {
            'summary': {
                'total_products': len(products),
                'processing_time': self.stats['processing_time'],
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            'images': {
                'total_tested': self.stats['images_tested'],
                'valid_images': self.stats['images_valid'],
                'invalid_images': self.stats['images_tested'] - self.stats['images_valid'],
                'generated_covers': self.stats['images_generated'],
                'success_rate': f"{(self.stats['images_valid'] / max(1, self.stats['images_tested']) * 100):.1f}%"
            },
            'products_by_type': {},
            'products_by_language': {},
            'issues': []
        }
        
        # Analyze products
        for product in products:
            # By type
            ptype = product.get('type', 'unknown')
            report['products_by_type'][ptype] = report['products_by_type'].get(ptype, 0) + 1
            
            # By language
            lang = product.get('language', 'unknown')
            report['products_by_language'][lang] = report['products_by_language'].get(lang, 0) + 1
            
            # Check for issues
            if not product.get('title'):
                report['issues'].append(f"Product {product.get('id', 'unknown')} missing title")
            if not product.get('author'):
                report['issues'].append(f"Product {product.get('id', 'unknown')} missing author")
            if product.get('image_source') == 'placeholder':
                report['issues'].append(f"Product {product.get('id', 'unknown')} has no working image")
        
        return report

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='HD Products Image Optimizer')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file path')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--validate-only', action='store_true', help='Only validate images, don\'t generate covers')
    parser.add_argument('--generate-covers', action='store_true', help='Generate covers for all products with invalid images')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout in seconds')
    parser.add_argument('--report', help='Generate optimization report to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize optimizer
    optimizer = HDProductOptimizer()
    optimizer.validator.timeout = args.timeout
    
    start_time = time.time()
    
    try:
        # Load products
        products = optimizer.load_products(args.input)
        if not products:
            logger.error("No products loaded, exiting")
            return
        
        optimizer.stats['total_products'] = len(products)
        
        # Validate images
        products = await optimizer.validate_images(products)
        
        # Generate covers if requested or if validation found issues
        if args.generate_covers or not args.validate_only:
            products = optimizer.generate_fallback_covers(products)
        
        # Optimize data structure
        if not args.validate_only:
            products = optimizer.optimize_data_structure(products)
        
        # Save results
        if args.output:
            optimizer.save_products(products, args.output)
        
        # Generate report
        total_time = time.time() - start_time
        optimizer.stats['processing_time'] = total_time
        
        report = optimizer.generate_report(products)
        
        # Save report if requested
        if args.report:
            with open(args.report, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {args.report}")
        
        # Print summary
        logger.info("=" * 50)
        logger.info("OPTIMIZATION COMPLETE")
        logger.info("=" * 50)
        logger.info(f"Products processed: {report['summary']['total_products']}")
        logger.info(f"Images tested: {report['images']['total_tested']}")
        logger.info(f"Valid images: {report['images']['valid_images']}")
        logger.info(f"Generated covers: {report['images']['generated_covers']}")
        logger.info(f"Success rate: {report['images']['success_rate']}")
        logger.info(f"Processing time: {total_time:.2f}s")
        
        if report['issues']:
            logger.warning(f"Found {len(report['issues'])} issues:")
            for issue in report['issues'][:5]:  # Show first 5 issues
                logger.warning(f"  - {issue}")
            if len(report['issues']) > 5:
                logger.warning(f"  ... and {len(report['issues']) - 5} more issues")
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
