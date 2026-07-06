#!/usr/bin/env python3
"""
Create comprehensive mapping between old slugs and new permalinks.
Combines title matching with content analysis for better results.
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
        
        match = re.search(r'title:\s*(.+)', content)
        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def build_file_info(posts_dir):
    """Build comprehensive file info including permalink, title, and filename."""
    file_info = {}
    
    for md_file in Path(posts_dir).glob('*.md'):
        permalink = extract_permalink(md_file)
        title = extract_title(md_file)
        if permalink:
            file_info[md_file.stem] = {
                'permalink': permalink,
                'title': title,
                'filename': md_file.name
            }
    
    return file_info

def extract_old_slugs(posts_dir):
    """Extract all old slugs from all markdown files."""
    slug_to_files = defaultdict(list)
    
    for md_file in Path(posts_dir).glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            pattern = r'https://blog\.jsdiff\.com/archives/([^/\s\)\]\}]+)'
            matches = re.findall(pattern, content)
            
            for old_slug in matches:
                decoded_slug = unquote(old_slug)
                slug_to_files[decoded_slug].append(md_file.stem)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return slug_to_files

def normalize_string(s):
    """Normalize string for comparison - remove spaces, special chars, etc."""
    if not s:
        return ""
    # Remove spaces, hyphens, underscores, and convert to lowercase
    s = re.sub(r'[\s\-_]', '', s.lower())
    # Remove common Chinese/English differences
    s = s.replace('ubuntu', 'ubuntu')
    s = s.replace('redis', 'redis')
    return s

def find_best_match(old_slug, file_info):
    """Find the best matching file for an old slug."""
    # First try exact title match
    for stem, info in file_info.items():
        if info['title'] == old_slug:
            return info['permalink']
    
    # Try normalized title match
    normalized_slug = normalize_string(old_slug)
    for stem, info in file_info.items():
        if normalize_string(info['title']) == normalized_slug:
            return info['permalink']
    
    # Try exact filename stem match
    if old_slug in file_info:
        return file_info[old_slug]['permalink']
    
    # Try case-insensitive filename match
    old_slug_lower = old_slug.lower()
    for stem, info in file_info.items():
        if stem.lower() == old_slug_lower:
            return info['permalink']
    
    # Try partial match (for cases like "如何在ubuntu1804上安装和保护redis")
    # Look for files that contain key parts of the slug
    if 'redis' in old_slug.lower():
        for stem, info in file_info.items():
            if 'redis' in stem.lower():
                # Check if there are other matching keywords
                if 'ubuntu' in old_slug.lower() and 'ubuntu' in stem.lower():
                    return info['permalink']
                if '安装' in old_slug or 'install' in old_slug.lower():
                    if 'an-zhuang' in stem or 'install' in stem.lower():
                        return info['permalink']
    
    return None

def main():
    print("Building file info...")
    file_info = build_file_info(POSTS_DIR)
    print(f"Found {len(file_info)} files with permalinks")
    
    print("\nExtracting old slugs...")
    slug_to_files = extract_old_slugs(POSTS_DIR)
    print(f"Found {len(slug_to_files)} unique old slugs")
    
    print("\nCreating comprehensive mapping...")
    mapping = {}
    unmatched = []
    
    for old_slug in sorted(slug_to_files.keys()):
        permalink = find_best_match(old_slug, file_info)
        if permalink:
            mapping[old_slug] = permalink
        else:
            unmatched.append(old_slug)
    
    print(f"\nMatched {len(mapping)} slugs")
    print(f"Unmatched {len(unmatched)} slugs")
    
    # Write mapping to file
    with open('/Users/changyadai/IdeaProjects/hexo-blog/comprehensive_mapping.txt', 'w', encoding='utf-8') as f:
        f.write("# OLD SLUG -> NEW PERMALINK MAPPING\n")
        f.write("# Edit this file to add mappings for unmatched slugs?\n\n")
        
        for old_slug in sorted(mapping.keys()):
            f.write(f"{old_slug} -> {mapping[old_slug]}\n")
        
        f.write("\n# UNMATCHED SLUGS (need manual mapping)\n")
        f.write("# Format: old_slug -> new_permalink\n")
        for old_slug in sorted(unmatched):
            # Try to suggest a file based on the files that reference this slug
            referencing_files = slug_to_files.get(old_slug, [])
            if referencing_files:
                f.write(f"# {old_slug} (referenced in: {', '.join(referencing_files[:3])})\n")
            else:
                f.write(f"# {old_slug}\n")
    
    print("\nMapping written to comprehensive_mapping.txt")
    
    # Show some matched examples
    if mapping:
        print("\nSome matched examples:")
        for old_slug in list(mapping.keys())[:15]:
            print(f"  {old_slug} -> {mapping[old_slug]}")
    
    # Show some unmatched examples
    if unmatched:
        print("\nFirst 20 unmatched slugs:")
        for slug in unmatched[:20]:
            print(f"  - {slug}")

if __name__ == "__main__":
    main()
