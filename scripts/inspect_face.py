import os
import pprint
import subprocess

import freetypybind as ft
import freetypybind.query_face


def _fc_paths():
    return sorted(subprocess.run(["fc-list", "--format=%{file}\n"],
                                 stdout=subprocess.PIPE).stdout.splitlines())


def names(path: str, *, keys_only: bool = False):
    if path == ":all:":
        for path in _fc_paths():
            names(path, keys_only=keys_only)
        return
    for face_index in range(ft.Face(path, 0).num_faces):
        face = ft.Face(path, face_index)
        for key, value in face.get_sfnt_name_table().items():
            if keys_only:
                print(*key)
            else:
                print("\n{}\n{}".format(" ".join(map(str, key)), value))


def query(path: str):
    if path == ":all:":
        for path in _fc_paths():
            query(path)
        return
    for face_index in range(ft.Face(path, 0).num_faces):
        face = ft.Face(path, face_index)
        pprint.pprint(ft.query_face.query_face(face))


if __name__ == "__main__":
    import defopt
    defopt.run([names, query])
