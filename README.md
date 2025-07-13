# Walden Perry's Blog

A personal blog built with [Zola](https://www.getzola.org/), a fast static site generator written in Rust.

## Development

1. Install Zola: `brew install zola` (macOS)
2. Clone this repository
3. Run `zola serve` to start the development server
4. Visit `http://127.0.0.1:1111`

## Deployment

Build the site with `zola build` - output will be in the `public/` directory.

## Structure

- `content/` - Blog posts and pages in Markdown
- `templates/` - HTML templates 
- `static/` - Static assets (CSS, images, etc.)
- `config.toml` - Site configuration
