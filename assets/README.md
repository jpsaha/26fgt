# Assets

Static web assets.

This directory contains files used by the generated website that are not generated
from the Typst source itself.

## Structure

### `css/`

Website stylesheets.

The main stylesheet is:

```text
assets/css/style.css
```

### `og/`

Open Graph images used for social-media previews and link sharing.

The default Open Graph image is:

```text
assets/og/default.png
```

The image is generated from an Asymptote source file:

```text
assets/og/default.asy
```

A PDF version is also retained as the vector master:

```text
assets/og/default.pdf
```

The image-generation workflow is:

```bash
asy -f pdf -o assets/og/default assets/og/default.asy

magick -density 700 assets/og/default.pdf \
  -resize 1200x630! \
  -filter Lanczos \
  assets/og/default.png

file assets/og/default.png

open  assets/og/default.png

```

The final PNG is **1200 × 630 pixels**, suitable for use as the default
`og:image` for the website.
