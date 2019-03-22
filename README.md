# Reinforcement learning project 2018/2019/2

# Installation
```sh
$ apt update
$ apt install pip3
$ pip3 install --user gym-retro
$ python3 -m retro.import Mortal\ Kombat\ II\ \(World\).md
```

# Control

## Controller
The controller has 12 buttons.
![Controller](https://cdn11.bigcommerce.com/s-ymgqt/images/stencil/original/products/44395/38244/6-button-turbo__64130.1503433948.jpg?c=2&imbypass=on)

## env.step()

The `env.step()` function's input is a 12<sup>1</sup> digit binary number as a String.
Each bit represents a state of an action button. Mapped below:

| Button | Decimal | Action |
|---|---|---|
| MODE  | 512  | - |
| START | 256  | Block <sup>2</sup> |
| UP    | 128  |  Jump |
| DOWN  | 64   |  Squat |
| LEFT  | 32   | Move Left  |
| RIGHT | 16   | Move Right  |
| B     | 2048 | Low Kick  |
| A     | 1024 | Punch     |
| C     | 8    | High Kick |
| Y     | 4    | - |
| X     | 2    | - |
| Z     | 1    | - |

You can press and/or hold multiple buttons at once. 
For instance you could pass the env.step function this `f'{128|2048:012b}'` which would mean `'100010000000'`, causing kicking while jumping.  
1: Controlling both players at once requires a 12+12 digit binary number as a String, where the first 12 bit represents the first player's actions while the second 12 bit represents the second player's actions. For example `f'{128|2048:012b}'+f'{128|2048:012b}'`, which would mean `'100010000000100010000000'`, causing both players jumping.
2: The `START` button is filtered by the environment, to be able to use it, set the `env` variable's `use_restricted_actions` attribute's value to `retro.Actions.ALL`.

