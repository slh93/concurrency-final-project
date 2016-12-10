# Comp50: Concurrency 
## Final Project
#### Authors: Rachel Marison, Sam Heilbron

### Concept

This is a game of tag, very similar to [http://agar.io](agar.io). Basically, users join a game and they move around an enclosed space as a spehere trying to "eat" others. When they do, they become larger and as a result slower. If you are eaten, you are eliminated. To "eat" someone you must completely overlap their positition with yours. Just touching them doesn't result in anything. There are also small food items sitting around that don't move and allow players to get food easily. Players may also split themselves in half, and have 2 smaller spheres moving around together. This allows them to move faster, but makes it harder to eat others since they're smaller.


### Included Files

1. **main.py**: Prints out an opening message explaining the rules of the game to the user. It then prompts the user to select their preferred form of input (mouse or keyboard). A game is then started by creating and running an instance of the Game class

2. **games.py**:
	Contains all possible game classes. A Game is a wrapper for all components of a game. It keeps track of the users alive in the game (userList). It also keeps track of the gameboard, which is described more in boards.py below. It sets up all the users, draws and redraws them on the board, and kills users that have been eaten. It also listens for the game to finish by waiting on the gameOverFlag, which is signaled when the human is eaten, and the gameOverTimeout, which is signaled when the game clock has run out.

3. **boards.py**:
	Contains all possible board classes. The SyncGameBoard class represents a thread-safe gameboard for the game. It handles creating a pygame display, a board containing the center position of all users, and a board containing locks for each position of the gameboard, thus allowing for atomic access on the gameboard. The SyncGameBoard is in charge of moving users from one place to another on the board as well as removing them once they have been eaten.

4. **decisions.py**:
	Contains all possible decision classes. Decision classes represent the types of decisions that users make in order to move. All classes are built on top of the Basic class which connects the decision that is made to the movement class (see below).
		*	The **Stationary** class always decides to stay in place. 
    	*	The **KeyInput** class handles keyboard inputs to change the users direction.
    	*	The **MouseInput** class handles mouse movements to change the users direction.
    	*	The **AISmartInput** class decides to move towards where the human player is
    	*	The **AIRandomInput** class randomly chooses a direction to go in

5. **movements.py**:
	Contains all the possible movement classes. In this game, all user blobs are circles and the Circle_ class handles the actual movement of the users.
       	*	**Circle_** contains attributes related to its position (center, radius) and a semphare is required to get and set these values. It also contains a direction attribute which it shares with a decision class and thus another semaphore ensures atomic access to this value.
       	*	The Circle class tells the board to update with it's new position and then is responsible for handling collisions. The Circle looks for locked positions on the gameboard that are within the radius of the circle.

6. **users.py**:
    Contains all the possible user classes. All users are built off the base Blob class. The Blob class has decision and  movement classes (explained above), a color to display to the screen, and id to distinguish them from other blobs and a threading event isDead which is triggered when the user is eaten. This event kills the threads which are controlling the users decision and movement threads.
        *	The **Human** class represent the human user in the game. The movement class is handled in a separate thread but pygame requires that IO be handled in the main thread.
        *	The **AI** class is a base class for all non-human users. Both movement and decision instances are handled in separate threads.
        *	**Food**, **AISmart**, and **AIRandom** all inherit the AI class and just vary in their attributes.

7. **enums.py**:
	This file contains all enumerations used in the code. These include **Direction**, **Color**, **InitialUserRaidus**, and **Timeout**.


### Concurrency Challenges and Decisions
	* Users decisions and movements
		Since humans can make a decision to do something with their brain, while also doing something with their body, it makes sense for users of the game to have this capability. Therefore, the decision and movement classes are handled by 2 different threads. This successfully decouples 


Program Architecture:
	A game (games.py) consists of a board (boards.py) and a group of users (user.py)
	Users may be either a Human, Food or AI. All Users have a base class called blob.
	Users have a class for decisions and a class for movement. 
		Decisions (decisions.py) may be either Stationary, MouseInput, KeyInput or AiInput.
		Movement (movements.py) may be a Sphere (possible others to come soon)
	For all users, the decision and movement classes run in 2 separate threads.
	For the lone human, the decision (either key input or mouse input) class runs
		in the main thread since that is required. 

	The way the decisions and movement classes work together is that the decision class
		loops every few milliseconds and using the input (key or mouse) updates the intended direction of the user. In another thread, the movement class operates at a frequency based on its size. The larger it gets, the slower the interval. At every interval, the movement class updates the position of the user. These two classes share access to the direction variable so a mutex ensures atomic access to it.
