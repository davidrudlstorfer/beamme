# The MIT License (MIT)
#
# MeshPy: A general purpose 3D beam finite element input generator
# Copyright (c) 2018-2025 MeshPy Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""This file defines the base volume element in MeshPy."""

import numpy as np
import vtk

from meshpy.core.element import Element
from meshpy.core.vtk_writer import add_point_data_node_sets


class VolumeElement(Element):
    """A base class for a volume element."""

    # This class variables stores the information about the element shape in
    # vtk. And the connectivity to the nodes.
    vtk_cell_type = None
    vtk_topology: list = []

    def __init__(self, nodes=None, dat_pre_nodes="", dat_post_nodes="", **kwargs):
        super().__init__(nodes=nodes, material=None, **kwargs)
        self.dat_pre_nodes = dat_pre_nodes
        self.dat_post_nodes = dat_post_nodes

    def _get_dat(self):
        """Return the dat line for this element."""

        # String with the node ids.
        nodes_string = ""
        for node in self.nodes:
            nodes_string += f"{node.i_global} "

        # Return the dat line.
        return (
            f"{self.i_global} {self.dat_pre_nodes} {nodes_string} {self.dat_post_nodes}"
        )

    def get_vtk(self, vtk_writer_beam, vtk_writer_solid, **kwargs):
        """Add the representation of this element to the VTK writer as a
        quad."""

        # Check that the element has a valid vtk cell type.
        if self.vtk_cell_type is None:
            raise TypeError(f"vtk_cell_type for {type(self)} not set!")

        # Dictionary with cell data.
        cell_data = {}

        # Dictionary with point data.
        point_data = {}

        # Array with nodal coordinates.
        coordinates = np.zeros([len(self.nodes), 3])
        for i, node in enumerate(self.nodes):
            coordinates[i, :] = node.coordinates

        # Add the node sets connected to this element.
        add_point_data_node_sets(point_data, self.nodes)

        # Add cell to writer.
        indices = vtk_writer_solid.add_points(coordinates, point_data=point_data)
        vtk_writer_solid.add_cell(
            self.vtk_cell_type, indices[self.vtk_topology], cell_data=cell_data
        )


class VolumeHEX8(VolumeElement):
    """A HEX8 volume element."""

    vtk_cell_type = vtk.vtkHexahedron
    vtk_topology = list(range(8))


class VolumeTET4(VolumeElement):
    """A TET4 volume element."""

    vtk_cell_type = vtk.vtkTetra
    vtk_topology = list(range(4))


class VolumeTET10(VolumeElement):
    """A TET10 volume element."""

    vtk_cell_type = vtk.vtkQuadraticTetra
    vtk_topology = list(range(10))


class VolumeHEX20(VolumeElement):
    """A HEX20 volume element."""

    vtk_cell_type = vtk.vtkQuadraticHexahedron
    vtk_topology = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        16,
        17,
        18,
        19,
        12,
        13,
        14,
        15,
    ]


class VolumeHEX27(VolumeElement):
    """A HEX27 volume element."""

    vtk_cell_type = vtk.vtkTriQuadraticHexahedron
    vtk_topology = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        16,
        17,
        18,
        19,
        12,
        13,
        14,
        15,
        24,
        22,
        21,
        23,
        20,
        25,
        26,
    ]
