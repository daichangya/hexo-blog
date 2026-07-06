#!/usr/bin/env python3
"""
Extract all old blog.jsdiff.com slugs from markdown files to create a mapping.
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

def extract_old_slugs(posts_dir):
    """Extract all old slugs from all markdown files."""
    slug_to_files = defaultdict(list)
    
    for md_file in Path(posts_dir).glob('*.md'):
        permalink = extract_permalink(md_file)
        if not permalink:
            continue
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all old blog links
            pattern = r'https://blog\.jsdiff\.com/archives/([^/\s\)\]\}]+)'
            matches = re.findall(pattern, content)
            
            for old_slug in matches:
                decoded_slug = unquote(old_slug)
                slug_to_files[decoded_slug].append({
                    'file': md_file.name,
                    'permalink': permalink,
                    'original_slug': old_slug
                })
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return slug_to_files

def main():
    print("Extracting old slugs from markdown files...")
    slug_to_files = extract_old_slugs(POSTS_DIR)
    
    print(f"\nFound {len(slug_to_files)} unique old slugs\n")
    
    # Sort by slug
    for slug in sorted(slug_to_files.keys()):
        files = slug_to_files[slug]
        print(f"Old slug: {slug}")
        print(f"  Found in {len(files)} file(s):")
        for file_info in files:
            print(f"    - {file_info['file']} -> permalink: {file_info['permalink']}")
        print()
    
    # Also output to a file for easier editing
    with open('/Users/changyadai/IdeaProjects/hexo-blog/slug_mapping.txt', 'w', encoding='utf-8') as f:
        for slug in sorted(slug_to_files.keys()):
            files = slug_to_files[slug]
            # Use the first file's permalink as the target
            target_permalink = files[0]['permalink']
            f.write(f"{slug} -> {target_permalink}\n")
    
    print("\nMapping written to slug_mapping.txt")

if __name__ == "__main__":
    main()
