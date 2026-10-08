"""Verify the wheel contains the app and can open a widget outside checkout."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

wheel = next(Path('dist').glob('*.whl')).resolve()
subprocess.run([sys.executable, '-m', 'pip', 'install', '--force-reinstall',
                '--no-deps', str(wheel)], check=True)
env = dict(os.environ, QT_QPA_PLATFORM='offscreen')
env.pop('PYTHONPATH', None)
with tempfile.TemporaryDirectory() as cwd:
    subprocess.run([sys.executable, '-c',
        'from PyQt5.QtWidgets import QApplication; '
        'from aipairprogrammer.ai_pair_programmer import AIPairProgrammer, QueryWorker; '
        'from aipairprogrammer.__main__ import main; '
        'app = QApplication([]); widget = AIPairProgrammer(); '
        'assert widget._request is None; assert not widget._request_cancelled; '
        'widget.load_history(); widget.historian.add("question", "answer"); '
        'widget.save_history(); assert widget.historian.count() == 1; '
        'widget.close(); print("Installed wheel GUI smoke test passed")'],
        cwd=cwd, env=env, check=True)
