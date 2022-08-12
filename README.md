# Retired Reinforcement learning project of 2018/2019/2

## Description

One of our beloved old project, we usually bring this project for expos.

You can read more about gym-retro at this link: https://openai.com/blog/gym-retro/

## Installation

For the installation, conda is required!

To install the project, just clone the repository, and then run the following commands.

```sh
conda env create -f environment.yml #Creates a v. environment with the requered packages
conda activate mkombat              #Activates it
python -m retro.import Mortal\ Kombat\ II\ \(World\).md #Imports the game
```

And that is all! At an expo, we usually run the agent_vs_keyboard_example.py. You must run it in the examples folder!

```sh
cd example_codes/
python agent_vs_keyboard_example.py
```

## Remove

If you ever want to remove the project, just delete the folder, and remove the v environment.

```sh
rm -r reinforcement_learning/
conda deactivate
conda remove --name mkombat --all
```

## Getting Started

Read the [upstream wiki](https://github.com/legokor/reinforcement_learning/wiki) to get started with this project, or RL in general.
