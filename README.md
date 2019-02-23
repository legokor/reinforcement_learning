# Reinforcement learning project 2018/2019/2

# Installation
```sh
$ apt install pip3
$ pip3 install --user gym-retro
$ python3 -m retro.import Mortal\ Kombat\ II\ \(World\).md
```

# Iranyitas
A jatekban 12 gomb van. Az `env.step()` fuggveny egy 12 jegyu binaris szamot (stringkent) var parameterul. Mindegyik bit egy-egy gomb allapotat kodolja.

| Gomb | decimalis | mit csinal |
|---|---|---|
| MODE  | 512  |   |
| START | 256  |   |
| UP    | 128  |   |
| DOWN  | 64   |   |
| LEFT  | 32   |   |
| RIGHT | 16   |   |
| B     | 2048 | Low Kick  |
| A     | 1024 | Punch     |
| C     | 8    | High Kick |
| Y     | 4    | ?? |
| X     | 2    | ?? |
| Z     | 1    | ?? |

Egyszerre persze tobb gombot is lenyomva tarthatsz. Pl. a `f"{128|2048:012b}"` vagyis `"100010000000"` string ugralas kozben fog rugdosni.
