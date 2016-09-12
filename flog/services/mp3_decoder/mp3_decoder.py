import os
from pydub import AudioSegment
from flog.configs.conf import upload_folder, mp3_bitrate

def mp3_decoder(files, filename, subfolder):
    track = AudioSegment.from_mp3(files)
    track.export(os.path.join(upload_folder, subfolder, filename), format = "mp3", bitrate = mp3_bitrate)