from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")
