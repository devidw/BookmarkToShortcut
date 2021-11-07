import os
import glob
import re

class BookmarkToShortcut:
    """Convert browser bookmarks into shortcut files"""

    supported_formats = {'desktop', 'url', 'webloc'}
    _format_templates = {
        # Windows
        'url': '[InternetShortcut]\nURL={url}',
        # Linux
        'desktop': '[Desktop Entry]\nEncoding=UTF-8\nIcon=text-html\nType=Link\nName={name}\nURL={url}',
        # Mac OS
        'webloc': '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n\t<dict>\n\t\t<key>URL</key>\n\t\t<string>{url}</string>\n\t</dict>\n</plist>',
    }

    def __init__(self, in_dir, out_dir, formats):
        self.in_dir = in_dir
        self.out_dir = out_dir
        # formats which are in supported format set and passed
        self.formats = self.supported_formats & formats

        # check directory existence
        for dir in [self.in_dir, self.out_dir]:
            if not os.path.isdir(dir):
                raise ValueError ('directory doesn\'t exist')

        # check format support
        # unsupported formats already removed at this point
        if not self.formats:
            raise ValueError ('unsupported output format')

    @property
    def _in_files(self):
        """all input files inside input directory"""
        # NOTE: on Windows it's \ instead of /
        in_files = tuple(glob.glob(self.in_dir + '/*.html'))
        if in_files:
            return in_files
        else:
            raise ValueError ('no valid file to convert')

    def _format_contents(self, file_format, replacements):
        """prepare file contents for writing"""
        url, name = replacements
        return self._format_templates[file_format].format(url=url, name=name)

    def _write_file(self, name, contents):
        """create file and write contents into it"""
        filename = ''.join(c for c in name if re.match('^[\w\-. ]+$', c))
        with open(self.out_dir + '/' + filename, 'w') as f:
            f.write(contents)

    def _parse(self, file):
        """parse file to extract bookmarks"""
        with open(file) as f:
            html = f.read()
            # NOTE: only works for " not for '
            pattern = r'<a.+href="([^"]+)".*>(.+)<\/a>'
            matches = re.findall(pattern, html, re.IGNORECASE)
            return matches

    def convert(self):
        """desc"""
        # parse all input files
        for file in self._in_files:
            bookmarks = self._parse(file)
            # loop trough bookmarks
            for url, name in bookmarks:
                # write files foreach output format
                for format in self.formats:
                    contents = self._format_contents(format, (url, name))
                    self._write_file(name + '.' + format, contents)
