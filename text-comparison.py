import math

def clean_text(text):
    """Returns text in all lowercase with most punctuation excluded"""
    #Make lowercase
    clean = text.lower()
    #Remove punctuation
    for i in "\".,?!()$&/[]:;":
        clean = clean.replace(i, '')
    #Special case for - because it is normally used for normally separate words
    clean = clean.replace('-', ' ')
    return clean

def partial_clean(text):
    """Removes punctuation that doesn't end a sentence"""
    clean = text.lower()
    for i in "\",()$&/[]:\\":
        clean = clean.replace(i, '')
    clean.replace('-', ' ')
    return clean

def save_dict(fileName, dictToSave):
    """Saves the given dict to a file of the given name."""
    f = open(fileName, 'w')
    f.write(str(dictToSave))
    f.close()

def load_dict(fileName):
    """Loads given file and returns dict"""
    f = open(fileName, 'r')
    dict_str = f.read()
    f.close()

    return dict(eval(dict_str))

def stem(stringToStem):
    """Returns the stem of the given word"""
    stem = stringToStem
    if stem[-1] == "s":
        stem = stem[:-1]
    if len(stem) >= 5:
        if stem[-2:] == "ly":
            stem = stem[:-2]
        if stem[-3:] == "ing":
            stem = stem[:-3]
        elif stem[-2:] == "ed":
            stem = stem[:-2]
        elif stem[-2:] == "er":
            stem = stem[:-2]
        if len(stem) > 2:
            if stem[-1] == stem[-2]:
                stem = stem[:-1]
            if stem[-1] == 'i':
                stem = stem[:-1] + 'y'
    if len(stem) >0:
        if stem[-1] == 'e':
            stem = stem[:-1]

    return stem

def compare_dictionaries(d1, d2):
    """Finds the similarity score of two dictionaries"""
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for i in d2:
        if i in d1:
            score += d2[i] * math.log(d1[i]/total)
        else:
            score += d2[i] * math.log(.5/total)

    return score

class TextModel():
    def __init__(self, model_name):
        """Initializes a model with given name and no text"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.sentence_starters = {}

    def __repr__(self):
        """"Returns a string with name, number of words, and number of word lengths"""
        s = "text model name: " + self.name
        s += "\n" + "number of words: " + str(len(self.words))
        s += "\n" + "number of word lengths: " + str(len(self.word_lengths))
        s += "\n" + "number of word stems: " + str(len(self.stems))
        s += '\n' + "number of sentence starters: " + str(len(self.sentence_starters))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """

        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        word_list = partial_clean(s).split()
        count = 0
        for i in range(len(word_list)):
            #Check first word in sentence
            if word_list[i-1][-1] in '.?!;':
                if word_list[i] in self.sentence_starters:
                    self.sentence_starters[word_list[i]] += 1
                else:
                    self.sentence_starters[word_list[i]] = 1

            count += 1
            if word_list[i][-1] in ".?!;":
                if count in self.sentence_lengths:
                    self.sentence_lengths[count] += 1
                else:
                    self.sentence_lengths[count] = 1
                count = 0

        word_list = clean_text(s).split()

        # Template for updating the words dictionary.
        for w in word_list:
            # Update self.words to reflect w
            # either add a new key-value pair for w
            # or update the existing key-value pair.
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
        # Add code to update other feature dictionares.
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1

            wStem = stem(w)
            if wStem in self.stems:
                self.stems[wStem] += 1
            else:
                self.stems[wStem] = 1

    def add_file(self, fileName):
        """Adds a text document to the model"""
        file = open(fileName, 'r', encoding='utf8', errors='ignore')
        fileString = file.read()
        self.add_string(fileString)

    def similarity_scores(self, other):
        """Returns a list of similarity scores for all attributes"""
        return[compare_dictionaries(other.words, self.words), compare_dictionaries(other.word_lengths, self.word_lengths),
               compare_dictionaries(other.stems, self.stems), compare_dictionaries(other.sentence_lengths, self.sentence_lengths),
               compare_dictionaries(other.sentence_starters, self.sentence_starters)]

    def classify(self, source1, source2, wordsWeight = 10, wordLengthWeight = 7, stemWeight = 4, sentenceLengthWeight = 4, sentenceStarterWeight = 6):
        """Determines wether the model is more like source 1 or source 2"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        weights = [wordsWeight, wordLengthWeight, stemWeight, sentenceLengthWeight, sentenceStarterWeight]
        score1Total = 0
        score2Total = 0
        for i in range(len(scores1)):
            score1Total += scores1[i] * weights[i]
            score2Total += scores2[i] * weights[i]
        if score1Total >= score2Total:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)


    def save_model(self):
        """Saves the model to files"""
        save_dict(self.name + "_words.txt", self.words)
        save_dict(self.name + "_word_lengths.txt", self.word_lengths)
        save_dict(self.name + "_stems.txt", self.stems)
        save_dict(self.name + "_sentence_lengths.txt", self.sentence_lengths)
        save_dict(self.name + "_sentence_starters.txt", self.sentence_starters)

    def read_model(self):
        """Loads model from files"""
        self.words = load_dict(self.name + "_words.txt")
        self.word_lengths = load_dict(self.name + "_word_lengths.txt")
        self.stems = load_dict(self.name + "_stems.txt")
        self.sentence_lengths = load_dict(self.name + "_sentence_lengths.txt")
        self.sentence_starters = load_dict(self.name + "_sentence_starters.txt")

def run_tests():
    """ Runs tests given sources and texts to analyze to determine similarity """
    source1 = TextModel('Shakespeare')
    source1.add_file('shaks12.txt')
    #Don't forget to save
    source1.save_model()

    source2 = TextModel('Star Wars')
    source2.add_file('ANH_screenplay.txt')
    source2.add_file('ESB_screenplay.txt')
    source2.add_file('RotJ_screenplay.txt')
    source2.add_file('TPM_screenplay.txt')
    source2.add_file('AotC_screenplay.txt')
    source2.add_file('RotS_screenplay.txt')
    source2.save_model()

    new1 = TextModel('WR120')
    new1.add_file('Vladek.txt')
    new1.classify(source1, source2)
    new1.save_model()

    new2 = TextModel('Force Awakens')
    new2.add_file("TFA_screenplay.txt")
    new2.classify(source1, source2)
    new2.save_model()

    new3 = TextModel("Macbeth")
    new3.add_file("Macbeth.txt")
    new3.classify(source1, source2)
    new3.save_model()

    new4 = TextModel("Game of Thrones")
    new4.add_file("Game_Of_Thrones.txt")
    new4.classify(source1, source2)
    new4.save_model()

run_tests()