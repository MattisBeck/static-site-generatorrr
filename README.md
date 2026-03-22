# static-site-generatorrr

A simple static site generator written in Python — built for learning and to make expanding websites easier, because handwriting HTML is tedious.

Inspired by tools like [Hugo](https://github.com/gohugoio/hugo) and [Jekyll](https://github.com/jekyll/jekyll), this project converts Markdown files into a full static website using a single HTML template.

---

## How it works

1. Write content as Markdown files in the `content/` directory.
2. Place static assets (CSS, images, etc.) in the `static/` directory.
3. Run the generator — it converts every `.md` file to an `.html` file, applies `template.html`, and writes the result to `docs/`.

### Supported Markdown features

- Headings (`#` through `######`)
- Paragraphs
- Bold (`**text**`) and italic (`_text_`)
- Inline code (`` `code` ``)
- Code blocks (` ``` `)
- Blockquotes (`>`)
- Unordered lists (`- item`)
- Ordered lists (`1. item`)
- Links (`[text](url)`) and images (`![alt](url)`)

---

## Project structure

```
static-site-generatorrr/
├── content/          # Markdown source files
├── static/           # Static assets (CSS, images, …)
├── src/              # Python source code
├── docs/             # Generated output (HTML)
├── template.html     # HTML template used for every page
├── main.sh           # Run the generator locally
├── build.sh          # Run the generator with a custom base path
└── test.sh           # Run the test suite
```

---

## Usage

### Generate the site locally

```bash
bash main.sh
```

### Generate the site with a custom base path (e.g. for GitHub Pages)

```bash
bash build.sh
```

### Run tests

```bash
bash test.sh
```

---

## Template

`template.html` is the base layout for every page. Two placeholders are replaced at build time:

| Placeholder      | Replaced with                              |
|------------------|--------------------------------------------|
| `{{ Title }}`    | The first `# H1` heading in the Markdown file |
| `{{ Content }}`  | The full Markdown content converted to HTML |
