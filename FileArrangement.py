import os
import glob

from Variables import*
from shutil import copyfile

class FileArrangement:

    def __init__(self, t_path):
        self.target_path=t_path
        # self.var=Variables()
        self.get_source_code()

    def get_source_code(self):
        dir_names=os.listdir(self.target_path)

        has_bky_file=False
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                if file.endswith(".bky"):
                    has_bky_file=True
                    source_path=os.path.join(root, file)
                    xml_file=source_path.replace('.bky', '.xml')
                    copyfile(source_path, xml_file)

        return has_bky_file



