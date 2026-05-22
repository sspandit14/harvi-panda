from dataclasses import dataclass
from typing import Tuple
import numpy as np
import pyrealsense2 as rs

@dataclass
class FrameBundle:
    color: np.ndarray
    depth: np.ndarray
    timestamp_s: float

class D435_Helper:
    def __init__(self, width:int=640, height:int=480, fps:int=15):
        self.width = width
        self.height = height
        
        self.pipeline = rs.pipeline()

        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.color, width, height, rs.format.z16, fps)

        self.align = rs.align(rs.stream.color)

        self.profile = None 
        self.camera_started = False

    def start(self) -> None:
        if self.camera_started:
            return
        
        self.profile = self.pipeline.start(self.config)
        self.camera_started = True

    def stop(self) -> None:
        if not self.camera_started:
            return
        
        self.pipeline.stop()
        self.camera_started = False

    def camera_parameters(self) -> Tuple[float, float, float, float]:
        # return (fx, fy, cx, cy) for color stream
        if self.profile is None:
            print("Camera not started, can't read parameters... bozo...")
            return

        color_stream = self.profile.get_stream(rs.stream.color).as_video_stream_profile()
        intrinsics = color_stream.get_intrinsics()

        return (intrinsics.fx, intrinsics.fy, intrinsics.ppx, intrinsics.ppy)


    def get_frames(self):
        if not self.camera_started:
            print ("Need to start the camera before calling get_frame()... bozo...")
            return
        
        frames = self.pipeline.wait_for_frames()
        frames = self.align.process(frames)

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            print("Error in getting color or depth frame... bozo...")
            return
        
        color = np.asanyarray(color_frame.get_data())
        depth = np.asanyarray(depth_frame.get_data())

        timestamp_s = color_frame.get_timestamp() / 1000.0

        return FrameBundle(color=color, depth=depth, timestamp_s=timestamp_s)