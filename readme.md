# Minesweeper Solver

## Game features

Game parameters are set in the constructor of the `Game` class:
- `height` - the height of the field in pixels;
- `width` - width of the field in pixels;
- `cell_size` - size of the cell in pixels
- `bomb_number` - number of bombs;
- `fps` - number of frames per second;
- `saved_field` - saved field, by default None.

**Commands:**
- To open a cell - `LMB`;
- To mark a cell - `RMB`.

To start the game you need to run the script `main.py`. Two game formats are offered:

- **Regular** is a regular game;

<img src="/regular.gif"/>

- **Solver** - launches the solver. The `Solver` class takes a visible field as input.

<img src="/solver.gif" title="Solver"/>

The game is automatically saved after closing the interface in the `data.pickle` file.

## Solver logic

The main idea is to calculate the probability of finding a bomb in each cell of the field, 
based on the already open cells. To start with, we calculate the probabilities for
individual cells, which may result in several probabilities in the same cell as a 
consequence of the influence of several cells adjacent to each other. To calculate the 
probability of finding a mine in a cell adjacent to several open cells, we use the formula
for calculating the probability of at least one event: the probability of the 
occurrence of the event `A`, consisting in the occurrence of at least one of the 
events `A1, A2,..., An`, independent  in together, is equal to the difference between 
one and the product of the probabilities of the opposite events:

`A = 1 - (1 - A1) * (1 - A2) * ... * (1 - An)`. 

However, it should be remembered that the sum of probabilities in each group of cells
must be equal to the number of mines in the group. Therefore, all values in each group 
must be multiplied so that their sum is finally is equal to the number of mines. This
number is equal to the number of mines in the group divided by the current sum of
cells in the group. A similar calculation for the second group is performed already 
taking  into account corrections from the previous one. After that the probability in 
common cells will change again, so similar equalization for each group should be 
repeated several times, until system arrives at some stable values, which will be true 
probabilities of finding mines in cells. It remains only to choose one of the cells 
with minimum probability and make a move.