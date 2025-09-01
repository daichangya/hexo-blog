import yaml
from pypinyin import lazy_pinyin, Style
import os
import re
import urllib.parse

# 预先收集所有已存在的 permalink
existing_permalinks = set()


def parse_front_matter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 分割 Front Matter 和正文
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        raise ValueError("Invalid Front Matter format: '---' not found or incomplete.")

    front_matter = parts[1].strip()
    body = parts[2]

    # 解析 YAML
    metadata = yaml.safe_load(front_matter)
    return metadata, body


def update_front_matter(file_path, new_path, updates):
    metadata, body = parse_front_matter(file_path)

    # 更新字段
    for key, value in updates.items():
        metadata[key] = value

    # 确保新文件的目录存在
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    # 重新生成 Front Matter 和内容（保留字段顺序）
    new_content = f"---\n{yaml.dump(metadata, allow_unicode=True, sort_keys=False)}---\n{body}"

    # 写入新文件
    with open(new_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    if new_path != file_path:
        print(f"Updating permalink for {file_path} to {new_path}")
        # 删除原文件
        os.remove(file_path)


def generate_pinyin_permalink(filename, existing_permalinks):
    # 去除文件名中的 .md 后缀
    filename = filename.replace('.md', '')

    # 将中文部分转换为拼音，非中文部分保留（包括数字和字母）
    parts = []
    current_part = ""
    for char in filename:
        if '\u4e00' <= char <= '\u9fa5':
            # 中文字符，转换为拼音
            if current_part:
                parts.append(current_part)
                current_part = ""
            pinyin = lazy_pinyin(char, style=Style.NORMAL)[0]
            parts.append(pinyin)
        else:
            # 非中文字符，保留字母和数字
            if char.isalnum():
                current_part += char
            else:
                # 符号，跳过
                if current_part:
                    parts.append(current_part)
                    current_part = ""
    if current_part:
        parts.append(current_part)

    # 合并所有部分并用 '-' 连接
    permalink = '-'.join(parts)

    # 去除末尾的短横线
    permalink = permalink.rstrip('-')

    # 限制长度不超过40字符，并确保最后一个单词完整
    limit = 40
    if len(permalink) > limit:
        last_hyphen = permalink[:limit].rfind('-')
        if last_hyphen > 0:
            permalink = permalink[:last_hyphen]
        else:
            permalink = permalink[:limit]

    # 检查 permalink 是否唯一，若不唯一则添加数字后缀
    base_permalink = f"/archives/{permalink}"
    if base_permalink not in existing_permalinks:
        return base_permalink
    else:
        suffix = 1
        while True:
            new_permalink = f"{base_permalink}-{suffix}"
            if new_permalink not in existing_permalinks:
                return new_permalink
            suffix += 1


def process_all_posts(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    metadata, _ = parse_front_matter(file_path)
                    if 'permalink' in metadata:
                        existing_permalinks.add(metadata['permalink'])
                    # if 'permalink' in metadata and re.search(r'[\u4e00-\u9fa5]', urllib.parse.unquote(metadata['permalink'])):
                    new_permalink = generate_pinyin_permalink(metadata['title'], existing_permalinks)
                    updates = {"permalink": new_permalink + "/"}
                    # 确保正确移除前缀
                    clean_permalink = new_permalink
                    if new_permalink.startswith("/archives/"):
                        clean_permalink = new_permalink[len("/archives/"):]
                    new_path = os.path.join("source", "_posts", clean_permalink + ".md")
                    update_front_matter(file_path, new_path, updates)
                    # print(f"Updated permalink for {file_path}: {new_permalink}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


# 示例用法
if __name__ == "__main__":
    posts_directory = "source/_posts"
    process_all_posts(posts_directory)

    # permalink = "/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86%E5%89%AF%E6%9C%AC%E5%92%8C%E5%AE%A2%E6%88%B7%E7%AB%AF/"
    # print(permalink)
    # print(urllib.parse.unquote(permalink))
    file_path = "二度北戴河.md"
    new_permalink = generate_pinyin_permalink(file_path, existing_permalinks)
    # 确保正确移除前缀
    clean_permalink = new_permalink
    if new_permalink.startswith("/archives/"):
        clean_permalink = new_permalink[len("/archives/"):]
    new_path = os.path.join("source", "_posts", clean_permalink + ".md")
    print(file_path)
    print("permalink: " + new_permalink)
    print("clean permalink: " + clean_permalink)
    print("new_path: " + new_path)