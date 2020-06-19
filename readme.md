# Amstelhaege

This is the project Amstelhaege for the subject "Heuristieken / Programmeertheorie 2017".


###### Assignment
The assignment is to deliver a map (2D or 3D) for each of the three house variants for the new district Amstelhaege. The scores for a map is the sum of all houses in the neighbourhood.


###### Description
A new residential area will be built in the Duivendrechtse polder. The houses are intended for the middle and upper segment of the market, in particular expats and highly educated employees active on the Amsterdam Zuidas.

The municipality is considering three variants for the houses: the 20-house variant, the 40-house variant and the 60-house variant. It is assumed that a house becomes more valuable as the free-standing / space increases.


###### Requirements
- The residential area will be placed on a piece of land of 160x180 meters.
- The number of homes in the neighbourhood consists of 60% single-family homes, 25% of bungalows and 15% of maisons.
- A single-family house is 8x8 meters (wide x deep) and has a value of €285.000, - The house needs around two meters of free space; every meter extra provides a price improvement of 3%.
- A bungalow is 10x7.5 meters (wide x deep) and has a value of €399.000, -. The home needs around three meters of free space, every meter extra provides a price improvement of 4%.
- A maison is 11x10.5 meters (wide x deep) and has a value of €610.000, - The house needs around six meters of free space, every meter extra provides a price improvement of 6%.
- The free space of a house is the smallest distance to the nearest other house in the neighbourhood. In other words, for a 6 meter free space, all other houses in the neighbourhood must be at least 6 meters away. This distance is defined as the shortest distance between two walls, not from the center of the house.
- The compulsory free space for every house must fall within the residential area.
- In case of percent value increase per meter, the increase is not cumulative. A maison with two meters extra clearance is therefore worth 12.0% more, not 12.36%.
- The district must consist of 20% of surface water, divided into no more than four parts that are rectangular or oval in shape. In order to keep the neighbourhood attractive, the bodies must have a height-width ratio between 1 and 4\. No long thin parts!



## Getting Started

- code - main code for the project
- docs - documentations about the project
- results - results of each algorithm-variant combination

### Prerequisites

- Python 3.6.x

The following packages are libraries:
  - Copy
  - Math
  - Matplotlib
  - Numpy
  - Random

You can easy-install them using the following line of code:
```
pip install -r requirements.txt
```

Navigate to code/amstelhaege.py. In this file  a variant can be chosen and initialised with AmstelhaegeSetup(). Objects can be placed with randomPlacements() and algorithms can be run with e.g. hillclimber().

```
python amstelhaege.py
```


## Built With

- [Atom](https://atom.io/) - IDE
- [Python 3.6](https://docs.python.org/3/) - Python3


## Versioning

- v1.0 (18-12-2017)


## Acknowledgements

- Maarten van der Sande
- Bas Terwijn
- Daan van den Berg


## Authors

**Name:** Khalid El Khuri
**Student number:** 11927739

**Name:** Orin Habich
**Student number:** 10689508

**Name:** Xander Locsin
**Student number:** 10722432
