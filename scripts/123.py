import hou

start = 1001
end = 1100
hou.playbar.setFrameRange(start, end)
hou.playbar.setPlaybackRange(start, end)
hou.setFrame(1001)