# Program to read in one or two files containing the works to be analysed and build a profile for each
# and as an opption, compare the distance of the two profiles and return a score

import os
import math


# check if the three arguments are valid or not
def error_handle(textfile1, arg2, normalize):
    # check boolean value
    if normalize is False:
        pass
    elif normalize is True:
        pass
    else:
        print("Boolean value expected for the third argument.")
        return None

    # check if file1 exists or not and empty or not
    try:
        if os.stat(textfile1).st_size == 0:
            print(textfile1 + " is empty.")
    except OSError:
        print(textfile1 + " does not exist.")
        return None

    # check if file2 exists or not and empty or not
    try:
        if arg2.lower() == "listing":
            pass
        elif os.stat(arg2).st_size == 0:
            print(arg2 + " is empty.")
    except OSError:
        print(arg2 + " does not exist. Please enter \"listing\" or a correct file name.")
        return None

    return textfile1, arg2, normalize


# read contents from file, construct a list of sentences, return the list and the number of paragraphs
def get_file(textfile1):
    file = open(textfile1, "r")
    content = file.read()
    n = content.count("\n\n")

    # calculate the number of paragraphs
    if n < 1:
        num_paragraph = 1
    else:
        num_paragraph = content.count("\n\n") + 1

    # construct a list of sentences
    word_list = content.split()
    sentence_list = []
    sentence = ""

    for item in word_list:
        last_char = item[-1]

        if last_char in [".", "?", "!"]:
            sentence += item
            sentence_list.append(sentence)
            sentence = ""
        elif last_char in ["'", "\""]:
            if item[-2] in [".", "?", "!"]:
                sentence += item
                sentence_list.append(sentence)
                sentence = ""
            else:
                sentence += item + " "
        else:
            sentence += item + " "

    return sentence_list, num_paragraph


# create a profile for the text, return the dictionary contains the profile and the number of sentences
def words_punctuation(sentence_list, num_paragraph):
    # construct a dictionary contains number of ",",";","'","-"
    content = "".join(sentence_list).lower().replace("--", " ")
    word_list = []
    dic = {}
    num_quote = 0
    num_hyphen = 0

    for sentence in sentence_list:
        single_sentence = sentence.split()
        for n in range(len(single_sentence)):
            word_list.append(single_sentence[n].lower().replace("--", " "))

    for word in word_list:
        last_char = word[-1]

        for last_char in ",;":
            dic[last_char] = content.count(last_char)

        for i in range(len(word)):
            if word[i] == "'":
                if i - 1 >= 0 and i + 1 < len(word):
                    if word[i - 1].isalpha() and word[i + 1].isalpha():
                        num_quote += 1
                        dic[word[i]] = num_quote

            if word[i] == "-":
                if i - 1 >= 0 and i + 1 < len(word):
                    if word[i - 1].isalpha() and word[i + 1].isalpha():
                        num_hyphen += 1
                        dic[word[i]] = num_hyphen

    # construct a dictonary contains number of punctuations
    for ch in "'.?! \"\n\t,-;:@#$&()$%+-*/<>=[]\\_{}|~^":
        content = content.replace(ch, " ")
    text = content.split()
    words_tobe_counted = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of", "or",
                          "since", "that", "though", "until", "when", "whenever", "whereas", "which", "while", "yet"]

    dic_punc = {}
    for k in range(len(words_tobe_counted)):
        item = words_tobe_counted[k]
        dic_punc[item] = text.count(item)

    # construct a dictioonary contains sentances per paragraph and words per sentance
    dic_sen_word = {}
    cont = " ".join(sentence_list).lower().replace("--", " ")

    for j in range(len(sentence_list)):
        num_sentence = j + 1

    for sentence in sentence_list:
        for w1 in "\"":
            cont1 = cont.replace(w1, "")
            for w2 in ",":
                cont2 = cont1.replace(w2, " ")
                list_of_words = cont2.split()
                num_word = len(list_of_words)

    dic_sen_word["sentance_per_para"] = num_sentence / num_paragraph
    dic_sen_word["word_per_sentance"] = num_word / num_sentence

    # combine the dictionaries
    dic.update(dic_punc)
    dic.update(dic_sen_word)

    return dic, num_sentence


# normalise the profile
def normalise(dic, num_sentence):
    new_dic = {}
    key_list = dic.keys()
    for item in key_list:
        if item == "sentance_per_para" or item == "word_per_sentance":
            new_dic[item] = dic[item]
        else:
            new_dic[item] = round(dic[item] / num_sentence, 4)
    dic = new_dic
    return dic


# print out the profile by descending order
def output(dic):
    items = list(dic.items())
    items.sort()
    for i in range(len(dic)):
        word, count = items[i]
        count = "%.4f" % count
        print("{0:<20}{1:>5}".format(word, count))


# calculate the distance between two profiles
def dist(profile_1, profile_2):
    key_list = profile_1.keys()
    sum_item = 0

    for item in key_list:
        distance = (float(profile_1[item]) - float(profile_2[item])) ** 2
        sum_item += distance

    score = "%.4f" % math.sqrt(sum_item)

    print("The distance between the two texts is: {0:^5}".format(score))


# if two text files were given, construct profile_1 for the first file
def profile1(textfile1):
    sentence_list, num_paragraph = get_file(textfile1)
    dic, num_sentence = words_punctuation(sentence_list, num_paragraph)
    profile_1 = normalise(dic, num_sentence)
    return profile_1


# if two text files were given, construct profile_2 for the second file
def profile2(arg2):
    sentence_list, num_paragraph = get_file(arg2)
    dic, num_sentence = words_punctuation(sentence_list, num_paragraph)
    profile_2 = normalise(dic, num_sentence)
    return profile_2


def main(textfile1, arg2, normalize=False):
    # check the arguments are valid or not
    # if the arguments are not valid, stop the program
    if error_handle(textfile1, arg2, normalize) is None:
        print("Program stopped because of the wrong argument.")
        return None

    # if the second is "listing", construct and print the profile
    if arg2.lower() == "listing":
        print("profile of text", textfile1)
        sentence_list, num_paragraph = get_file(textfile1)
        dic, num_sentence = words_punctuation(sentence_list, num_paragraph)

        # if the third argument is True, construct and print the normalised profile
        if normalize == True:
            dic = normalise(dic, num_sentence)
        output(dic)

    # if the second argument is a text file and the third argument is true
    # construct two profiles, compare the normalised profiles and print out the score
    # if the third argument is false, compare the profiles and print out the score
    elif os.path.exists(arg2) is True:
        if normalize == True:
            profile_1 = profile1(textfile1)
            profile_2 = profile2(arg2)
            dist(profile_1, profile_2)
        else:
            profile_1 = words_punctuation(get_file(textfile1)[0], get_file(textfile1)[1])[0]
            profile_2 = words_punctuation(get_file(arg2)[0], get_file(arg2)[1])[0]
            dist(profile_1, profile_2)


# nubers2text2 . py
# A progra to convert a sequence of Unicode nubers into
# a string of text . Efficient version using a list accuulator .
def main():
    print("This program converts a sequence of Unicode nubers into ")
    print("the string of text that it represents . \n")
    # Get the message to encode
    inString = input("Please enter the Unicode-encoded message : ")
    # Loop through each substring ad build Unicode message
    chars = []
    for numStr in inString.split():
        code = int(numStr)
        chars.append(chr(code))
        message = " ".join(chars)
        # convert digits to a nuber
        # accuulate new character
        print(" \nThe decoded message is : ", message)


main()