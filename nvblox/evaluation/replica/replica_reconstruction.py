#!/usr/bin/python3

#
# Copyright 2022 NVIDIA CORPORATION
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse

import subprocess
from pathlib import Path
from typing import Tuple

import replica


def replica_reconstruction(dataset_path: Path,
                           output_root_path: Path = None,
                           fuse_replica_binary_path: Path = None) -> Tuple[Path, Path]:
    """Builds a reconstruction for the replica dataset

    Args:
        dataset_path (Path): Path to the root folder of the dataset.

        output_root_path (Path, optional): Root of the directory where to dump the results.
            Note we create a subfolder below this directory named as the dataset name.
            If no argument is given, an output folder is created below the evaluation
            scripts. Defaults to None.

        fuse_replica_binary_path (Path, optional): The path to the binary which does the
            fusion. Defaults to the build folder. Defaults to None.

    Raises:
        Exception: If the binary is not found.

    Returns:
        Tuple[Path, Path]: Path to the reconstructed mesh + Path to the reconstructed ESDF. 
    """
    dataset_name = replica.get_dataset_name_from_dataset_root_path(
        dataset_path)

    if fuse_replica_binary_path is None:
        fuse_replica_binary_path = replica.get_default_fuse_replica_binary_path()
    if not fuse_replica_binary_path.is_file():
        raise Exception(f"Cant find binary at:{fuse_replica_binary_path}")

    output_dir = replica.get_output_dir(dataset_name, output_root_path)
    reconstructed_mesh_path = output_dir / 'reconstructed_mesh.ply'
    reconstructed_esdf_path = output_dir / 'reconstructed_esdf.ply'

    # Reconstruct the mesh + esdf
    print(f"Running executable at:\t{fuse_replica_binary_path}")
    print(f"On the dataset at:\t{dataset_path}")
    print(f"Outputting mesh at:\t{reconstructed_mesh_path}")
    print(f"Outputting esdf at:\t{reconstructed_esdf_path}")
    mesh_output_path_flag = "--mesh_output_path"
    esdf_output_path_flag = "--esdf_output_path"
    subprocess.run([f"{fuse_replica_binary_path}", f"{dataset_path}",
                   mesh_output_path_flag, f"{reconstructed_mesh_path}",
                   esdf_output_path_flag, f"{reconstructed_esdf_path}"])

    return reconstructed_mesh_path, reconstructed_esdf_path


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="""Reconstruct a mesh from the replica dataset and test it 
                       against ground-truth geometry.""")

    parser.add_argument("dataset_path", type=Path,
                        help="Path to the dataset root folder.")
    parser.add_argument("--output_root_path", type=Path,
                        help="Path to the directory in which to save results.")
    parser.add_argument("--fuse_replica_binary_path", type=Path,
                        help="Path to the fuse_replica binary. If not passed we search the standard build folder location.")

    args = parser.parse_args()

    replica_reconstruction(args.dataset_path,
                           output_root_path=args.output_root_path,
                           fuse_replica_binary_path=args.fuse_replica_binary_path)
