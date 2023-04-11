Title: First post: How this website is built
Date: 2023-04-10

I use [Pelican](https://github.com/getpelican/pelican) as Static Site Generator to build this website. It allows a intuitive approach to write blog posts and other pages with markdown. Furthermore, I use the [Flex theme](https://github.com/alexandrevicenzi/Flex).

## Installation

The installation was quite easy. I started with the follwoing mamba/conda environment:

```yaml
name: website
dependencies:
  - python=3.10.*
  - "pelican[markdown]"
  - markdown
```

Install with: `mamba env create -f environment.yml`.

Then, switch to an empty directory and execute `pelican-quickstart`.
From there, place the files (`.md` or `.rst`) for:

* static sites (like the about me page) into `content/pages/`
* blog articles into `content/<category_name>/`

Also, have a look at the [quickstart guide](https://getpelican.com/) from Pelican.


## Choosing theme
You find a collection of pelican themes on [github/getpelican/pelican-themes](https://github.com/getpelican/pelican-themes). Git clone a desired theme and reference it inside `pelicanconf.py`:

```python
THEME = '<path to flex directory>/Flex'
THEME_COLOR = 'dark'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = False
THEME_COLOR_ENABLE_USER_OVERRIDE = False
```

## Other configs
You can find another example inside the Flex repo [here](https://github.com/alexandrevicenzi/Flex/tree/master/docs). Other config options I've set inside `pelicanconf.py`:

```python
# Set avatar and headings below
SITETITLE = 'Fabian Bardos'
SITESUBTITLE = 'Open (Data|Source) Enthusiast'
SITELOGO = SITEURL + "/images/avatar.png"

# Social widget
SOCIAL = (
    ('github', 'https://github.com/fbardos'),
    ('stack-overflow', 'https://stackoverflow.com/users/4856719/fbardos'),
    ('mastodon', 'https://mastodon.social/@eschi'),
)

DEFAULT_PAGINATION = 5

# With disabled URL hash, the links do not point to a html anchor.
# If enabled, the browsser scrolls down to the heading and eliminates
# the visible padding above the heading.
DISABLE_URL_HASH = True

# Static paths are needed to load images and favicon (under extra)
# to the generated output html files.
STATIC_PATHS= [
    'images',
    'extra',
]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

```
