import subprocess
import itertools
import random
import cv2
import librosa
from video_group import VideoGroup

class MusicVideo:
    def __init__(self, video_dir, audio_track):
        """
        
        """
        self.video_groups = VideoGroup.make_clip_groups(video_dir)
        self.audio_track = audio_track
        self.all_video_clips = list(itertools.chain.from_iterable(
            map(lambda x: x.video_clips, self.video_groups.values())
        ))
        
    def pick_video(self, interval):
        clips = self.all_video_clips
        clip_number = random.randint(0, len(clips) - 1)

        clip = clips[clip_number]
        total_frames = clip.get_total_frames()
        start_frame = random.randint(0, total_frames - interval)
        
        return clip, start_frame, start_frame + interval


    def write(self, output_path: str = "output.avi"):
        y, sr = librosa.load(self.audio_track)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("processed_video.avi", fourcc, 30, (1920, 1080))

        num_clips = len(beats) // 4
        flip_frame = 0
        
        for clip_number in range(num_clips):
            flip_frame = (flip_frame + 1) % 2
            beat_times = beats[clip_number: clip_number + 4]
            interval = beat_times[-1] - beat_times[0]
            video_clip, start_frame, end_frame = self.pick_video(interval)

            def frame_effect(frame):
                return cv2.flip(frame, flip_frame)

            video_clip.write_frames(
                start_frame=start_frame,
                end_frame=end_frame,
                out=out,
                frame_effect=frame_effect
            )
            
            
        out.release()
        subprocess.call([
            "ffmpeg",
            "-y",
            "-i",
            "processed_video.avi",
            "-i",
            f"{self.audio_track}",
            "-map",
            "0:0",
            "-map",
            "1:0",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            f"{output_path}"
        ])
        
