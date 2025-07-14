import omni.ext
import omni.ui as ui
from .ui import SpawnControlsUI  
class MyReplicatorExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[MyReplicatorExtension] Startup")
        self._window = ui.Window("Synthetic Data Generator", width=400, height=400)
        with self._window.frame:
            self.ui = SpawnControlsUI()

    def on_shutdown(self):
        print("[MyReplicatorExtension] Shutdown")
        self._window = None