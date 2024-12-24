from functools import cache

class Secret:
    @classmethod
    @cache
    def generate_next(cls, n):
        n = Secret.prune_mix(n, n * 64)
        n = Secret.prune_mix(n, n // 32)
        n = Secret.prune_mix(n, n * 2048)
        return n

    @classmethod
    def generate_all(cls, n, times):
        for _ in range(times):
            n = cls.generate_next(n)
            yield n

    @staticmethod
    @cache
    def mix(n1, n2):
        return n1 ^ n2
    
    @staticmethod
    @cache
    def prune(n):
        return n % 16777216
    
    @staticmethod
    @cache
    def prune_mix(n1, n2):
        return Secret.prune(Secret.mix(n1, n2))
    
class Market:
    GENERATE_AMT = 2000
    SEQUENCE_LENGTH = 4

    def __init__(self, secret_numbers = []):
        self.secret_numbers = secret_numbers

    def from_file(self, file):
        with open(file) as f:
            self.secret_numbers = list(map(int, f.read().splitlines()))
        return self

    def get_nths(self, n):
        for secret in self.secret_numbers:
            yield list(Secret.generate_all(secret, n))[-1]

    @staticmethod
    @cache
    def get_price(n):
        return int(str(n)[-1])

    def get_price_changes(self, n):
        changes = {}
        for secret in self.secret_numbers:
            prices = [Market.get_price(secret)]
            prices.extend(list(map(Market.get_price, Secret.generate_all(secret, n))))
            changes[secret] = {}
            changes[secret]["prices"] = prices[1:]
            changes[secret]["changes"] = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        return changes
    
    @staticmethod
    def find_sublist(list, sublist):
        for i in range(len(list) - len(sublist) + 1):
            if list[i:i + len(sublist)] == sublist:
                return i + len(sublist) - 1
        return None
    
    def find_sequence(self, n):
        price_changes = self.get_price_changes(n)

        base_changes = price_changes[self.secret_numbers[0]]["changes"]
        base_prices = price_changes[self.secret_numbers[0]]["prices"]
        sublists = []
        for i in range(Market.SEQUENCE_LENGTH - 1, len(base_changes)):
            sublists.append((base_prices[i], base_changes[i - Market.SEQUENCE_LENGTH + 1:i + 1]))
        sublists.sort(key = lambda sublist: sublist[0], reverse = True)
        sublists = [sublist[1] for sublist in sublists]

        sequences = []
        for sublist in sublists:
            total_price = 0
            for secret in self.secret_numbers:
                change_list = price_changes[secret]["changes"]
                price_i = Market.find_sublist(change_list, sublist)
                if price_i is not None:
                    total_price += price_changes[secret]["prices"][price_i]
            sequences.append((total_price, sublist))
        sequences.sort(key = lambda sequence: sequence[0], reverse = True)
        return sequences[0]
    
class Test:
    PART_1_TESTS = {
        1: 8685429,
        10: 4700978,
        100: 15273692,
        2024: 8667524
    }
    PART_2_TESTS = {
        "input": [1, 2, 3, 2024],
        "sequence": (23, [-2, 1, -1, 3])
    }

    @classmethod
    def run(cls):
        market = Market(cls.PART_1_TESTS.keys())
        results = list(market.get_nths(Market.GENERATE_AMT))
        for i, test in enumerate(cls.PART_1_TESTS.items()):
            n, expected = test
            assert results[i] == expected, f"Part 1 test failed for n = {n}, expected {expected}, got {results[i]}"

        market = Market(cls.PART_2_TESTS["input"])
        sequence = market.find_sequence(Market.GENERATE_AMT)
        assert sequence == cls.PART_2_TESTS["sequence"], f"Part 2 test failed, expected {cls.PART_2_TESTS['sequence']}, got {sequence}"

Test.run()
market = Market().from_file("22/input.txt")
print(sum(market.get_nths(Market.GENERATE_AMT)))
print(market.find_sequence(Market.GENERATE_AMT))