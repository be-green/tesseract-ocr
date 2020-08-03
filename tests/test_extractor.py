import pytest
import os
import logging
import fitz
from pathlib import Path
from kelloggrs import extract

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def extractor_logger(config):
    logger = logging.getLogger("cafrs")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh = logging.FileHandler(f"{config['out_path']}/extract.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    return logger


def test_extract_script(script_runner):
    ret = script_runner.run("extract_pages", "-h")
    assert ret.success
    assert ret.stdout != ""
    assert ret.stderr == ""


def test_extract_pdfs(config):
    in_path = Path(dir_path) / f"../{config['in_path']}"
    extract.extract_pdfs(in_path, page_nums={0, 1, 2, 3, 4})


def test_extract_pages(config):
    in_path = Path(dir_path) / f"../{config['in_path']}"
    out_path = Path(dir_path) / f"../{config['out_path']}"
    pdf_file = in_path / config["test_pdf_1"]
    pages = extract.extract_pages(pdf_file)
    assert len(pages[1]) == 9

    pages = extract.extract_pages(pdf_file, page_nums={1, 2, 3})
    assert len(pages[1]) == 3
