Game of Life- Keir Parker

GOL_Class.py is a class containing the methods to simulate the Game of Life by John Horton Conway. GOL_Script.py is the script to run the simulation.

Rules for the Game of Life are included in comments but for more information see the following link "https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life"

At present, methods for the following structures exist: absorbing state, blinker, glider and a completely random lattice.

To run, User should enter: GOL.py <dimension of lattice> <structure> <task>
EXAMPLES: 50 random viz, 50 glider viz, 50 blinker viz, 50 glider data


The following tasks are defined in the script:(1) <task> = "viz". Simple animation of GOL with user defined initial structure, (2) <task> = "data". If user selects a Glider, tracks the position of the centre of mass of glider and displays in a graph. Also calculates the constant velocity of the glider.


SIRS Model - Keir Parker

The SIRs model (susceptible, infected, recovered) model is a mathematical model to simulate the spread of infectious disease. See https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model for more details

SIRS_Class.py contains all methods to simulate and sample such a system as a 2D lattice. SIRS_Script.py contains the instructions for different tasks. 

To Run: python3 SIRS_Script.py <dimension> <p1> <p2> <p3> <task>

p1,p2,p3 are probabilities of a cell switching from S->I, I->R, R->S. Where the following numbers represent each state: -1=S, 0=I, 1=R.

Available 'tasks' in the script are:
- <task> = "viz" creates an animation of the system with the user defined probabilities.
(0.9,0.08,0.01 creates recurring waves of infection)
(0.98,0.5,0.98 creates a dynamical state)
(0.9,0.08,0 creates an absorbing state)

- <task> = "phase" simulates the SIRs model for a range of probs of S->I & I->R. p2 should be set to 0.5. In this task the lattice is sampled routinely and the average infected fraction density and variance in the infected fraction desnity are presented as contour plots. 

- <task> = "immune" simulates the SIRs model with an increasing fraction of fixed immune cells. A graph is produced which indicates the minimum immune fraction to reduce the average infected fraction to 0. p1=p2=p3=0.5.
