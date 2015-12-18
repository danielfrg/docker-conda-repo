import os
import sys
import time
import subprocess

# from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler


class CondaChannelHandler(FileSystemEventHandler):
    channel_dir = None
    subdirs = ("linux-32", "linux-64", "osx-64", "osx-32", "win-64", "win-32",
               "linux-armv6l", "linux-armv7l")

    def on_modified(self, event):
        print('New file on:', event.src_path)
        diff = event.src_path[len(self.channel_dir) + 1:]
        parts = splitpath(diff)
        if len(parts) > 0 and parts[0] in self.subdirs:
            plat_arch = parts[0]
            self.index(plat_arch)

    def index_all(self):
        for subdir in self.subdirs:
            path = os.path.realpath(os.path.join(self.channel_dir, subdir))
            if os.path.exists(path):
                self.index(subdir)

    def index(self, plat_arch):
        dir_ = os.path.join(channel_dir, plat_arch)
        cmd = ["conda", "index", dir_]
        subprocess.call(cmd)


def splitpath(path):
    """
    Split (recursively) a path into parts
    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


if __name__ == "__main__":
    default_channel_dir = os.path.join(os.getcwd(), "channel")
    default_channel_dir = os.path.realpath(default_channel_dir)
    channel_dir = sys.argv[1] if len(sys.argv) > 1 else default_channel_dir

    handler = CondaChannelHandler()
    handler.channel_dir = channel_dir

    handler.index_all()

    observer = Observer()
    observer.schedule(handler, channel_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
