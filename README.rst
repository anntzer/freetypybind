pybind11 bindings to FreeType
=============================

Mostly developed for Matplotlib.

Use
---

.. code-block:: python

   import freetypybind as ft
   face = ft.Face("/path/to/font", index=0)
   face.set_char_size(pt_size=12, dpi=100)
   bitmap = ft.Layout.simple("hello, world", face, ft.Load.DEFAULT).render()

   from matplotlib import pyplot as plt
   plt.imshow(bitmap, origin="upper", cmap="gray_r")
   plt.show()
