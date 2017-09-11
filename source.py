#!/usr/bin/env python2.7
from __future__ import print_function

__DOCKER_IMAGE__ = 'docker.io/autodesk/moldesign:moldesign_complete-0.7.4a2'

import moldesign
import parmed
import openbabel, pybel
from simtk.openmm import app as openmmapp
import pyscf

STRINGTYPES = {'pdb': 'pdb',
               'mmcif': 'mmcif',
               'cif': 'mmcif',
               'sdf': 'sdf',
               'mol2': 'mol2',
               'xyz': 'xyz',
               'smi': 'smi',
               'smiles': 'smi',
               'inchi': 'inchi',
               'iupac': 'iupac',
               'name': 'iupac',
               'pdbcode': 'pdbcode',
               None: None}

PYTHONNAMES = {moldesign.Molecule: 'mdt',
               parmed.Structure: 'parmed',
               openbabel.OBMol: 'openbabel',
               pybel.Molecule: 'openbabel',
               openmmapp.Topology: 'openmm',
               pyscf.gto.Mole: 'pyscf'}

PARSERS = {'*': moldesign.read,
           'smi': moldesign.from_smiles,
           'inchi': moldesign.from_inchi,
           'iupac': moldesign.from_name,
           'pdbcode': moldesign.from_pdb}

EXPORTERS = {'*': moldesign.write,
             'mdt': moldesign.Molecule,
             'openbabel': moldesign.interfaces.mol_to_pybel,
             'openmm': moldesign.interfaces.mol_to_topology,
             'parmed': moldesign.interfaces.mol_to_parmed,
             'pyscf': moldesign.interfaces.mol_to_pyscf}

IMPORTERS = {parmed.Structure: moldesign.interfaces.parmed_to_mdt,
             pybel.Molecule: moldesign.interfaces.pybel_to_mol,
             openmmapp.Topology: moldesign.interfaces.topology_to_mol}


def convert(data, output_type, input_type=None):
    """ Flexibly convert between a variety of molecular file formats and python objects

    Args:
        data (str): data to convert (may be file contents)
        output_type (str or type): Type to convert to
        input_type (str or type): (optional) type of the input data. If not passed,
                 will check smi, inchi, and iupac, and pdbcode

    Returns:
        (str or object): contents of requested file, or requested python object
    """

    input_type = PYTHONNAMES.get(input_type, input_type)
    input_type = STRINGTYPES[input_type]

    mol = import_molecule(data, input_type)
    output = export_molecule(mol, output_type)
    return output


def import_molecule(data, input_type):
    if isinstance(data, basestring):
        if input_type is None:
            mdtmol = _infer_string_type(data)
        elif input_type in PARSERS:
            mdtmol = PARSERS[input_type](data)
        else:
            mdtmol = PARSERS['*'](data, format=input_type)

    else:
        if input_type is None:
            input_type = PYTHONNAMES[data.__class__]

        mdtmol = PARSERS[input_type](data, input_type)

    return mdtmol


def export_molecule(mol, output_type):
    if output_type not in EXPORTERS:
        return EXPORTERS['*'](mol, format=output_type)
    else:
        return EXPORTERS[output_type](mol)



def _object_to_mdt(data, input_type):
    raise NotImplementedError


def _infer_string_type(data):
    if len(data) == 4 and data[0].isdigit():
        try:
            m = moldesign.from_pdb(data)
        except Exception as e:
            print('Not recognized as PDB ID', e)
        else:
            print('Reading molecule as PDB ID "%s"' % data)
            return m

    try:
        m = moldesign.from_smiles(data)
    except Exception as e:
        print('Not recognized as SMILES name', e)
    else:
        print('Reading molecule as smiles "%s"' % data)
        return m

    try:
        m = moldesign.from_name(data)
    except Exception as e:
        print('Not recognized as IUPAC name', e)
    else:
        print('Reading molecule as IUPAC name "%s"'%data)
        return m

    try:
        m = moldesign.from_inchi(data)
    except Exception as e:
        print('Not recognized as INCHI string', e)
    else:
        print('Reading molecule as inchi string "%s"'%data)
        return m

    raise ValueError("Failed to parse input data '%s' as PDB id, SMILES, IUPAC, or INCHI" %
                     data)

