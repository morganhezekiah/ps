import random, string


class GenerateRandomString(object):
    @staticmethod
    def randomStringGenerator(length):
        letter = ""
        array =[]
        for i in range(length):
            array.append(random.choice(string.ascii_lowercase))
        out = letter.join(array)
        return out