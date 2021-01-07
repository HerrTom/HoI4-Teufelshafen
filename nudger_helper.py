import sys, os
import os.path
import glob
from shutil import copyfile
from PyQt5 import QtGui, QtCore, QtWidgets

class mainwindow(QtWidgets.QMainWindow):
    def main(self):
        super().__init__(self)
        self.state_path = os.path.realpath('../../history/states/')
        self.loc_path = os.path.realpath('../../localisation/')
        self.map_path = os.path.realpath('../../map/')

        self.state_watcher = QtCore.QFileSystemWatcher()
        self.state_watcher.addPath(self.state_path)
        # State watcher
        self.state_watcher.directoryChanged.connect(self.state_dir_changed)

        self.loc_watcher = QtCore.QFileSystemWatcher()
        self.loc_watcher.addPath(self.loc_path)
        # loc watcher
        self.loc_watcher.directoryChanged.connect(self.loc_dir_changed)

        self.map_watcher = QtCore.QFileSystemWatcher()
        self.map_watcher.addPath(self.map_path)
        # map watcher
        self.map_watcher.directoryChanged.connect(self.map_dir_changed)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.handle_timer)

        self.copy_states_flag = False
        self.copy_loc_flag = False
        self.copy_map_flag = False

    def copy_file(self, path, to_dir, extension='txt'):
        # files to copy
        files = glob.glob(path+'/*.'+extension)
        for f in files:
            dest = to_dir+os.path.basename(f)
            print(f, dest)
            copyfile(f, dest)

    def copy_states(self):
        self.copy_file(self.state_path, './history/states/', 'txt')

    def state_dir_changed(self):
        print('States Changed')
        self.timer.start()
        self.copy_states_flag = True

    def copy_loc(self):
        self.copy_file(self.loc_path, './localisation/', 'yml')
    
    def loc_dir_changed(self):
        print('Localisation Changed')
        self.timer.start()
        self.copy_loc_flag = True

    def copy_map(self):
        self.copy_file(self.loc_path, './map/', 'txt')
    
    def map_dir_changed(self):
        print('Map Dir Changed')
        self.timer.start()
        self.copy_map_flag = True

    
    def handle_timer(self):
        if self.copy_states_flag:
            self.copy_states_flag = False
            self.copy_states()
        if self.copy_loc_flag:
            self.copy_loc_flag = False
            self.copy_loc()
        if self.copy_map_flag:
            self.copy_map_flag = False
            self.copy_map()


def on_dir_changed(path):
    print(path)


if __name__ == '__main__':
    # change path
    os.chdir(os.path.dirname(sys.argv[0]))
    # Run the watcher
    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.main()
    sys.exit(app.exec_())
