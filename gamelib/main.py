import const
import deck

players_list = []


class Player(object):
    def __init__(self, name, hand, end="play", coins=50):
        self.name = name
        self.end = end
        self.coins = coins
        self.current_bet = 0
        self.hand = hand

    def hit(self, card):
        self.hand.hand.append(card)

    def is_busted(self):
        if self.hand.get_scores() > 21:
            return True
        else:
            return False

    def scores(self):
        return self.hand.get_scores()

    def __repr__(self):
        player_str = self.name + "(BUSTED)" if self.is_busted() else self.name
        return "Player: {}\nCoins: {}\nBet: {}\nHand: {}\nScore: {}".format(
            player_str,
            self.coins,
            self.current_bet,
            self.hand,
            self.scores()
        )


def create_players(num_of_players, current_deck):
    players_name = []
    for i in range(1, num_of_players + 1):
        player_name = input(const.color[i - 1] +
                            "Hello, player" + str(i) +
                            ". Enter your name > " +
                            const.color[5])
        players_name.append(player_name)

    for i, name in enumerate(players_name):
        p_hand = current_deck.deal_hand()
        p = Player(name, p_hand)
        players_list.append(p)

        y = False
        while not y:
            bet = input(const.color[i] + "\n" + p.name + ", your bid > ")
            y = bet.isdecimal()
            if y:
                bet = int(bet)
                if bet > 50 or bet < 1:
                    y = False
        p.current_bet = bet
        print(p)
        print(const.color[5])


def create_dealer(current_deck):
    d_hand = current_deck.deal_hand()
    dealer = Player("Dealer", d_hand)
    dealer.coins = 99999
    print(const.color[6] + str(dealer) + const.color[5])
    return dealer


# return win of dealer on first deal
def dealer_win(dealer):
    points = dealer.scores()
    if points == 21:
        for player in players_list:
            player.coins = player.coins - player.current_bet
        print("____________________________\nDialer win!")
        win = True
    else:
        win = False
    return win


# return num of players, who win on first deal
def player_win():
    count_of_end = 0
    for i, player in enumerate(players_list):
        if player.scores() == 21:
            player.coins += player.current_bet * 2
            print(const.color[i] + "____________________________\n" +
                  player.name + " win! " +
                  player.name + " get your doubled bid!\n" +
                  "Coins: " + player.coins +
                  const.color[5])
            player.end = "n"
            count_of_end += 1
    return count_of_end


def res_dealer_win(dealer, player):
    if player.is_busted or (dealer.scores() > player.scores()):
        player.coins -= player.current_bet
        print(player.name + "'s coins: " + str(player.coins))
        print("Dialer win! " + player.name + " lose.\n" + const.color[5])
    else:
        res_player_win(dealer, player)


def res_player_win(dealer, player):
    if dealer.is_busted or (player.scores() > dealer.scores()):
        player.coins += player.current_bet
        print(player.name + "'s coins: " + str(player.coins))
        print(player.name + " win!\n" + const.color[5])


def res_draw(player):
    print(player.name + "'s coins: " + str(player.coins))
    print(player.name + ": Draw!\n" + const.color[5])


def deal(dealer, current_deck):
    # d_points = sum(card.score for card in dealer.hand.hand)
    count_of_end = 0
    d_points = dealer.scores()
    for i, player in enumerate(players_list):
        if player.end != "n":
            p_points = player.scores()
            print(const.color[i] + "\n" + player.name +
                  ", your hand: " + str(player.hand) +
                  "\nScore: " + str(p_points))
            player.end = input("Do you want to hit a card?\n[y/n/stay] > " +
                               const.color[5])
            if player.end.lower() == "y".lower():
                player.end = "play"
                player.hit(current_deck.deal_card())
                p_points = player.scores()
                print(const.color[i])
                print(player)
                print(const.color[5])
                if p_points > 21 or d_points > 21:
                    player.end = "n"
                    count_of_end += 1
            elif player.end.lower() == "n".lower():
                count_of_end += 1
            elif player.end.lower() == "stay".lower():
                print("Skip.")
            else:
                print("Invalid input.")
    if d_points < 16:
        dealer.hit(current_deck.deal_card())
        print(const.color[6])
        print(dealer)
        print(const.color[5])
    return count_of_end


def result(dealer):
    d_points = dealer.scores
    for i, player in enumerate(players_list):
        p_points = player.scores()
        print(const.color[i] + player.name + " points: " + str(p_points))
        if p_points > d_points or dealer.is_busted():
            if p_points < 22:
                player.coins = player.coins + player.current_bet
                print(player.name + "'s coins: " + str(player.coins))
                print(player.name + " win!\n" + const.color[5])
            elif player.is_busted and d_points < 22:
                player.coins = player.coins - player.current_bet
                print(player.name + "'s coins: " + str(player.coins))
                print(player.name + " lose.\n" + const.color[5])
            else:
                print(player.name + "'s coins: " + str(player.coins))
                print(player.name + ": Draw.\n" + const.color[5])  # Bust in both.
        elif d_points == p_points and not dealer.is_busted():  # Equal points, but less than 21.
            print(player.name + "'s coins: " + str(player.coins))
            print(player.name + ": Draw!\n" + const.color[5])
        else:  # The croupier and the player <21. But the player has less points.
            player.coins = player.coins - player.current_bet
            print(player.name + "'s coins: " + str(player.coins))
            print("Dialer win! " + player.name + " lose.\n" + const.color[5])


def newgame():
    global num_of_decks
    y = False
    while not y:
        num_of_decks = input("Set the number of decks(max8) > ")
        y = num_of_decks.isdecimal()
        if y:
            num_of_decks = int(num_of_decks)
            if num_of_decks > 8 or num_of_decks < 1:
                y = False

    y = False
    while not y:
        num_of_players = input("Enter the number of players at the table(max5) > ")
        y = num_of_players.isdecimal()
        if y:
            num_of_players = int(num_of_players)
            if num_of_players > 5 or num_of_players < 1:
                y = False

    d = deck.Deck(num_of_decks)
    print("\nDeck: \n" + str(d.deck) + "\n")

    create_players(num_of_players, d)
    dealer = create_dealer(d)
    dlr_win = dealer_win(dealer)
    count = 0
    count_of_end = 0
    count_of_end += player_win()

    while count_of_end < num_of_players and count < 3 and not dlr_win:
        count += 1
        print(const.color[7] + "\nDealer's deals " + str(count) + ":" + const.color[5])
        count_of_end += deal(dealer, d)

    if not dlr_win:
        print("____________________________")
        print(const.color[6] +
              "Dealer's points: " + str(dealer.scores()) + "\n" +
              const.color[5])
        # result(dealer)
        d_points = dealer.scores()
        for i, player in enumerate(players_list):
            print(const.color[i] + player.name + " points: " + str(player.scores()))
            p_points = player.scores()
            if p_points > 21 and d_points > 21:
                res_draw(player)
            elif d_points == p_points:
                res_draw(player)
            elif d_points < 22:
                res_dealer_win(dealer, player)
            else:
                res_player_win(dealer, player)


def main():
    newgame()
