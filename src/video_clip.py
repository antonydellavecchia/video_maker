import cv2
import numpy as np

class VideoClip:
    def __init__(self, path: str):
        """
        Defines the class for qorking with a video clip
        """
        self.path = path
        self.total_frames = None
        
    def play(self):
        self.write_frames(show_frames=True)

    def get_total_frames(self):
        if not self.total_frames:
            cap = cv2.VideoCapture(self.path)
            self.total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            cap.release()

        return self.total_frames
    
    def write_frames(
        self,
        start_frame: int = 0,
        end_frame = float("inf"),
        out: cv2.VideoWriter = None,
        show_frames: bool = False,
        frame_effect = lambda x: x
    ):
        cap = cv2.VideoCapture(self.path)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if end_frame > total_frames:
            extra_time = (end_frame % total_frames)
            end_frame -= extra_time
            start_frame -= extra_time

        if start_frame < 0:
            start_frame = 0

        # check for valid frame number
        if 0 <= start_frame <= total_frames:
            # set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frame_number = start_frame
        while True:
            frame_number += 1
            ret, frame = cap.read()

            #print(frame_number, end_frame)
            if ret and frame_number < end_frame:
                frame = frame_effect(frame)

                if show_frames:
                    cv2.imshow('frame', frame)
                
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break
            else:
                break
            
            if out:
                out.write(frame)

        # Release everything if job is finished
        cap.release()

        if show_frames:
            cv2.destroyAllWindows()
