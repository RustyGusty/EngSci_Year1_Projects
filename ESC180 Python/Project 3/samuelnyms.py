'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    numerator = 0
    for key1 in vec1:
        for key2 in vec2:
            if key1 == key2:
                numerator += (vec1.get(key1) * vec2. get(key2))
    return numerator/(norm(vec1)*norm(vec2))

def create_dictionary(sentences):
    dictionary = {}
    for sentence in sentences: # s times
        sentence_dictionary = {}
        for word in sentence: # w times
            sentence_dictionary[word] = {}
        for i in sentence_dictionary: # (w - dupe) times ~ w times
            dictionary[i] = sentence_dictionary[i]
    return dictionary # s * (2w) = O(sw) = O(n)

def remove_duplicates(sentences):
    for sentence in range(len(sentences)): # s times
        unique = []
        for i in range(len(sentences[sentence])): # w times
            if sentences[sentence][i] not in unique:
                unique.append(sentences[sentence][i])
        sentences[sentence] = unique
    return sentences # s * w = O(n)

def build_semantic_descriptors(sentences):
    remove_duplicates(sentences) # O(n)
    word_dictionary = create_dictionary(sentences) # O(n)
    for sentence in sentences: # s times
        for word in sentence: # w times
            for current_word in sentence: # w times
                if current_word != word:
                    if current_word in word_dictionary[word]:
                        word_dictionary[word][current_word] += 1
                    else:
                        word_dictionary[word][current_word] = 1
    return word_dictionary # n + n + s*w^2 ~ O(2n + n*w) ~ O(n) assuming w is constant

import time as t

def build_semantic_descriptors_from_files(filenames):
    start_time = t.time()
    combined_sentences = []
    for filename in filenames:
        sentence = []
        current_text = open(filename, "r", encoding="latin1")
        current_text = current_text.read()
        current_text = current_text.lower()
        current_text = current_text.strip()
        current_text = current_text.replace("?",".")
        current_text = current_text.replace("!",".")
        current_text = current_text.replace(".",".")
        current_text = current_text.replace(","," ")
        current_text = current_text.replace("-"," ")
        current_text = current_text.replace("--"," ")
        current_text = current_text.replace(":"," ")
        current_text = current_text.replace(";"," ")
        current_text = current_text.replace("("," ")
        current_text = current_text.replace(")"," ")
        split = current_text.split(".")
        for word in split:
            sentence.append(word.split())
        combined_sentences += sentence
    text_time = t.time()
    print("Time to read text: ", text_time - start_time)
    temp = build_semantic_descriptors(combined_sentences)
    build_time = t.time()
    print("Time to build descriptors: ", build_time - start_time)
    return temp

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity_score = 0.0
    best_choice_index = 0

    for i in range(len(choices)):
        if choices[i] not in semantic_descriptors or word not in semantic_descriptors:
            similarity_score = -1
        else:
            similarity_score = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
        if similarity_score > max_similarity_score:
            best_choice_index = i
            max_similarity_score = similarity_score
    return choices[best_choice_index]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct_choices = 0.0
    similarity_tests = open(filename, "r", encoding="latin1")
    similarity_tests = similarity_tests.read()
    similarity_tests = similarity_tests.strip()
    similarity_tests = similarity_tests.split("\n")
    total_tests = len(similarity_tests)
    for test in range(len(similarity_tests)):
        similarity_tests[test] = similarity_tests[test].split()
        if most_similar_word(similarity_tests[test][0], similarity_tests[test][2:], semantic_descriptors, similarity_fn) == similarity_tests[test][1]:
            correct_choices += 1
        #     print(similarity_tests[test], "passed.")
        # else:
        #     print(similarity_tests[test], "failed. Should be", similarity_tests[test][1], "but said", most_similar_word(similarity_tests[test][0], similarity_tests[test][2:], semantic_descriptors, similarity_fn), "instead.")
    return (correct_choices/total_tests) * 100

sentences = [["i", "am", "a", "sick", "man", "a", "a"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]

if __name__ == "__main__":
    semantic_descriptors = build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt", "bible.txt"])
    print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))