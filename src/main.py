import numpy as np
import matplotlib.pyplot as plt

import librosa
import librosa.display

import argparse
from pathlib import Path
from music_video import MusicVideo


def main():
    parser = argparse.ArgumentParser(description="video maker")

    parser.add_argument(
        "--input-dir",
        type=str
    )

    parser.add_argument(
        "--input-track",
        type=str
    )

    args = parser.parse_args()

    music_video = MusicVideo(args.input_dir, args.input_track)
    music_video.write()


def audio_analysis(track_path):
    y, sr = librosa.load(track_path)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # beats contains the frame indices of each detected beat
    # for synchronization and visualization, we'll need to expand this
    # to cover the limits of the data.  This can be done as follows:
    beats = librosa.util.fix_frames(beats, x_min=0, x_max=chroma.shape[1])

    # Now beat-synchronize the chroma features
    chroma_sync = librosa.util.sync(chroma, beats, aggregate=np.median)

    # For visualization, we can convert to time (in seconds)
    beat_times = librosa.frames_to_time(beats)

    # We'll plot the synchronized and unsynchronized features next
    # to each other
    
    fig, ax = plt.subplots(nrows=2, sharex=True)
    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[0],
                                   key='Eb:maj')
    ax[0].set(title='Uniform time sampling')
    ax[0].label_outer()

    librosa.display.specshow(chroma_sync, y_axis='chroma', x_axis='time',
                             x_coords=beat_times, ax=ax[1], key='Eb:maj')
    ax[1].set(title='Beat-synchronous sampling')
    fig.colorbar(img, ax=ax)

    # For clarity, we'll zoom in on a 15-second patch
    ax[1].set(xlim=[10, 25])

    #plt.show()
    return beats
    

if __name__ == "__main__":
    main()
