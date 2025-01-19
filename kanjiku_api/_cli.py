import sys
import argparse

from kanjiku_api import __version__


def cli() -> str:
    """This Function is repsonsible for the command line interface.

    Returns:
        str: Path to the config File
    """
    parser = argparse.ArgumentParser(
        prog="kanjiku_api",
        description="This will start the Kanjiku API",
    )
    parser.add_argument(
        "--config",
        "-c",
        help="path to the configuration file",
        default="./config.toml",
        type=str,
    )
    parser.add_argument(
        "--version", "-v", help="start the application in debug mode", action="store_true"
    )

    inputvars = parser.parse_args()

    if inputvars.version:
        print(__version__)
        sys.exit(0)

    print(
        fr"""  _  __            _ _ _          
 | |/ /__ _ _ __  (_|_) | ___   _ 
 | ' // _` | '_ \ | | | |/ / | | |
 | . \ (_| | | | || | |   <| |_| |
 |_|\_\__,_|_| |_|/ |_|_|\_\\__,_|
                |__/                  
kanjiku_api: {__version__}
"""
    )

    return inputvars.config
