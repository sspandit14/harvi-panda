from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import cv2
from pupil_apriltags import Detector

@dataclass
class TagPose:
    tag_id: int
    position: np.ndarray
    timestamp_s: float
    center: np.ndarray
    corners: np.ndarray
    decision_margin: float
    hamming: int

class AprilTagHelper:
    def __init__(self, camera_params: Tuple[float, float, float, float], tag_size_m: float, family: str = "tag36h11",):
        self.camera_params = camera_params
        self.tag_size_m = tag_size_m
        self.detector = Detector(families=family)

    def detect(self, color_bgr: np.ndarray, timestamp_s: float, target_id: Optional[int] = None):
        gray = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2GRAY)

        detections = self.detector.detect(gray, estimate_tag_pose = True, camera_params = self.camera_params, tag_size = self.tag_size_m)

        results = []

        for det in detections:
            if target_id is not None and det.tag_id != target_id:
                continue

            results.append(
                TagPose(
                    tag_id=det.tag_id,
                    position=np.array(det.pose_t, dtype=np.float64).reshape(3),
                    timestamp_s=timestamp_s,
                    center=np.array(det.center, dtype=np.float64),
                    corners=np.array(det.corners, dtype=np.float64),
                    decision_margin=float(det.decision_margin),
                    hamming=int(det.hamming),
                )
            )
        
        return results