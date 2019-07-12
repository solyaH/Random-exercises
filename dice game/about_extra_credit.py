import random


def non_scored(dice):
    num_of_non_scored = 0
    dictionary = {x: dice.count(x) for x in set(dice)}
    for key, value in dictionary.items():
        if key in [2, 3, 4, 6]:
            if (value % 3) != 0:
                num_of_non_scored += value
    return num_of_non_scored


def score(dice):
    total = 0
    dictionary = {x: dice.count(x) for x in set(dice)}
    for key, value in dictionary.items():
        remainder = value % 3
        quotient = value // 3
        if key == 1:
            total += quotient*1000
            total += remainder * 100
        else:
            if key == 5:
                total += remainder * 50
            total += quotient * key * 100
    return total


class DiceSet:
    def __init__(self):
        self._values = None

    @property
    def values(self):
        return self._values

    def roll(self, n):
        self._values = [random.randint(1, 6) for _ in range(n)]


class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.dice = DiceSet()
        self.turn_score = 0
        self.num_of_dice = 0

    def take_turn(self):
        self.total_score += 300
        self.num_of_dice = 5

    def next_step(self):
        self.dice.roll(self.num_of_dice)
        rolled = self.dice.values
        new_score = score(rolled)
        self.num_of_dice = non_scored(rolled) if non_scored(rolled) != 0 else 5
        self.turn_score += new_score
        return new_score, rolled

    def end_turn(self):
        if self.turn_score != 0:
            self.total_score += self.turn_score
            self.turn_score = 0


class Game:
    def __init__(self, num_of_players, my_file):
        self.my_file = my_file
        self.players = [Player(str(x + 1)) for x in range(num_of_players)]

    def play(self):
        while True:
            for player in self.players:
                self.one_player_session(player)
                if player.total_score >= 3000:
                    self.end_game()
                    return

    def one_player_session(self, player):
        self.my_file.write("\nPlayer {0} turn\n".format(player.name))
        player.take_turn()
        do_next_step = 1
        while True:
            if do_next_step:
                new_score, rolled = player.next_step()
                self.my_file.write('# Rolled: {0}\n'.format(rolled))
                self.my_file.write('## Score = {0}\n'.format(new_score))
                if new_score == 0:
                    player.turn_score = 0
                    player.end_turn()
                    break
                self.my_file.write('## Number of next step dices = {0}\n'
                           .format(player.num_of_dice))
            else:
                player.end_turn()
                break
            do_next_step = random.randint(0, 1)
        self.my_file.write('--- Total {0} ---\n'.format(player.total_score))

    def end_game(self):
        self.my_file.write("----- Last round -----\n")
        for player in self.players:
            self.one_player_session(player)
        winner = max(self.players, key=lambda item: item.total_score)
        self.my_file.write("\n----- The END -----\n")
        self.my_file.write("****Winner is  player {0} with score {1}****\n"
                    .format(winner.name, winner.total_score))


if __name__ == '__main__':
    my_file = open("game.txt", "w")
    game = Game(4, my_file)
    game.play()
    my_file.close()
