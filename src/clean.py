import shutil
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from utils.in_out import read_json


class Organizer:
    """
    This class is used to organize files in a directory by
    moving files into directories based on their extension
    """
    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exists.")

        json_ext = read_json(DATA_DIR / "extensions.json") #--> dir:[ext1, ext2,..]
        self.file_type_destination = {}
        for dir_val, ext_keys in json_ext.items():
            for ext in ext_keys:
                self.file_type_destination[ext] = dir_val

    def __call__(self):
        """
        This class is used to organize files in a directory by
        moving files into directories based on their extension
        """

        logger.info(f"Organizing files in {self.directory}...")

        for file_path in self.directory.iterdir():
            try:

                #ignore hidden files:
                if file_path.name.startswith('.'):
                    continue

                #ignore directories
                if file_path.is_dir():  #--> It only grabs the non-directory files. If it is a directory it goes back to the start of loop
                    continue
                # Method 1: Rename existing file



                if file_path.suffix not in self.file_type_destination:
                    DEST_DIR = self.directory / 'others_'
                else:
                    DEST_DIR = self.directory / self.file_type_destination[file_path.suffix]

                DEST_DIR.mkdir(exist_ok = True)
                logger.info(f"Moving {file_path} to {DEST_DIR} ")

                # move file to new destination

                shutil.move(str(file_path), str(DEST_DIR))

            except shutil.Error as e:

                dest_file = DEST_DIR / file_path.name
                if dest_file.exists():
                    logger.info(f"{file_path.name} already exist in {DEST_DIR} so we put another copy. ")
                    new_file_stem = file_path.stem + "(Copy)"
                    new_file_name = new_file_stem + file_path.suffix
                    new_file_path = self.directory / new_file_name

                shutil.move(str(file_path) , str(new_file_path))
                shutil.move(str(new_file_path) , str(DEST_DIR))





if __name__ ==  "__main__":
    org_files = Organizer('/mnt/c/Users/Asronic/Downloads')
    org_files()
    logger.info("Done")
