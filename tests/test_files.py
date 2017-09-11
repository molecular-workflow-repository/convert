import pickle
from pathlib import Path

import pytest
from molflow.loader import load_workflow



@pytest.fixture
def workflow():
    return load_workflow('convert')

@pytest.mark.parametrize('output_format', ['pdb', 'mmcif', 'smi', 'inchi'])
def test_file_to_file(workflow, output_format):
    pass