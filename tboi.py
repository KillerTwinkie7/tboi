#This program is used to compute odds in The Binding of Isaac: Four Souls
import math
from tkinter import *

main_window = Tk()
main_window.title("The Binding of Isaac: Four Souls Combat Odds Calculator")

#Labels
Label(main_window, text="Character's Health?",fg="red",bg="black",width=60,height=1).grid(row= 0, column= 0)
Label(main_window, text="Character's Damage?",fg="red",bg="black",width=60,height=1).grid(row= 1, column= 0)
Label(main_window, text="Monster's Health?",fg="red",bg="black",width=60,height=1).grid(row= 2, column= 0)
Label(main_window, text="Monster's Damage?",fg="red",bg="black",width=60,height=1).grid(row= 3, column= 0)
Label(main_window, text="Dice Value?",fg="red",bg="black",width=60,height=1).grid(row= 4, column= 0)
Label(main_window, text="How many cards do you have that can prevent damage or reroll dice rolls?",fg="red",bg="black",width=60,height=1).grid(row= 5, column= 0)
Label(main_window, text="Curse of the Tower? (0 for no, 1 for yes)",fg="red",bg="black",width=60,height=1).grid(row= 6, column= 0)
Label(main_window, text="Guppy's Hairball? (0 for no, 1 for yes)",fg="red",bg="black",width=60,height=1).grid(row= 7, column= 0)
Label(main_window, text="",fg="red",bg="black",width=60,height=2).grid(row= 8, column= 0)

#Text Input
yH = Entry(main_window, width = 2, borderwidth = 2) #your health
yH.grid(row= 0, column= 1)

yD = Entry(main_window, width = 2, borderwidth = 2) #your damage
yD.grid(row= 1, column= 1)

mH = Entry(main_window, width = 2, borderwidth = 2) #monster health
mH.grid(row= 2, column= 1)

mD = Entry(main_window, width = 2, borderwidth = 2) #monster damage
mD.grid(row= 3, column= 1)

d = Entry(main_window, width = 2, borderwidth = 2) #dice values
d.grid(row= 4, column= 1)

h = Entry(main_window, width = 2, borderwidth = 2) #help cards
h.grid(row= 5, column= 1)

coft = Entry(main_window, width = 2, borderwidth = 2) #Curse of the Tower
coft.grid(row= 6, column= 1)

g = Entry(main_window, width = 2, borderwidth = 2) #Guppy's hairball
g.grid(row= 7, column= 1)

#Function for N choose R
def nCr(n,r):
    if n-r < 0:     #|I know this is heresy, but it's required for the model to work correctly.
        return 0    #|Negative factorials are undefined under basically every other circumstance.
    numer = math.factorial(n)
    denom = math.factorial(r)*math.factorial(n-r)
    return numer/denom;

#Function to calculate the odds of a successful fight
def odds(yourHealth, yourDamage, monsterHealth, monsterDamage, dice, help_cards, coft, guppy): #where yH is your health, yD is your damage, mH is monster health, mD is monster damage, d is what dice roll is required to deal damage, and h is how much total damage you can prevent with cards in play.
    die = [0, 1, 5/6, 2/3, 1/2, 1/3, 1/6]   #| Assigns probabilities based on what's labelled on the card.

    yourHealth = int(yourHealth)        #|
    yourDamage = int(yourDamage)        #|
    monsterHealth = int(monsterHealth)  #|  This is all importing data from the GUI.
    monsterDamage = int(monsterDamage)  #|
    dice = int(dice)                    #|
    help_cards = int(help_cards)        #|
    coft = int(coft)                    #|
    guppy = int(guppy)                  #|

    if yourHealth == 0:                 #|
        print("You're dead numbnuts.")  #|  Data validation
        return                          #|

    dice_roll = die[dice]                                           #| Stores the value of the dice roll in integer form instead of in a list.
    chances = math.ceil((yourHealth) / (monsterDamage) - 1)         #| The amount of chances you have to defeat the monster until your health runs out.
    req_success = math.ceil((monsterHealth) / (yourDamage))         #| The amount of times you have to deal a successful attack to kill the monster.

    #| Ended up using this function a lot, so I, well, made it a function.
    def std_prob(req_success, dice_roll, chances):
        prob = [] #| List of probability values to be added to get the final probability value.
        x = 0
        while x <= chances:
            odds = (nCr(req_success+x,x) - nCr((req_success+x)-1,req_success))*((dice_roll)**req_success)*(1-dice_roll)**x #See Note 1 at bottom
            prob.append(odds)
            x += 1
        actual_odds = sum(prob)*100
        return actual_odds
    #| See Note 1 |#

    if coft != 1 and guppy != 1: #| Calculates odds of winning without Curse of the Tower in play.
        if help_cards == 0: #| If you have no cards to help you in combat.
            actual_odds = std_prob(req_success,dice_roll,chances)
            final_probability = "You have a {}% chance of winning this fight.".format(round(actual_odds,3))
            print(final_probability)
            print("_______________________________________________________________________________________________________________________")
        elif help_cards >= 1: #| If you do have cards to help you.
            y = 0
            for y in range(help_cards):
                chances += help_cards
                actual_odds = std_prob(req_success,dice_roll,chances)
                y += 1
            final_probability = "You have a {}% chance of winning this fight with {} helpful cards.".format(round(actual_odds,3),y)
            print(final_probability)
            print("_______________________________________________________________________________________________________________________")

#| This block below can likely be condensed, but it works and I don't really want to touch it right now. |#

    elif coft == 1 and guppy != 1: #| Calculates odds without help cards other than Curse of the Tower.
        #| See Note 2. |#
        prob = []
        chances += 1 + help_cards #You're given an extra chance because it is now possible to die and kill the monster at the same time with CofT active, and we want to account for the amount of damage prevention you have.
        #| Adding the amount of help cards to the chances may not be correct, as help cards prevent damage and CofT only triggers when you take damage. |#
        m = 0
        while m <= chances:
            c = 0
            while c <= chances:
                if m+c > chances: #Breaks out of the loop if your missed CofT attempts and successful CofT attempts surpass your total number of chances.
                    break
                if c == 0: #if you're only considering missed CofT attempts, the model is identical to the one above, barring multiplying (.5) from everything else
                    if m == chances: #if you miss the total amount of chances you have and none of them are successful, you're dead.
                        break
                    if m != 0 or c != 0: #if both m and c are 0, then you're merely accounting for the probability of success with each CofT attempt failed.
                        coft_odds = (.5)*(nCr(req_success+m,m) - nCr((req_success+m)-1,req_success))*((die[dice])**req_success)*(1-die[dice])**m
                        prob.append(coft_odds)
                    else:
                        coft_odds = (nCr(req_success+m,m) - nCr((req_success+m)-1,req_success))*((die[dice])**req_success)*(1-die[dice])**m
                        prob.append(coft_odds)
                if m+c == chances: #if the total amount of missed and successful CofT attempts equals your total chances, there's only one way you can succeed.
                    coft_odds = (nCr(req_success-c,m))*((die[dice])**(req_success-c))*((1-die[dice])**(m+c))*((.5)**(m+c))
                    prob.append(coft_odds)
                    c+=1
                    break
                if c != 0: #Program wasn't doing anything when c != 0, so here it is.
                    coft_odds = (nCr(req_success+m,c))*((die[dice])**(req_success-c))*((1-die[dice])**(m+c))*((.5)**(m+c))
                    prob.append(coft_odds)
                c+=1
            m+=1
        actual_odds = (sum(prob))*100
        final_coft_probability = "You have (approximately) a {}% chance of winning this fight with Curse of the Tower and without the use of any other cards to help you.".format(round(actual_odds,3))
        print(final_coft_probability)
        print("_______________________________________________________________________________________________________________________")

    elif guppy == 1: #| Odds of winning a fight if you have Guppy's Hairball.
    #| See Note 3 |#
        prob = []
        m = 0 #| Number of missed rolls
        while m <= chances:
            g = 0 #| Number of successful guppy rolls
            while g <= chances+3: #| This is for considering 3 extra rolls past your maximum health, as it's possible to prevent damage infinitely, but is very unlikely to happen more than 3 times.
                guppy_odds = ((nCr(m+g,g))*(nCr(req_success+(m+g),(m+g)) - nCr((req_success+(m+g))-1,req_success))*((dice_roll)**req_success)*(1-dice_roll)**(m+g))*((5/6)**m)*((1/6)**g) #| Note that the only real difference betweeen this and the original equation is that x has been replaced with m+g
                prob.append(guppy_odds)
                g += 1
            m += 1
        final_probability = sum(prob)*100
        final_guppy_probability = "You have (approximately) a {}% chance of winning this fight with Guppy's Hairball, and without any other cards to help you.".format(round(final_probability,3))
        print(final_guppy_probability)
        print("_______________________________________________________________________________________________________________________")

    else:
        print("This is a fail-safe.")

#Function for button presses.
def on_enter():
    yourHealth = yH.get()
    yourDamage = yD.get()
    monsterHealth = mH.get()
    monsterDamage = mD.get()
    dice = d.get()
    help_cards = h.get()
    tower_curse = coft.get()
    guppy = g.get()


    odds(yourHealth, yourDamage, monsterHealth, monsterDamage, dice, help_cards, tower_curse, guppy)

#Buttons
Button(main_window, text="Enter", bg="red", fg="black", command= on_enter).grid(row=8, column = 1)

main_window.mainloop()

#where yH is your health, yD is your damage, mH is monster health, mD is monster damage,
#and d is what dice roll is required to deal damage.

#***NOTE 1*** This is the hardest part of the program. What's happening here is we have to compute all of the possible ways you can succeed
#in a fight. However, this isn't as easy as using factorials and combinatorics, as you will double count a lot of already considered
#possibilities, which skews the probability. To see how this line works, consider:
#
#You: 4 Health, 1 damage
#Monster: 7 Health, 1 damage, 5+ on dice roll.
#
#To calculate these odds, we need to add the probabilities of not failing a single dice roll, failing once, failing twice, and failing
#3 times. Notice that if we fail 4 times, the combat is over, and we want to compute the odds of a *successful* attack. So, to begin,
#we compute the odds of not missing a single attack, which in this case would be (1/3)^7. Now, we need to compute the odds of winning,
#assuming you failed once. To do this, we can look at all of the possibilitiesof 8c1 (8 choose 1), which are as follows:
# FSSSSSSS
# SFSSSSSS
# SSFSSSSS
# SSSFSSSS
# SSSSFSSS
# SSSSSFSS
# SSSSSSFS
# SSSSSSSF
#But, notice that last entry has a failed dice roll at the end. We need to throw this value out as we have already rolled 7 successful
#dice rolls, and thus do not need to roll an 8th time. So, the probability of rolling 7 successful rolls with 1 failed roll is:
#7*(1/3^7)*(2/3)
#Continuing on with the pattern, let us consider the possibility of rolling 7 successful rolls with 2 failed rolls. To do this, we need to
#consider 9c2. For demonstrative purposes, 6c2 is listed below.
#FFSSSS
#FSFSSS
#FSSFSS
#FSSSFS
#FSSSSF *
#SFFSSS
#SFSFSS
#SFSSFS
#SFSSSF *
#SSFFSS
#SSFSFS
#SSFSSF *
#SSSFFS
#SSSFSF *
#SSSSFF *
#If you were to count 9c2, you'd see that there are 36 outcomes. However, notice in the example above each entry marked with an *. These are all of the entries
#that ended with a failed dice roll, and thus would not occur, as they have already been accounted for in previous cases (those being successful
#attacks with no failures, and successful attacks with 1 failure.). So, we throw them out. This trend continues as you increase the amount
#of chances you have to take damage and not die. Now the question becomes, "how do we know how many entries to throw out in each iteration?"
#After looking at different cases and seeking counsel, I had come up with the original equation used in the code. If we take the example we used
#above (that being, your character has 4 health, 1 damage, and the monster having 7 health with 1 damage and a 5+ dice roll), and expand each iteration out to match forms, we have:
#
#0 fail(s): (7c0)*(1/3^7)*(2/3)^0
#1 fail(s): (8c1 - 7c7)*(1/3^7)*(2/3)^1
#2 fail(s): (9c2 - 8c7)*(1/3^7)*(2/3)^2
#3 fail(s): (10c3 - 9c7)*(1/3^7)*(2/3)^3
#
#From this example, it is easier to see how the equation used in the code is implemented. Note that we do not consider 4 failures as that would
#result in the death of our charatcer.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#***NOTE 2***
#In this block, we're considering the probability of success when Curse of the Tower is in play, which reads "each time you take damage, roll: 1-3, deal damage to all other players. 4-6: deal 1 damage to any monster".
#Essentially, this means that each time a player takes damage, they have a 50% chance to deal damage back, which requires a new model.
#Firstly, I used 2 loops, one nested within each other. I needed to find out the probability of each case, so the loops allowed me to go through each individual case. The cases I used are as follows:
#P(0 missed curse of the tower attempts (M), 0 successful CofT attempts)
#P(0M,1C)
#P(0M,2C)
#...
#P(0M,bC)
#P(1M,0C)
#P(1M,1C)
#...
#P(1M,bC)
#P(2M,0C)
#...
#P(aM,bC), where a+m <= the total amount of chances the attacking player has.
#Among these cases are a few special cases. Firstly, if both M and C are 0, that's equivalent to rolling all successful attacks without dropping one. In this case, it does not matter if Curse of the Tower is active or not,
#your odds are the same. Next, we need to be careful about the total amount of misses and successes we have. If M == chances, that means we have missed CofT rolls equal to our total health, in which case, we're dead. We throw
#these combinations out. Then, if M + C = chances, this means that you've taken damage equal to your total health, in which case your last attack roll *must* be successful. Because of this, we have to count all the ways we can
#succeed by "fixing" a successful attack roll at the end of the permutations. For example, if we must be successful 4 times, and have 2 health, then the ways we can do that are:
#F_m S S F_h
#S F_m S F_h
#S S F_m F_h
#where F_m is for failed CofT attempts (read "fail miss") and F_h is for successful CofT attempts (read "fail hit"). In general, there are (req_success-c C m) ways of organizing these combinations.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#
#***NOTE 3***
#This model I used for Guppy's hairball has a small amount of inaccuracy. Theoretically, it's possible to roll an infinite amount of 6's every time you take damage while you have Guppy's Hairball, I can't account for
#all of these possibilities however, so I estimate. The error occurs when I take the probability of success assuming I've activated Guppy's Hairball at least once. For the sake of example, let's work with the assumption that
#I will successfully block 1 damage with Guppy's collar. Essentially, this means that my failed attack roll never happened, and I reroll. The problem with coming up with a model that takes this into account is just the same
#as before- this can happen infinitely many times. However, the odds of this happening are infinitesimally small, and can be ignored. However, there are some more likely ways this can happen. Consider the case where your character
#has 2 health. It's possible to activate guppy's hairball 3 times, or 4 times, or 5 times, and so on. I only consider the possibility of activating guppy's hairball equal to or less than the total amount of health the player has plus 3,
#as successfully blocking damage greater than that is increasingly unlikely the higher your health becomes.  As for explanation of the model, one immediately notices a similarity to the standard model, albeit with some minor addicitons.
#Firstly, we have the term nCr((m+g),g). Essentially, this accounts for all the ways that you can successfully block damage when you have more than 1 health. For example, If I have 2 health, and I'm considering the case where I successfully
#block 3 damage on a monster with 2 health, I need to consider the following:
#F_m F_s F_s F_s S S
#F_s F_m F_s F_s S S
#F_s F_s F_m F_s S S
#F_s F_s F_s F_m S S
#S F_m F_s F_s F_s S
#...
#Thus, there are 4C3 ways to arrange 3 successful blocks and 1 unsuccessful block, multiplied by all the ways we can succeed the overall attack with this in mind.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
