#!/usr/bin/env python3
"""
Create intelligent mapping between old slugs and new permalinks based on title matching.
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

def extract_title(file_path):
    """Extract title from markdown file frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find title in frontmatter
        match = re.search(r'title:\s*(.+)', content)
        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def build_title_mapping(posts_dir):
    """Build a mapping of titles to permalinks."""
    title_mapping = {}
    
    for md_file in Path(posts_dir).glob('*.md'):
        permalink = extract_permalink(md_file)
        title = extract_title(md_file)
        if permalink and title:
            title_mapping[title] = permalink
    
    return title_mapping

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

def find_best_match(old_slug, title_mapping):
    """Find the best matching title for an old slug."""
    # First try exact match
    if old_slug in title_mapping:
        return title_mapping[old_slug]
    
    # Try case-insensitive match
    old_slug_lower = old_slug.lower()
    for title, permalink in title_mapping.items():
        if title.lower() == old_slug_lower:
            return permalink
    
    return None

def main():
    print("Building title mapping...")
    title_mapping = build_title_mapping(POSTS_DIR)
    print(f"Found {len(title_mapping)} files with titles")
    
    print("\nExtracting old slugs...")
    old_slugs = extract_old_slugs(POSTS_DIR)
    print(f"Found {len(old_slugs)} unique old slugs")
    
    print("\nCreating intelligent mapping...")
    mapping = {}
    unmatched = []
    
    for old_slug in sorted(old_slugs):
        permalink = find_best_match(old_slug, title_mapping)
        if permalink:
            mapping[old_slug] = permalink
        else:
            unmatched.append(old_slug)
    
    print(f"\nMatched {len(mapping)} slugs")
    print(f"Unmatched {len(unmatched)} slugs")
    
    # Write mapping to file
    with open('/Users/changyadai/IdeaProjects/hexo-blog/title_mapping.txt', 'w', encoding='utf-8') as f:
        for old_slug in sorted(mapping.keys()):
            f.write(f"{old_slug} -> {mapping[old_slug]}\n")
        
        f.write("\n# UNMATCHED SLUGS (need manual mapping)\n")
        for old_slug in sorted(unmatched):
            f.write(f"# {old_slug}\n")
    
    print("\nMapping written to title_mapping.txt")
    
    # Show some matched examples
    if mapping:
        print("\nSome matched examples:")
        for old_slug in list(mapping.keys())[:10]:
            print(f"  {old_slug} -> {mapping[old_slug]}")
    
    # Show some unmatched examples
    if unmatched:
        print("\nFirst 20 unmatched slugs:")
        for slug in unmatched[:20]:
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
