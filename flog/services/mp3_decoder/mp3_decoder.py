import os
from pydub import AudioSegment
from flog.configs.conf import UPLOAD_FOLDER, MP3_BITRATE

def mp3_decoder(files, filename, subfolder):
    track = AudioSegment.from_mp3(files)
    track.export(os.path.join(UPLOAD_FOLDER, subfolder, filename), format = "mp3", bitrate = MP3_BITRATE)