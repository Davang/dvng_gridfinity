# dvng_gridfinity

Based on [Gridfinity | The modular, open-source grid storage system](https://www.youtube.com/watch?v=ra_9zU-mnl8), by [Zack Freedman's](https://www.youtube.com/@ZackFreedman).
As it is an open design I belive it shall be possible to use only open tools for its development.
Check [the gridfinity official especification](https://gridfinity.xyz/specification/) to know more about the design.
My implementation may not be strictly compliant with it, so be careful integrating it with your own or 3rd party designs, they may not work.

There is a bibliography at the botton with any model I used as inspiration.

All models are parametrizable through the `user_input` variable set.
Depending on the file there may be different parameters available.
In most of them there is one for managing the grid and height.

All model are within the [mec](./mec/) directory.
Baseplate and container each have a base file with the basic designs.
Each custom design is placed in a different file.
The miscellaneous directory has gridfinity compatible desgins that re neither baseplates or containers.

## [Baseplate](./mec/baseplate/)

| 5x2 no filling corner | 4x3 filling corner | 3x3 single chamfer |
| - | - | - |
| ![](./etc/baseplate/no_corner_5x2.png) | ![](./etc/baseplate/corner_4x3.png) | ![](./etc/baseplate/single_chamfer_3x3.png) |

| 7x4 tiered | 5x7 slanted | 5x7 clipable |
| - | - | - |
| ![]( ) | ![]( ) | ![]( ) |

## [Container](./mec/container/)

| 5x3x3 stackable | 2x2x10 non-stackable | 5x5x4 non-stackable |
| - | - | - |
| ![](./etc/container/basic_5x3x3.png) | ![](./etc/container/flat_2x2x10.png) | ![](./etc/container/flat_5x5x4.png) |

| 5x2 slanted base | 4x3 slanted lip | 5x7 clickable |
| - | - | - |
| ![]( ) | ![]( ) | ![]( ) |

| pencil holders | vernier calliper | SD cards |
| - | - | - |
| ![]( ) | ![]( ) | ![]( ) |


## [Miscellaneous](./mec/misc/)

| spacer 5x2x3 | lid 3x4 | lid stackable 7x3 | L cleat |
| - | - | - | - |
| ![](./etc/misc/spacer_5x2x3.png) | ![](./etc/misc/lid_3x4.png) | ![](./etc/misc/lid_stack_7x3.png) | ![]( ) |

---

## Bibliography
* [Gridfiniry sepcs](https://gridfinity.xyz/)
* [Clip-on Gridfinity Baseplate and Bin](https://www.printables.com/model/368313-clip-on-gridfinity-baseplate-and-bin)
* [Gridfinity Angled baseplates](https://www.printables.com/model/656549-gridfinity-angled-baseplates)
* [Gridfinity | Tiered Baseplate | Parametric](https://www.printables.com/model/554733-gridfinity-tiered-baseplate-parametric)
* [Polyonimo](https://en.wikipedia.org/wiki/Polyomino)

---

Davang -