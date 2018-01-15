import os
import pprint

import freetypybind as ft
import freetypybind.query_face


def names(path: str):
    face = ft.Face(os.fsencode(path), 0)
    for face_index in range(face.num_faces):
        face = ft.Face(os.fsencode(path), face_index)
        for key, value in face.get_sfnt_name_table().items():
            print()
            print(*key)
            print(value)


def query(path: str):
    face = ft.Face(os.fsencode(path), 0)
    for face_index in range(face.num_faces):
        face = ft.Face(os.fsencode(path), face_index)
        pprint.pprint(ft.query_face.query_face(face))


if __name__ == "__main__":
    import defopt
    defopt.run([names, query])
