import synonyms as me
import samuelnyms as sam
import time as t

def time_semantic_descriptors_from_files(filenames):
    start_time = t.time()
    sentences = []
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
    text_time = t.time()
    print("Time to read text: ", text_time - start_time)
    temp = me.build_semantic_descriptors(sentences)
    build_time = t.time()
    print("Time to build descriptors: ", build_time - start_time)
    return temp

def check_discord():
    semantic_descriptors = me.build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt", "text3.txt", "text4.txt", "text5.txt", "text6.txt"])

    my_res = semantic_descriptors["suspicious"]

    their_res = {'but': 6, 'of': 9, 'all': 2, 'these': 1, 'various': 1, 'suspected': 1, 'characters': 1, 'pierre': 1, 'was': 7, 'considered': 1, 'to': 7, 'be': 3, 'the': 9, 'most': 1, 'we': 1, 'learn': 1, 'that': 7, 'luther': 1, 'had': 6, 'a': 9, 'hot': 1, 'temper': 1, 'and': 8, 'said': 4, 'such': 1, 'things': 1, 'rousseau': 1, 'wrote': 1, 'books': 1, 'do': 3, 'not': 1, 'why': 1, 'after': 3, 'reformation': 1, 'peoples': 1, 'massacred': 1, 'one': 4, 'another': 2, 'nor': 1, 'during': 1, 'french': 1, 'revolution': 1, 'they': 3, 'guillotined': 1, '"ah': 1, 'good': 1, "that's": 1, 'quite': 1, 'right': 1, 'then': 4, '"': 2, 'he': 6, 'in': 6, 'tone': 1, 'customs': 1, 'official': 1, 'who': 3, 'has': 2, 'been': 5, 'up': 2, 'now': 2, 'hearing': 1, 'your': 1, 'explanations': 1, 'stamps': 1, 'passport': 1, 'lets': 1, 'you': 2, 'proceed': 1, 'on': 1, 'journey': 1, 'without': 1, 'troubling': 1, 'examine': 1, 'luggage': 1, 'she': 3, 'never': 3, 'free': 1, 'interest': 1, 'curiosity': 1, 'shewn': 1, 'his': 5, 'life': 1, 'her': 4, 'passionate': 1, 'desire': 1, 'should': 1, 'favour': 1, 'which': 1, 'it': 3, 'felt': 1, 'as': 4, 'possibly': 1, 'tedious': 1, 'waste': 1, 'time': 1, 'disturbance': 1, 'arrangements': 1, 'granting': 1, 'access': 1, 'study': 1, 'how': 1, 'obliged': 1, 'beg': 1, 'would': 1, 'let': 1, 'take': 1, 'him': 2, "verdurins'": 1, 'when': 2, 'did': 1, 'allow': 1, 'come': 1, 'once': 1, 'month': 1, 'first': 1, 'before': 2, 'himself': 1, 'swayed': 1, 'repeat': 1, 'what': 1, 'joy': 1, 'custom': 1, 'their': 2, 'seeing': 1, 'each': 1, 'other': 1, 'daily': 1, 'for': 4, 'longed': 1, 'at': 1, 'seemed': 1, 'only': 1, 'tiresome': 1, 'distraction': 1, 'since': 1, 'conceived': 1, 'distaste': 1, 'definitely': 1, 'broken': 1, 'herself': 1, 'while': 2, 'become': 1, 'so': 3, 'insatiable': 1, 'dolorous': 1, 'need': 1, 'â\x80\x9d': 2, 'shoshone': 2, 'pete': 2, 'with': 5, 'moisture': 2, 'eyes': 2, 'two': 2, 'men': 2, 'drew': 2, 'away': 2, 'from': 3, 'shack': 2, 'kept': 2, 'view': 2, 'door': 2, 'drawn': 2, 'pistols': 2, 'muriel': 2, 'grown': 2, 'john': 2, 'moment': 2, 'thought': 2, 'taking': 2, 'helpless': 2, 'charge': 2, 'shelter': 2, 'poor': 2, 'feel': 1, 'i': 2, 'have': 1, 'narrow': 1, 'minded': 1, 'beebe': 1, 'just': 1, 'scolding': 1, 'me': 3, 'my': 1, 'nature': 1, 'eager': 1, 'sat': 1, 'opposite': 1, 'trying': 1, 'catch': 1, 'eye': 1, 'vaguely': 1, 'think': 1, 'little': 2, 'either': 1, 'wife': 1, 'or': 1, 'something': 1, 'phenomena': 1, 'almost': 1, 'forced': 1, 'us': 1, 'staircase': 1, 'fried': 1, 'fish': 1, 'man': 1, 'struck': 1, 'an': 1, 'extremely': 1, 'pugnacious': 1, 'looking': 1, 'fellow': 1, 'sargon': 1, 'going': 1, 'lodging': 1, 'house': 1, 'keeper': 1, 'faith': 1, 'new': 1, 'saviour': 1, 'mankind': 1, 'weakened': 1, 'dreadfully': 1, 'were': 1, 'intolerant': 1, 'because': 1, 'want': 1, 'internal': 1, 'assurance': 1, 'saw': 1, 'great': 1, 'vista': 1, 'inquiries': 1, 'made': 1, 'people': 1, 'faced': 1, 'some': 1, 'are': 1, 'cruel': 1, 'arrived': 1, 'flushed': 1, 'dishevelled': 1, 'out': 1, 'breath': 1, 'found': 1, 'inn': 1, 'reluctant': 1, 'announced': 1, 'wanted': 1, 'bill': 1, 'instantly': 1, 'refused': 1, 'any': 1, 'breakfast': 1, 'cup': 1, 'tea': 1, 'chunk': 1, 'bread': 1, 'butter': 1, 'set': 1, 'about': 1, 'packing': 1, 'roll': 1}

    for my_word, my_count in my_res.items():
        try:
            their_count = their_res[my_word]
            if my_count != their_count:
                print(f"{my_word} has a wrong count: {my_count} vs {their_count}")
            del their_res[my_word]
        except KeyError:
            print(f"{my_word} is not in their dictionary!")



def compare_sam():
    my_res = me.time_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt", "bible.txt"])
    their_res = sam.build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt", "bible.txt"])

    # (my_res, their_res) = (their_res, my_res)

    for my_word, my_count in my_res.items():
        try:
            their_count = their_res[my_word]
            # if my_count != their_count:
            #     print(f"{my_word} has a wrong count: {my_count} vs {their_count}")
            # del their_res[my_word]
        except KeyError:
            print(f"{my_word} is not in their dictionary!")