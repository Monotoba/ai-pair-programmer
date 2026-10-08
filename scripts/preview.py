"""Render a safe sample-data GUI preview without making an API request."""
import argparse
import os
from pathlib import Path
import tempfile


def render_preview(output):
    # Isolate preview files from real settings/history. Qt must be selected before
    # QApplication creation; the caller can use QT_QPA_PLATFORM=offscreen.
    from PyQt5.QtWidgets import QApplication
    from aipairprogrammer.ai_pair_programmer import AIPairProgrammer

    previous = os.environ.get('AIPAIRPROGRAMMER_DATA_DIR')
    with tempfile.TemporaryDirectory() as directory:
        os.environ['AIPAIRPROGRAMMER_DATA_DIR'] = directory
        widget = None
        try:
            application = QApplication.instance() or QApplication([])
            widget = AIPairProgrammer()
            widget.model_combo_box.setCurrentText('your-account-model-id')
            widget.query_edit.setPlainText('How can I make a Python function easier to test?')
            widget.response_edit.setPlainText(
                'Sample response — preview only; no API request was sent.\n\n'
                'Separate calculations from file and network access. Pass '
                'dependencies as arguments to make tests predictable.\n\n'
                'def total_with_tax(subtotal, tax_rate):\n'
                '    return subtotal * (1 + tax_rate)\n\n'
                'Test ordinary inputs, zero values, and documented error cases.'
            )
            widget.request_status.setText('Offline preview · sample text · no API request')
            widget.send_button.setEnabled(False)
            widget.show()
            application.processEvents()
            output = Path(output)
            output.parent.mkdir(parents=True, exist_ok=True)
            if not widget.grab().save(str(output), 'PNG'):
                raise OSError('Could not save preview image.')
        finally:
            if widget is not None:
                widget.close()
                widget.deleteLater()
                application.processEvents()
            if previous is None:
                os.environ.pop('AIPAIRPROGRAMMER_DATA_DIR', None)
            else:
                os.environ['AIPAIRPROGRAMMER_DATA_DIR'] = previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='docs/images/desktop-preview.png')
    args = parser.parse_args()
    render_preview(args.output)


if __name__ == '__main__':
    main()
