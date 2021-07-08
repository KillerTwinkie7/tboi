# tboi
A program to spit out probabilities of successful attacks in the card game The Binding of Isaac: Four Souls. Likely has applications in other board/card games with heavy empahsis on dice rolls.

Since I'm an amateur programmer, I did not implement GUI. For the program to calculate different values, go into the code and change the values in the 'odds' function.
The variables listed are yH, yD, mH, mD, d, and h, which are your health, your damage, monster health, monster damage, the dice value required to deal damage, and how
many cards you have that can assist you in defeating the monster (usually cards like soul hearts, etc).

So for example, the line 'odds(2,1,4,1,4,0)' would spit out the probability of winning a fight against a monster when you have 2 health and deal 1 damage, the monster
has 4 health, deals 1 damage, and takes damage on a roll of 4 or higher, and you have no cards that can assist you in defeating the monster.
