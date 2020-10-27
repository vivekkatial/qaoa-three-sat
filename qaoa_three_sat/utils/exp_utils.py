"""Utility functions for running experiments

Author: Vivek Katial
"""

import argparse
import contextlib
import tempfile
import shutil


def str2bool(v):
    """Function to convert argument into ArgParse to be boolean

    :param v: Input from user
    :type v: str
    :returns: True or False of boolean type
    :rtype: {bool}
    :raises: argparse
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


@contextlib.contextmanager
def make_temp_directory():
    """Make temp directory """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
