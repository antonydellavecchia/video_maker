from video_clip import VideoClip
from pathlib import Path


class VideoGroup:
    @staticmethod
    def make_clip_groups(video_dir):
        video_dir_path = Path(video_dir)
        video_groups = {}
    
        for child in video_dir_path.iterdir():
            if child.is_dir():
                group_name = child.name
                vid_group = VideoGroup(child, group_name)
                video_groups[group_name] = vid_group

        return video_groups

    def __init__(self, video_dir: Path, name: str):
        """
        Creates video group for all videos in same dir
        """
        self.name = name
        self.video_clips = [
            VideoClip(str(x)) for x in video_dir.iterdir() if x.is_file()
        ]
        
    def play_all(self):
        for vid in self.video_clips:
            vid.write_frames(show_frames=True)

    
