import time as t

def cosine_similarity(vec1, vec2):
    dot_prod = 0
    vec1_mag = 0
    vec2_mag = 0
    # Iterate through the elements of the smaller list to save having to check if word in vec as often
    if len(vec1) < len(vec2):
        vec1, vec2 = vec2, vec1
    for word, count in vec1.items():
        vec1_mag += count ** 2
        if word in vec2:
            dot_prod += count * vec2[word]
    for count in vec2.values():
        vec2_mag += count ** 2

    return dot_prod / ((vec1_mag) ** 0.5 * (vec2_mag) ** 0.5)

def build_semantic_descriptors(sentences):
    # Runtime analysis: s = number of sentences, n = number of words in a sentence
    res = {}
    # s times
    for sentence in sentences:
        # New dictionary to avoid having to index into the full dictionary each time
        sentence_res = []
        # w times
        for word in sentence:
            if word not in sentence_res:
                sentence_res.append(word)
        # w times
        for word in sentence_res:
            if word not in res:
                res[word] = {}
            # Avoid repeatedly searching the dictionary for the reference
            word_dict = res[word]
            # w time
            for sentence_word in sentence_res:
                if sentence_word == word:
                    continue
                if sentence_word not in word_dict:
                    word_dict[sentence_word] = 1
                else:
                    word_dict[sentence_word] += 1
    return res
# Complexity: O(s*w^2) = O(n*w), where s is the number of sentences and w is the number of words in the sentence, and n is the number of words tota

def print_dict(dict):
    for key, value in dict.items():
        print(f"{key}: {value}\n")


def build_semantic_descriptors_from_files(filenames):
    def replace_characters(string, char_list, end_char):
        for char in char_list:
            string = string.replace(char, end_char)
        return string

    sentences = []
    for filename in filenames:
        with open(filename, "r", encoding = "latin1") as f:
            string = f.read().strip().lower()
            string = replace_characters(string, [",", "-", ":", ";"], " ")
            string = replace_characters(string, ["?", "!"], ".")
            file_sentences = string.split(".")
            sentences.extend([file_sentences[i].split() for i in range(len(file_sentences))])

    return build_semantic_descriptors(sentences)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_guess = choices[0]
    best_score = -1

    try:
        word_semantics = semantic_descriptors[word]
    except KeyError:
        return choices[0]

    for choice in choices:
        try:
            choice_semantics = semantic_descriptors[choice]
            score = similarity_fn(word_semantics, semantic_descriptors[choice])
            if score > best_score:
                best_guess = choice
                best_score = score
        except KeyError:
            continue

    return best_guess


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct_guesses = 0
    total_guesses = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.split()
            word = line[0]
            correct = line[1]
            choices = line[2:]
            if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == correct:
                correct_guesses += 1

            total_guesses += 1
    return correct_guesses / total_guesses * 100

if __name__ == "__main__":
    semantic_descriptors = build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"])
    # semantic_descriptors = build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt", "bible.txt", "text3.txt", "text4.txt", "text5.txt", "text6.txt"])

    res = run_similarity_test("test.txt", semantic_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")




