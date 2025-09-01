---
title: html selector 介绍
id: 77f5e24b-506c-4ae0-9790-90807dccb31e
date: 2025-07-01 15:44:29
author: daichangya
excerpt: 在 HTML 中，选择器（Selector）主要用于在 CSS 中选择 HTML 元素，以便为这些元素应用样式；在 JavaScript 中，也可以使用选择器来获取
  HTML 元素节点。下面分别从 CSS 选择器和 JavaScript 中使用的选择器进行详细介绍。 CSS 选择器 CSS 选择器是
permalink: /archives/html-selector-jie-shao/
categories:
- html
---

在 HTML 中，选择器（Selector）主要用于在 CSS 中选择 HTML 元素，以便为这些元素应用样式；在 JavaScript 中，也可以使用选择器来获取 HTML 元素节点。下面分别从 CSS 选择器和 JavaScript 中使用的选择器进行详细介绍。

### CSS 选择器
CSS 选择器是 CSS 规则的一部分，用于定位要应用样式的 HTML 元素。根据选择器的不同特性和功能，可分为以下几类：

#### 1. 元素选择器
通过元素名称来选择 HTML 元素。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 选择所有的 p 元素 */
        p {
            color: blue;
        }
    </style>
</head>
<body>
    <p>这是一个段落。</p>
    <p>这是另一个段落。</p>
</body>
</html>
```
在上述代码中，`p` 就是元素选择器，它会选中页面中所有的 `<p>` 元素，并将它们的文本颜色设置为蓝色。

#### 2. 类选择器
通过元素的 `class` 属性值来选择元素。类选择器以点号（`.`）开头。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 选择所有 class 为 highlight 的元素 */
       .highlight {
            background-color: yellow;
        }
    </style>
</head>
<body>
    <p class="highlight">这是一个高亮的段落。</p>
    <span class="highlight">这是一个高亮的文本。</span>
</body>
</html>
```
这里的 `.highlight` 就是类选择器，它会选中所有 `class` 属性值为 `highlight` 的元素，并将它们的背景颜色设置为黄色。

#### 3. ID 选择器
通过元素的 `id` 属性值来选择元素。ID 选择器以井号（`#`）开头。每个 HTML 元素的 `id` 属性值应该是唯一的。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 选择 id 为 main-heading 的元素 */
        #main-heading {
            font-size: 24px;
        }
    </style>
</head>
<body>
    <h1 id="main-heading">这是主标题</h1>
</body>
</html>
```
`#main-heading` 是 ID 选择器，它会选中 `id` 属性值为 `main-heading` 的元素，并将其字体大小设置为 24 像素。

#### 4. 属性选择器
根据元素的属性及其值来选择元素。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 选择所有带有 title 属性的元素 */
        [title] {
            border: 1px solid red;
        }
        /* 选择所有 type 属性值为 text 的 input 元素 */
        input[type="text"] {
            background-color: lightgray;
        }
    </style>
</head>
<body>
    <a href="#" title="点击这里">链接</a>
    <input type="text" placeholder="输入文本">
    <input type="password" placeholder="输入密码">
</body>
</html>
```
在上述代码中，`[title]` 选择所有带有 `title` 属性的元素，`input[type="text"]` 选择所有 `type` 属性值为 `text` 的 `<input>` 元素。

#### 5. 伪类选择器
用于选择处于特定状态的元素，如鼠标悬停、链接已访问等。伪类选择器以冒号（`:`）开头。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 鼠标悬停在链接上时的样式 */
        a:hover {
            color: red;
        }
        /* 已访问链接的样式 */
        a:visited {
            color: purple;
        }
    </style>
</head>
<body>
    <a href="#">这是一个链接</a>
</body>
</html>
```
`a:hover` 选择鼠标悬停在上面的 `<a>` 元素，`a:visited` 选择已经访问过的 `<a>` 元素。

#### 6. 组合选择器
可以将多个选择器组合起来使用，以更精确地选择元素。
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* 选择所有 div 元素内的 p 元素 */
        div p {
            color: green;
        }
    </style>
</head>
<body>
    <div>
        <p>这是 div 内的段落。</p>
    </div>
    <p>这是 div 外的段落。</p>
</body>
</html>
```
`div p` 是后代选择器，它会选中所有 `<div>` 元素内的 `<p>` 元素。

### JavaScript 中的选择器
在 JavaScript 中，可以使用选择器来获取 HTML 元素节点，主要通过以下几种方法：

#### 1. `document.getElementById()`
通过元素的 `id` 属性值来获取元素节点。
```html
<!DOCTYPE html>
<html lang="en">
<body>
    <h1 id="my-heading">这是一个标题</h1>
    <script>
        const heading = document.getElementById('my-heading');
        heading.style.color = 'red';
    </script>
</body>
</html>
```
在上述代码中，`document.getElementById('my-heading')` 会返回 `id` 属性值为 `my-heading` 的 `<h1>` 元素节点，然后将其文本颜色设置为红色。

#### 2. `document.getElementsByClassName()`
通过元素的 `class` 属性值来获取元素节点列表。
```html
<!DOCTYPE html>
<html lang="en">
<body>
    <p class="my-paragraph">这是一个段落。</p>
    <p class="my-paragraph">这是另一个段落。</p>
    <script>
        const paragraphs = document.getElementsByClassName('my-paragraph');
        for (let i = 0; i < paragraphs.length; i++) {
            paragraphs[i].style.color = 'blue';
        }
    </script>
</body>
</html>
```
`document.getElementsByClassName('my-paragraph')` 会返回所有 `class` 属性值为 `my-paragraph` 的元素节点列表，然后遍历该列表并将每个元素的文本颜色设置为蓝色。

#### 3. `document.getElementsByTagName()`
通过元素名称来获取元素节点列表。
```html
<!DOCTYPE html>
<html lang="en">
<body>
    <p>这是一个段落。</p>
    <p>这是另一个段落。</p>
    <script>
        const paragraphs = document.getElementsByTagName('p');
        for (let i = 0; i < paragraphs.length; i++) {
            paragraphs[i].style.color = 'green';
        }
    </script>
</body>
</html>
```
`document.getElementsByTagName('p')` 会返回所有 `<p>` 元素节点列表，然后遍历该列表并将每个元素的文本颜色设置为绿色。

#### 4. `document.querySelector()` 和 `document.querySelectorAll()`
`document.querySelector()` 方法返回匹配指定选择器的第一个元素节点，`document.querySelectorAll()` 方法返回匹配指定选择器的所有元素节点列表。
```html
<!DOCTYPE html>
<html lang="en">
<body>
    <p class="my-paragraph">这是一个段落。</p>
    <p class="my-paragraph">这是另一个段落。</p>
    <script>
        // 获取第一个 class 为 my-paragraph 的元素
        const firstParagraph = document.querySelector('.my-paragraph');
        firstParagraph.style.color = 'red';

        // 获取所有 class 为 my-paragraph 的元素
        const allParagraphs = document.querySelectorAll('.my-paragraph');
        for (let i = 0; i < allParagraphs.length; i++) {
            allParagraphs[i].style.backgroundColor = 'lightgray';
        }
    </script>
</body>
</html>
```
在上述代码中，`document.querySelector('.my-paragraph')` 返回第一个 `class` 属性值为 `my-paragraph` 的元素节点，`document.querySelectorAll('.my-paragraph')` 返回所有 `class` 属性值为 `my-paragraph` 的元素节点列表。