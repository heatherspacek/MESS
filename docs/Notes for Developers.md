Here's some definitions for terms or abstractions that can be found in this project. 
There is a loose hierarchy between them that this document can hopefully clarify.

| Term | Definition |
| ---- | ---------- |
| Action | A sequence of in-game inputs corresponding to a game action. They can be defined with statistical "spacers" to reflect that human execution will generally have a certain consistency distribution. **Examples:** Shallow wavedash; fox early nair |
| Trigger | A game-state that causes a StrategyPlayer to do some reaction. **Examples:** Opponent jumps at a certain distance; opponent enters a certain distance from the player; opponent has not done anything else for 1 second |
| Reaction | One or more actions triggered by a Trigger. **Examples:** shine out-of-shield; aimed overshoot nair |
| Strategy | A data structure containing some number of triggers (associated to reactions). This is intended to be  |
| StrategyPlayer | Program entity that holds a controller and follows a Strategy. |