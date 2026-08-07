"""
Terminal Pet Society - Command Watcher
Monitors shell activity and feeds commands to the pet for learning.
"""

import os
import time
import threading
from typing import Optional, Callable


class CommandWatcher:
    """
    Watches shell history files for new commands.
    Supports bash (.bash_history) and zsh (.zsh_history).
    """
    
    def __init__(self, callback: Callable[[str], Optional[str]]):
        self.callback = callback
        self.history_file = self._find_history_file()
        self.last_position = 0
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.poll_interval = 2.0  # seconds
    
    def _find_history_file(self) -> Optional[str]:
        """Find the shell history file."""
        candidates = [
            os.path.expanduser("~/.bash_history"),
            os.path.expanduser("~/.zsh_history"),
            os.path.expanduser("~/.history"),
            os.path.expanduser("~/.local/share/fish/fish_history"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None
    
    def _read_new_commands(self):
        """Read new commands from history file since last check."""
        if not self.history_file or not os.path.exists(self.history_file):
            return
        
        try:
            with open(self.history_file, "r", errors="ignore") as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
            
            for line in new_lines:
                cmd = line.strip()
                if cmd and not cmd.startswith("#"):
                    self.callback(cmd)
        except Exception:
            pass  # Silently ignore file read errors
    
    def _watch_loop(self):
        """Main watch loop running in a thread."""
        # Set initial position
        if self.history_file and os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", errors="ignore") as f:
                    f.seek(0, 2)  # seek to end
                    self.last_position = f.tell()
            except Exception:
                self.last_position = 0
        
        while self.running:
            self._read_new_commands()
            time.sleep(self.poll_interval)
    
    def start(self):
        """Start watching in a background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the watcher thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None


def get_recent_commands(limit: int = 20) -> list:
    """Get recent shell commands (for initial pet setup)."""
    history_files = [
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.zsh_history"),
        os.path.expanduser("~/.history"),
    ]
    
    commands = []
    for hf in history_files:
        if os.path.exists(hf):
            try:
                with open(hf, "r", errors="ignore") as f:
                    lines = f.readlines()
                # Take last N non-empty lines
                for line in reversed(lines):
                    cmd = line.strip()
                    if cmd and len(commands) < limit:
                        commands.append(cmd)
                if len(commands) >= limit:
                    break
            except Exception:
                pass
    
    return list(reversed(commands))
