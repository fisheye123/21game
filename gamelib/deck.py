import random

import const


class Hand(object):
    def __init__(self, cards):
        self.hand = cards

    def get_scores(self):
        score = sum(card.score for card in self.hand)
        return score

    def __repr__(self):
        return str(self.hand)


class Card(object):
    def __init__(self, value, suit):
        self.name = const.card_to_name[value]
        self.suit = suit
        self.title = "%s of %s" % (self.name, self.suit)
        self.score = 11 if self.name == "Ace" else value

    def __repr__(self):
        return self.title


class Deck(object):
    deck = []
    for suit in const.suit:
        for card in range(2, 11):
            deck.append(Card(card, suit))
    # deck = [Card(card, suit) for card in range(2, 11) for suit in const.suit]

    def __init__(self, num_decks):
        self.deck = self.deck * num_decks
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def deal_hand(self):
        return Hand([self.deal_card(), self.deal_card()])
