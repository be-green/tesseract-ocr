import pytest
import os
import logging
import fitz
from pathlib import Path
from kelloggrs import process


dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def process_logger(config):
    logger = logging.getLogger("process")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh = logging.FileHandler(f"{dir_path}/{config['in_path']}/process.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    return logger


def test_process_script(script_runner):
    ret = script_runner.run("process_pages", "-h")
    assert ret.success
    assert ret.stdout != ""
    assert ret.stderr == ""


def test_process_image(config):
    in_path = Path(dir_path) / f"{config['in_path']}"
    image_files = list((in_path / "9999999997-12-008041-index").glob("*.png"))
    text = process.process_image(image_files[3])
    assert "Full Name" in text
    assert "Address" in text

