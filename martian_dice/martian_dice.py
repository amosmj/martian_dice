#!/usr/bin/env python

"""
The game martian dice is a favorite of mine
The rules are relatively easy to teach and get
people playing in minute

Rules
===============
Roll 13 identicaly dice
1 Army
2 Space ship
1 human
1 cow
1 chicken

Each roll keep all armies
Then select one face that you will keep all of
Per turn you can only select a given face once
except space ships, which you may select as many
times as you want

Your turn ends when you choose or when you cannot
keep anymore dice (nothing left that you haven't
taken or no dice left)

At the end of the turn if you have the same number or
more space ships than armies, you will score points:
1 point per "Eathling face" (humnan, cow, chicken)
3 bonus points if you got one or more of each of
the Earthlings

Gameplay goes to the first person to reach 25

Based on these rules there is a lot of luck in
this game and really two decisions each roll
1. What face do I keep
2. Do I go again
"""
import random
import itertools

""" Not working and I don't know why. Specifically, not calling __init__"""


class Player:
    def __init__(self):
        possible_player_names = ["Alice", "Bob", "Charle", "Donna", "Eduadro", "Faust", "Glenda", "Hiro", "Justine",
                                 "Ingrid", "Kyle", "Lamar", "Mike", "Nancy", "Olga", "Quentin", "Patsy", "Roberta",
                                 "Susan", "Theo", "Eunice", "Wayne"]
        self.name = random.choice(possible_player_names)
        self.score = 0

    def modify_name(self):
        self.name += " mundane"

    def think_about_what_to_keep(self, roll, score):
        options = ["Space Ship", "Human", "Cow", "Chicken"]
        if score["Human"] is not 0:
            options.remove("Human")
        if score["Cow"] is not 0:
            options.remove("Cow")
        if score["Chicken"] is not 0:
            options.remove("Chicken")
        if roll["Space Ship"] is 0:
            options.remove("Space Ship")
        if score["Army"] >= score["Space Ship"] and roll["Space Ship"] > 0:
            choice = "Space Ship"
        else:
            choice = random.choice(options)
        return choice

    def think_about_whether_to_quit(self, score):
        return random.choice([True, False, False, False])

    def __str__(self):
        return "{} has {} point(s)".format(self.name, self.score)

    def __repr__(self):
        return "{}".format(self.name)


class Risky_Player(Player):

    def modify_name(self):
        self.name += " risky"

    def think_about_what_to_keep(self, roll, score):
        options = ["Space Ship", "Human", "Cow", "Chicken"]
        if score["Human"] is not 0:
            options.remove("Human")
        if score["Cow"] is not 0:
            options.remove("Cow")
        if score["Chicken"] is not 0:
            options.remove("Chicken")
        if roll["Space Ship"] is 0:
            options.remove("Space Ship")
        # This player is never forced to take Space Ships
        # because she isn't risk adverse
        choice = random.choice(options)
        return choice

    def think_about_whether_to_quit(self, score):
        # see how this player never passes play
        return random.choice([False, False, False])


class Thoughtful_Player(Player):

    def modify_name(self):
        self.name += " thoughtful"

    def think_about_what_to_keep(self, roll, score):
        options = ["Space Ship", "Human", "Cow", "Chicken"]
        if score["Human"] is not 0:
            options.remove("Human")
        if score["Cow"] is not 0:
            options.remove("Cow")
        if score["Chicken"] is not 0:
            options.remove("Chicken")
        if roll["Space Ship"] is 0:
            options.remove("Space Ship")
        # This player is never forced to take Space Ships
        # because she isn't risk adverse
        #
        # Left the options list in place because it's a good place to start
        # dice_left = roll["Army"] + roll["Space Ship"] + roll["Human"] + roll["Cow"] + roll["Chicken"]
        imbalance = score["Space Ship"] - score["Army"]
        if imbalance > -1 and roll["Space Ship"] > 0:
            # I'm in catch up mode on armies
            print("Thoughtful went straight to space ship")
            return "Space Ship"
        else:
            if len(options) <= 1:
                # I only have space ships and one option left
                # I want to return that option
                # NOTE: I'm kind of rushing this but it is very
                # possible to put myself in an unwinnable situation
                # with this
                for i in options:
                    print("i == {}".format(i))
                    if i != "Space Ship":
                        print("looking for the thing that isn't a spaceship")
                        return i
            else:
                # lots of choices left
                # going to take a tactic and try and return the biggest one
                # not sure how to do this right now and don't have internet
                # access to just kluging this together
                if imbalance > 2 or roll["Space Ship"] == 0:
                    # already lots of ships, ignore those
                    # note, that which Earthling I get doesn't really
                    # matter so I just arbitrarily look at them in the
                    # order of Human, Chicken, Cow
                    if roll["Human"] > roll["Chicken"]:
                        if roll["Human"] > roll["Cow"]:
                            print("think humans have the most")
                            return "Human"
                        else:
                            print("think cows have the most (1)")
                            return "Cow"
                    else:
                        if roll["Chicken"] > roll["Cow"]:
                            print("think that chickens have the most")
                            return "Chicken"
                        else:
                            print("think that the cows have the most(2)")
                            return "Cow"
                else:
                    # get some ships
                    print("probably need to rethink this spaceship call")
                    return "Space Ship"

    def think_about_whether_to_quit(self, score):
        # see how this player never passes play
        if score["Space Ship"] >= score["Army"]:
            dice_left = 13 - (score["Army"] + score["Space Ship"] + score["Human"] + score["Cow"] + score["Chicken"])
            if dice_left < (score["Space Ship"] - score["Army"]):
                return False
            else:
                # I have enouch defenders but not by a lot
                if dice_left < 4:
                    # for the purpose of this demo
                    # I've decided that this is a narrow
                    # enough margin to call it
                    # with more dice I might push on
                    return True

        else:
            # can't win in this scenario
            # press on until the game forces me to stop
            return False


class Die:
    def __init__(self):
        self.faces = ["Army", "Space Ship", "Space Ship", "Human", "Cow", "Chicken"]
        self.active_face = random.choice(self.faces)

    def roll(self):
        self.active_face = random.choice(self.faces)

    def __str__(self):
        return str(self.active_face)

    __repr__ = __str__


class Dice_Cup:
    def __init__(self, num_of_dice):
        self.cup = []
        for i in range(num_of_dice):
            self.cup.append(Die())

    def roll(self):
        for die in self.cup:
            die.roll()
        # print(self.cup)

    def remove_dice(self, count_to_remove):
        for die in self.cup:
            if count_to_remove > 0:
                self.cup.pop()
                count_to_remove -= 1


class Game:
    def __init__(self):
        self.game_over = False
        player_count = random.randint(2, 10)
        self.players = list()
        for player in range(player_count):
            new_player = random.choice([Player(), Risky_Player(), Thoughtful_Player()])
            new_player.modify_name()
            self.players.append(new_player)
        random.shuffle(self.players)
        self.start_player = self.players[0]
        print(self.players)

        self.player_scores = {}
        for player in self.players:
            self.player_scores[player] = 0
        self.turn_order = itertools.cycle(self.players)

    def turn(self):
        current_player = next(self.turn_order)
        dice_cup = Dice_Cup(13)
        score = {"Army": 0, "Space Ship": 0, "Human": 0, "Cow": 0, "Chicken": 0}
        turn_over = False

        while turn_over is False:
            roll = {"Army": 0, "Space Ship": 0, "Human": 0, "Cow": 0, "Chicken": 0}
            dice_cup.roll()
            for die in dice_cup.cup:
                roll[die.active_face] += 1
            print("{} rolled {}".format(current_player.name, roll))
            # you are forced to keep Army every time
            score["Army"] += roll["Army"]
            dice_cup.remove_dice(roll["Army"])

            # if there are no faces you can keep, your turn is over
            valid = ["Space Ship", "Human", "Chicken", "Cow"]
            if roll["Space Ship"] == 0:
                valid.remove("Space Ship")
            if roll["Human"] == 0 or score["Human"] > 0:
                valid.remove("Human")
            if roll["Chicken"] == 0 or score["Chicken"] > 0:
                valid.remove("Chicken")
            if roll["Cow"] == 0 or score["Cow"] > 0:
                valid.remove("Cow")
            if len(valid) > 0:
                # if there are valid faces, player logic needs to decide what to keep
                valid_choice = False
                break_counter = 0
                while valid_choice is False:
                    if break_counter > 25:
                        input("It looks like you probably have a logic error. Check your code and try again")
                        valid_choice = True
                    else:
                        break_counter += 1
                    choice = current_player.think_about_what_to_keep(roll, score)
                    if choice in ["Space Ship", "Human", "Chicken", "Cow"]:
                        if roll[choice] > 0:  # this is where the error appears to be
                            if score[choice] == 0 or choice == "Space Ship":
                                valid_choice = True
                                score[choice] += roll[choice]
                                dice_cup.remove_dice(roll[choice])
                            else:
                                print("Invalid Choice {}: You already kept that {}".format(choice, score))
                        else:
                            print("Invalid Choice {}: You didn't roll that {}".format(choice, roll))
                    else:
                        print("Very funny, do it again. do it right this time")
                        print(["Space Ship", "Human", "Chicken", "Cow"], choice)
                        input("Press any key")
                print("You chose", choice)
                if len(dice_cup.cup) == 0:
                    print("No dice left, end turn automatically")
                    turn_over = True

                # after making a choice the player may choose to resign
                turn_over = current_player.think_about_whether_to_quit(score)
            else:
                print("Turn over forced. No valid play")
                turn_over = True
        if score["Army"] <= score["Space Ship"]:
            # adding points gain
            results = score["Human"] + score["Cow"] + score["Chicken"]
            # if you get some of each, you get a 3 point bonus
            if score["Human"] and score["Cow"] and score["Chicken"] > 0:
                results += 3
            current_player.score += results
            print("{} score {} points this round".format(current_player.name, results))
        else:
            print("{} got driven back by the Army. No Points. Army: {}, Defenders: {}".format(current_player.name, score["Army"], score["Space Ship"]))
        # Evaluate if game is over, game ends at 25
        if current_player.score >= 25:
            self.game_over = True
        """
        Minor deviation from the rules here:
        technically I need to "go around the table"
        This was meant as a practice and demo of just
        how I iagine a different program working so
        I'm parking this
        """
        for player in self.players:
            print("{} scored {} points".format(player.name, player.score))


game = Game()
while game.game_over is False:
    game.turn()

"""
new_die = Die()
for i in range(12):
    new_die.roll()
    print("roll {} of {}".format(i, new_die.active_face))
"""
