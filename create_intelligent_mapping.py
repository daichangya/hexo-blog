#!/usr/bin/env python3
"""
Create intelligent mapping between old slugs and new permalinks based on filename matching.
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict

# Configuration
POSTS_DIR = "/Users/changyadai/IdeaProjects/hexo-blog/source/_posts"

def extract_permalink(file_path):
    """Extract permalink from markdown file frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find permalink in frontmatter
        match = re.search(r'permalink:\s*/archives/([^/\s]+)/', content)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def build_file_mapping(posts_dir):
    """Build a mapping of filename stems to permalinks."""
    file_mapping = {}
    
    for md_file in Path(posts_dir).glob('*.md'):
        permalink = extract_permalink(md_file)
        if permalink:
            file_mapping[md_file.stem] = permalink
    
    return file_mapping

def extract_old_slugs(posts_dir):
    """Extract all old slugs from all markdown files."""
    slug_set = set()
    
    for md_file in Path(posts_dir).glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all old blog links
            pattern = r'https://blog\.jsdiff\.com/archives/([^/\s\)\]\}]+)'
            matches = re.findall(pattern, content)
            
            for old_slug in matches:
                decoded_slug = unquote(old_slug)
                slug_set.add(decoded_slug)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return slug_set

def find_best_match(old_slug, file_mapping):
    """Find the best matching file for an old slug."""
    # First try exact match
    if old_slug in file_mapping:
        return file_mapping[old_slug]
    
    # Try case-insensitive match
    old_slug_lower = old_slug.lower()
    for stem, permalink in file_mapping.items():
        if stem.lower() == old_slug_lower:
            return permalink
    
    # Try to find partial matches (for cases like "如何在ubuntu1804上安装和保护redis" vs "ru-he-zai-Ubuntu-18-04-shang-an-zhuang")
    # This is harder, so we'll skip for now and return None
    return None

def main():
    print("Building file mapping...")
    file_mapping = build_file_mapping(POSTS_DIR)
    print(f"Found {len(file_mapping)} files with permalinks")
    
    print("\nExtracting old slugs...")
    old_slugs = extract_old_slugs(POSTS_DIR)
    print(f"Found {len(old_slugs)} unique old slugs")
    
    print("\nCreating intelligent mapping...")
    mapping = {}
    unmatched = []
    
    for old_slug in sorted(old_slugs):
        permalink = find_best_match(old_slug, file_mapping)
        if permalink:
            mapping[old_slug] = permalink
        else:
            unmatched.append(old_slug)
    
    print(f"\nMatched {len(mapping)} slugs")
    print(f"Unmatched {len(unmatched)} slugs")
    
    # Write mapping to file
    with open('/Users/changyadai/IdeaProjects/hexo-blog/intelligent_mapping.txt', 'w', encoding='utf-8') as f:
        for old_slug in sorted(mapping.keys()):
            f.write(f"{old_slug} -> {mapping[old_slug]}\n")
        
        f.write("\n# UNMATCHED SLUGS (need manual mapping)\n")
        for old_slug in sorted(unmatched):
            f.write(f"# {old_slug}\n")
    
    print("\nMapping written to intelligent_mapping.txt")
    
    # Show some unmatched examples
    if unmatched:
        print("\nFirst 20 unmatched slugs:")
        for slug in unmatched[:20]:
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
