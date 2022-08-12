# Retired Reinforcement learning project of 2018/2019/2

## Description

Beloved project, we usually bring this project for expos

You can read more about gym-retro at this link: https://openai.com/blog/gym-retro/

## Installation

For the installation, conda is required!

To install the project, just clone the repository, and then run the following commands.

```sh
cd reinforcement_learning/
bash install.sh
```
The shellscript contains the following commands, you don't need to run them:

```sh
conda env create -f environment.yml #Creates a v. environment with the requered packages
conda activate mkombat              #Activates it
python -m retro.import Mortal\ Kombat\ II\ \(World\).md #Imports the game
```

And that is all! At an expo, we usually run the agent_vs_keyboard_example.py. You must run it in the examples folder!

```sh
cd examples/
python agent_vs_keyboard_example.py
```

## Getting Started

Read the [upstream wiki](https://github.com/legokor/reinforcement_learning/wiki) to get started with this project, or RL in general.
