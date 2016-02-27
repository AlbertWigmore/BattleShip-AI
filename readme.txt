# Purdue Hackers Battleship Competition
:anchor: :computer: :boat: :boom:
## Team ARGO

The AI code uses a probability density function to work out the most likely place for a ship.
It finds every valid placement for a ship and adds 1 to the probability density grid. 
More probability is then added if there is currently a hit with an adjecent no try square.
Then choose most probable point and fire at will! :boom:

Note: We did write a function to place the ships but it was bad... very bad, it was a no go!
Therefore we just had a fixed placement :+1:.