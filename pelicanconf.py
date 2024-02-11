import datetime as dt


AUTHOR = 'Fabian Bardos'
SITENAME = 'Fabian Bardos'
SITEURL = 'http://bardos.dev'

# Set avatar and headings below
SITETITLE = 'Fabian Bardos'
SITESUBTITLE = 'Open (Data|Source) Enthusiast'
SITELOGO = SITEURL + "/images/avatar.png"

PATH = 'content'

TIMEZONE = 'Europe/Rome'

# With disabled URL hash, the links do not point to a html anchor.
# If enabled, the browsser scrolls down to the heading and eliminates
# the visible padding above the heading.
DISABLE_URL_HASH = True

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# THEME
THEME = 'refs/Flex'
THEME_COLOR = 'dark'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = False
THEME_COLOR_ENABLE_USER_OVERRIDE = False

# Use folder names as category
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'general'

# Static paths are needed to load images and favicon (under extra)
# to the generated output html files.
STATIC_PATHS= [
    'images',
    'extra',
]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# Social widget
SOCIAL = (
    ('github', 'https://github.com/fbardos'),
    ('stack-overflow', 'https://stackoverflow.com/users/4856719/fbardos'),
    ('mastodon', 'https://mastodon.social/@eschi'),
    # ('envelope', 'mailto:fabian@bardos.dev'),
)

# static paths will be copied without parsing their contents
# STATIC_PATHS = ['pages/about.rst']

# PAGE_PATHS = ['about']

# SOCIAL = (('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

COPYRIGHT_YEAR = dt.datetime.now().year
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike 4.0 International License",
    "version": "4.0",
    "slug": "by-sa",
    "icon": True,
    "language": "en_US",
}
