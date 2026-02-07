# dvng_gridfinity

Based on [Gridfinity | The modular, open-source grid storage system](https://www.youtube.com/watch?v=ra_9zU-mnl8), by [Zack Freedman's](https://www.youtube.com/@ZackFreedman). As it is an open design I belive it shall be possible to use only open tools for its development.

Check [the gridfinity official especification](https://gridfinity.xyz/specification/) to know more about the design. My implementation may not be strictly compliant with it, so be careful integrating it with your own or 3rd party designs, they may not work.

There is a bibliography at the botton with any model I used as inspiration.

## [Baseplate](./mec/baseplate.FCStd)

In addition to the classic baseplate there are custom vaiant baseplates. By default all baseplate do not have the corner filled.

All models are parametrizable through the `user_input` variable set. The grid size is controlled with the variables `grid_size.x_count` and `grid_size.y_count`.

The single chamfer profile is like the original one but the chamfer in the bottom is removed.
This simplifies the geometry, reduces printing time and is backwards compatible with the original design.

| 5x2 no filling corner | 4x3 filling corner |
| - | - |
| ![](./etc/baseplate/no_corner_5x2.png)| ![](./etc/baseplate/corner_4x3.png) |

* tiered
* slanted
* clipable

## [Container](./mec/container.FCStd)

| .... | .... |
| - | - |
| ![]( )| ![]( ) |

* hollow
* cutout
* slanted baseplate compatible
* clickable
* polyonimo


## [Miscellaneous](./mec/misc.FCStd)

This is a list of 3d models that are neither baseplater nor containers.

| spacer 5x2x3 | lid 3x4 | lid stackable 7x3 |
| - | - | - |
| ![](./etc/misc/spacer_5x2x3.png)| ![](./etc/misc/lid_3x4.png) | ![](./etc/misc/lid_stack_7x3.png) |

---

## Bibliography
* [Gridfiniry sepcs](https://gridfinity.xyz/)
* [Clip-on Gridfinity Baseplate and Bin](https://www.printables.com/model/368313-clip-on-gridfinity-baseplate-and-bin)
* [Gridfinity Angled baseplates](https://www.printables.com/model/656549-gridfinity-angled-baseplates)
* [Gridfinity | Tiered Baseplate | Parametric](https://www.printables.com/model/554733-gridfinity-tiered-baseplate-parametric)
* [Polyonimo](https://en.wikipedia.org/wiki/Polyomino)

---

Davang -