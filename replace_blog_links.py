#!/usr/bin/env python3
"""
Script to replace old blog.jsdiff.com links with new www.tushu.info links
based on the permalink in each markdown file's frontmatter.
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote

# Configuration
POSTS_DIR = "/Users/changyadai/IdeaProjects/hexo-blog/source/_posts"
OLD_DOMAIN = "blog.jsdiff.com"
NEW_DOMAIN = "www.tushu.info"

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

def build_permalink_map(posts_dir):
    """Build a mapping of old URL slugs to new permalinks."""
    permalink_map = {}
    
    for md_file in Path(posts_dir).glob('*.md'):
        permalink = extract_permalink(md_file)
        if permalink:
            # Store the permalink for this file
            permalink_map[md_file.stem] = permalink
    
    return permalink_map

def replace_links_in_file(file_path, permalink_map):
    """Replace old blog links with new ones in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match old blog links
        # https://blog.jsdiff.com/archives/XXXXX
        pattern = r'https://blog\.jsdiff\.com/archives/([^/\s\)\]\}]+)'
        
        def replace_match(match):
            old_slug = match.group(1)
            # Try to URL decode the old slug to see if it matches a filename
            decoded_slug = unquote(old_slug)
            
            # Check if the decoded slug matches any file stem
            if decoded_slug in permalink_map:
                new_permalink = permalink_map[decoded_slug]
                return f'https://{NEW_DOMAIN}/archives/{new_permalink}'
            
            # If not found, try the original slug
            if old_slug in permalink_map:
                new_permalink = permalink_map[old_slug]
                return f'https://{NEW_DOMAIN}/archives/{new_permalink}'
            
            # If still not found, keep the original link
            print(f"Warning: Could not find permalink for {old_slug} (decoded: {decoded_slug})")
            return match.group(0)
        
        content = re.sub(pattern, replace_match, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    print("Building permalink map...")
    permalink_map = build_permalink_map(POSTS_DIR)
    print(f"Found {len(permalink_map)} permalinks")
    
    print("\nReplacing links in markdown files...")
    modified_count = 0
    total_files = 0
    
    for md_file in Path(POSTS_DIR).glob('*.md'):
        total_files += 1
        if replace_links_in_file(md_file, permalink_map):
            modified_count += 1
            print(f"Modified: {md_file.name}")
    
    print(f"\nDone! Modified {modified_count} out of {total_files} files")

if __name__ == "__main__":
    main()
