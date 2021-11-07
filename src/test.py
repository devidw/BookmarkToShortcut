from BookmarkToShortcut import BookmarkToShortcut

converter = BookmarkToShortcut(
    'tests/in', # input directory
    'tests/out', # output directory
    {'url', 'desktop', 'webloc'} # formats to write
)
converter.convert()
