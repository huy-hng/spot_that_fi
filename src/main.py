#%%
print('from main')
from src.change_detector import ChangeDetector
from src.playlists import Playlists

live_playlists = Playlists().playlists

cd = ChangeDetector(live_playlists) 
cd.check_for_changes()