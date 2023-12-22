from utils import profile_and_print_result, get_line_content
from collections import Counter


class HandEvaluator:
    def __init__(self, cards_rank: str):
        self.cards_rank = cards_rank

    def eval_card(self, hand: str) -> int:
        """
        returns a value based on the individual
        value of each card on a hand.
        ABCDE

        # Basically converting a number of base 13 to base 10

        value = value('A') * 13^5 + value('B') * 13^4 .... value('E') * 13^0

        Value ranges from 0 (i.e., '22222') to (i.e., 'AAAAAA') 371292
        """
        value = 0
        total_cards = len(hand)
        base = len(self.cards_rank)
        for pos in range(0, total_cards):
            card = hand[pos]
            card_value = self.cards_rank.find(card)
            value += pow(base, total_cards - 1 - pos) * card_value

        return value

    @staticmethod
    def eval_kind(hand: str):
        counter = sorted(Counter(hand).items(), key=lambda item: item[1])
        counter.reverse()
        if counter[0][1] == 5:
            return 6
        elif counter[0][1] == 4:
            return 5
        elif counter[0][1] == 3 and counter[1][1] == 2:
            return 4
        elif counter[0][1] == 3 and counter[1][1] == 1:
            return 3
        elif counter[0][1] == 2 and counter[1][1] == 2:
            return 2
        elif counter[0][1] == 2:
            return 1
        else:
            return 0


def parse_input(cards_and_bets: [str]) -> [(str, int)]:
    """
    From ['32T3K 765', 'T55J5 684', 'KK677 28', 'KTJJT 220', 'QQQJA 483'] :
    to [('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)]
    """
    result = []
    for card_and_bet in cards_and_bets:
        split = card_and_bet.split()
        result.append((split[0], int(split[1])))
    return result


def get_total_winnings(hands_ranks: [(str, int, int, int)]) -> int:
    """
    :param hands_ranks: list of (hand, bet, kind rating, hand rating)
    :return: The total winnings
    """
    hands_and_bets = sorted(hands_ranks, key=lambda e: (e[2], e[3]))
    return sum(hands_and_bets[p][1] * (p + 1) for p in range(0, len(hands_and_bets)))


def day7_part1():
    hands_and_bets = get_line_content("input1_day7")
    hands_and_bets = parse_input(hands_and_bets)
    evaluator = HandEvaluator("23456789TJQKA")

    hands_ranks = [
        (h, b, evaluator.eval_kind(h), evaluator.eval_card(h))
        for h, b in hands_and_bets
    ]

    return get_total_winnings(hands_ranks)


def day7_part2():
    hands_and_bets = get_line_content("input1_day7")
    hands_and_bets = parse_input(hands_and_bets)
    cards_rank = "J23456789TQKA"
    hand_evaluator = HandEvaluator(cards_rank)
    hands_ranks = []
    for hand, bet in hands_and_bets:
        max_hand_value = hand_evaluator.eval_kind(hand)
        if "J" in hand:
            for c in cards_rank:
                new_hand = hand.replace("J", c)
                new_hand_value = hand_evaluator.eval_kind(new_hand)
                max_hand_value = max(max_hand_value, new_hand_value)

        hands_ranks.append((hand, bet, max_hand_value, hand_evaluator.eval_card(hand)))

    return get_total_winnings(hands_ranks)


profile_and_print_result(day7_part1)
profile_and_print_result(day7_part2)

#
# Result => 250254244. Time taken 0.013797998428344727 (s)
# Result => 250087440. Time taken 0.043907880783081055 (s)
