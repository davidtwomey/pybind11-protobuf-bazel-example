#
# Copyright 2020 the authors listed in CONTRIBUTORS.md
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import posixpath
import re
import shutil
import sys

from distutils import sysconfig
import setuptools
from setuptools.command import build_ext


HERE = os.path.dirname(os.path.abspath(__file__))


PROJECT_NAME = "my_package"
PACKAGE_NAME = "my_extension"
PROTO_FILE = "example_pb2.py"


class BazelExtension(setuptools.Extension):
    """A C/C++ extension that is defined as a Bazel BUILD target."""

    def __init__(self, name, bazel_target):
        self.bazel_target = bazel_target
        self.relpath, self.target_name = posixpath.relpath(bazel_target, "//").split(":")
        setuptools.Extension.__init__(self, name, sources=[])


class BuildBazelExtension(build_ext.build_ext):
    """A command that runs Bazel to build a C/C++ extension."""

    def run(self):
        for ext in self.extensions:
            self.bazel_build(ext)
        build_ext.build_ext.run(self)

    def bazel_build(self, ext):
        
        # TODO - detect any workspace file, whether has .bazel extension or not
        with open("WORKSPACE.bazel", "r") as f:
            workspace_contents = f.read()

        with open("WORKSPACE.bazel", "w") as f:
            f.write(
                re.sub(
                    r'(?<=path = ").*(?=",  # May be overwritten by setup\.py\.)',
                    sysconfig.get_python_inc().replace(os.path.sep, posixpath.sep),
                    workspace_contents,
                )
            )

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        bazel_argv = [
            "bazel",
            "build",
            ext.bazel_target,
            "--symlink_prefix=" + os.path.join(self.build_temp, "bazel-"),
            "--compilation_mode=" + ("dbg" if self.debug else "opt"),
        ]
        self.spawn(bazel_argv)

        if not ext.name.startswith("_"):
            ext.name = "_" + ext.name
        shared_lib_ext = ".so"
        shared_lib = ext.name + shared_lib_ext
        ext_bazel_bin_path = os.path.join(self.build_temp, "bazel-bin", ext.relpath, shared_lib)

        ext_dest_path = self.get_ext_fullpath(ext.name)
        ext_dest_dir = os.path.dirname(ext_dest_path)

        if not os.path.exists(ext_dest_dir):
            os.makedirs(ext_dest_dir)
        shutil.copyfile(ext_bazel_bin_path, ext_dest_path)

        package_dir = os.path.join(ext_dest_dir, PACKAGE_NAME)
        if not os.path.exists(package_dir):
            os.makedirs(package_dir)

        shutil.copyfile(
            f"{PROJECT_NAME}/python/__init__.py", os.path.join(package_dir, "__init__.py")
        )

        proto_file = PROTO_FILE
        proto_bazel_bin_path = os.path.join(
            self.build_temp,
            "bazel-bin",
            PROJECT_NAME,
            "proto",
            "example_python_proto_pb",
            PROJECT_NAME,
            "proto",
            proto_file,
        )
        print("proto path ", proto_bazel_bin_path)
        shutil.copyfile(proto_bazel_bin_path, os.path.join(package_dir, proto_file))


setuptools.setup(
    name="my.package",
    version="v0.0.1",
    description="Example PyBind11 Setup.py usage",
    python_requires=">=3.6",
    package_dir={"": f"{PROJECT_NAME}/python"},
    cmdclass=dict(build_ext=BuildBazelExtension),
    ext_modules=[
        BazelExtension(PACKAGE_NAME, f"//{PROJECT_NAME}/python:{PACKAGE_NAME}",)
    ],
    zip_safe=False,
    install_requires=["protobuf",],
)
