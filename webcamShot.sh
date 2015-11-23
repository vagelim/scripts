#!/bin/bash
vlc -I dummy v4l2:///dev/video0 --video-filter scene --no-audio --scene-path /tmp --scene-prefix webcam --scene-format png vlc://quit --run-time=1
