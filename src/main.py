#%%
import os

from src.change_detector import ChangeDetector
from src.playlists import LivePlaylists

print(f'from main cwd: {os.getcwd()}')
live_playlists = LivePlaylists()

cd = ChangeDetector(live_playlists) 
cd.check_for_changes()