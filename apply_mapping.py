#!/usr/bin/env python3
"""
Apply the comprehensive mapping to replace old blog.jsdiff.com links with new www.tushu.info links.
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote

# Configuration
POSTS_DIR = "/Users/changyadai/IdeaProjects/hexo-blog/source/_posts"
MAPPING_FILE = "/Users/changyadai/IdeaProjects/hexo-blog/comprehensive_mapping.txt"
OLD_DOMAIN = "blog.jsdiff.com"
NEW_DOMAIN = "www.tushu.info"

def load_mapping(mapping_file):
    """Load the mapping from the mapping file."""
    mapping = {}
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse mapping: old_slug -> new_permalink
            if ' -> ' in line:
                old_slug, new_permalink = line.split(' -> ', 1)
                mapping[old_slug] = new_permalink
    
    return mapping

def replace_links_in_file(file_path, mapping):
    """Replace old blog links with new ones in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Replace plain domain references (https://blog.jsdiff.com or https://blog.jsdiff.com/)
        # But skip image URLs (blog.jsdiff.com/upload/)
        content = re.sub(r'https://blog\.jsdiff\.com/(?![upload/])', f'https://{NEW_DOMAIN}/', content)
        
        # 2. Replace blog post links with /archives/
        pattern = r'https://blog\.jsdiff\.com/archives/([^/\s\)\]\}#]+)'
        
        def replace_match(match):
            full_match = match.group(0)
            old_slug = match.group(1)
            
            # Remove any URL fragment (anchor)
            if '#' in old_slug:
                old_slug = old_slug.split('#')[0]
            
            decoded_slug = unquote(old_slug)
            
            # Try decoded slug first
            if decoded_slug in mapping:
                new_permalink = mapping[decoded_slug]
                return f'https://{NEW_DOMAIN}/archives/{new_permalink}'
            
            # Try original slug
            if old_slug in mapping:
                new_permalink = mapping[old_slug]
                return f'https://{NEW_DOMAIN}/archives/{new_permalink}'
            
            # If not found, keep the original link
            return full_match
        
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
    print("Loading mapping...")
    mapping = load_mapping(MAPPING_FILE)
    print(f"Loaded {len(mapping)} mappings")
    
    print("\nReplacing links in markdown files...")
    modified_count = 0
    total_files = 0
    
    for md_file in Path(POSTS_DIR).glob('*.md'):
        total_files += 1
        if replace_links_in_file(md_file, mapping):
            modified_count += 1
            print(f"Modified: {md_file.name}")
    
    print(f"\nDone! Modified {modified_count} out of {total_files} files")

if __name__ == "__main__":
    main()
