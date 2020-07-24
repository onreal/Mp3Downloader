from __future__ import unicode_literals

import os
import unicodedata
import string
import youtube_dl
import random

from app import basedir
from app.helpers.LoggerHelper import LoggerHelper


class ConversionHelper(object):
    url = str
    filename = str
    tmp_filename = str
    total_bytes = str
    src_title = str
    valid_filename_chars = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩaAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ-_.() %s%s" % (string.ascii_letters, string.digits)
    char_limit = 255

    def __init__(self, url):
        self.url = url

    def conversion_options(self):
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
            'logger': LoggerHelper(),
            'progress_hooks': [self.progress_hook],
            'nocheckcertificate': 'true',
        }

    def progress_hook(self, d):
        if d['status'] == 'finished':
            self.filename = d['filename']
            self.total_bytes = d['total_bytes']
            print('Downloading, now converting ...')

    def process_conversion(self):

        simulate = self.conversion_options()
        simulate['simulate'] = True

        # extract info and get song title
        with youtube_dl.YoutubeDL(simulate) as ydl:
            info = ydl.extract_info(self.url, download=False)
            if info.get('track', None) is not None:
                self.src_title = info.get('track')
            elif info.get('alt_title', None) is not None:
                self.src_title = info.get('alt_title')
            elif info.get('title', None) is not None:
                self.src_title = info.get('title')
            elif info.get('uploader', None) is not None:
                self.src_title = info.get('uploader') + "-" + info.get('display_id')
            else:
                self.src_title = "mp3Father_no_title_" + random.randint(1, 9999999).__str__()

        directory = basedir + '/downloads'
        self.src_title = self.clean_filename(self.src_title)
        output_template = directory + '/' + self.src_title + '.%(ext)s'

        download = self.conversion_options()
        # add forcetitle attribute
        download['forcetitle'] = self.src_title
        download['outtmpl'] = output_template
        with youtube_dl.YoutubeDL(download) as ydl:
            ydl.download([self.url])

        # TODO check if file is saved successfully
        return self.src_title

    def clean_filename(self, filename, whitelist=valid_filename_chars, replace=' '):
        # replace spaces
        for r in replace:
            filename = filename.replace(r, '_')

        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('UTF8', 'ignore').decode()

        # keep only whitelisted chars
        cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
        if len(cleaned_filename) > self.char_limit:
            print(
                "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                    self.char_limit))

        return cleaned_filename[:self.char_limit]
