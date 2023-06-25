#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "autocomplete.h"

int cmpstr(const void* a, const void* b) {
    char* word1 = (*((term*)a)).term;
    char* word2 = (*((term*)b)).term;
    if (strcmp(word1, word2) > 0) {
        return 1;
    }
    else if (strcmp(word1, word2) < 0) {
        return -1;
    }
    else {
        return 0;
    }
}

void read_in_terms(term** terms, int* pnterms, char* filename) {
    FILE* file = fopen(filename, "r");
    char ch;
    double num = 0;
    do {
        ch = fgetc(file);

        if (ch == '\n' || ch == EOF) {
            break;
        }
        num *= 10;
        num += (int)(ch - '0');
    } while (!(ch == '\n' || ch == EOF));
    *pnterms = num;
    *terms = (term*)malloc(num * sizeof(term));
    int state;
    double num2 = 0;
    int index = 0;
    int index2 = 0;
    for (int i = 0; i < 200; i++) {
        (*terms)[index2].term[i] = 0;
    }
    while (ch != EOF) {
        state = 0;
        if (ch == '\n' || ch == ' ') {
            state = 1;
        }
        ch = fgetc(file);
        if (state == 1 && ch == ' ') {
            continue;
        }
        num2 = 0;
        index = 0;
        while (ch != 9 && ch != EOF) {
            num2 *= 10;
            num2 += (int)(ch - '0');
            ch = fgetc(file);
        }
        ch = fgetc(file);
        while (ch != '\n' && ch != EOF) {
            (*terms)[index2].term[index] = ch;
            index++;
            ch = fgetc(file);
        }
        if (ch == EOF) {
            break;
        }
        (*terms)[index2].term[index] = '\0';
        (*terms)[index2].weight = num2;
        index2++;
    }
    fclose(file);
    qsort(*terms, *pnterms, sizeof(term), cmpstr);
}

int compare_letters(char* word, char* substring) {
    if (strcmp(word, substring) == 0) {
        return 0;
    }
    for (int i = 0; word[i] != 0 && substring[i] != 0; i++) {
        if (word[i] > substring[i]) {
            return 1;
        }
        else if (word[i] < substring[i]) {
            return 2;
        }
    }
    if (strlen(substring) > strlen(word)) {
        return 2;
    }
    return 0;
}

int lowest_match(term* terms, int nterms, char* substr) {
    int x = strlen(substr);
    if (x > 200) {
        return -1;
    }
    else if (x == 0 && nterms > 0) {
        return 0;
    }
    else if (nterms == 0) {
        return -1;
    }
    int low = 0;
    int high = nterms - 1;
    while (high >= low) {
        int mid = (high - low) / 2 + low;
        if ((compare_letters(terms[mid].term, substr) == 0) && (mid == 0 || compare_letters(terms[mid - 1].term, substr) == 2)) {
            return mid;
        }
        else if (compare_letters(terms[mid].term, substr) == 2) {
            low = mid + 1;
        }
        else {
            high = mid - 1;
        }
    }
    return -1;

}

int highest_match(struct term* terms, int nterms, char* substr) {
    int x = strlen(substr);
    if (x > 200) {
        return -1;
    }
    else if (x == 0 && nterms > 0) {
        return 0;
    }
    else if (nterms == 0) {
        return -1;
    }
    int low = 0;
    int high = nterms - 1;
    while (high >= low) {
        int mid = (high - low) / 2 + low;
        if ((compare_letters(terms[mid].term, substr) == 0) && (mid == nterms - 1 || compare_letters(terms[mid + 1].term, substr) == 1)) {
            return mid;
        }
        else if ((compare_letters(terms[mid].term, substr) == 1)) {
            high = mid - 1;
        }
        else {
            low = mid + 1;
        }
    }
    return -1;

}

int cmpnumbers(const void* a, const void* b) {
    double weight1 = (*((term*)a)).weight;
    double weight2 = (*((term*)b)).weight;
    if (weight1 < weight2) {
        return 1;
    }
    else if (weight1 > weight2) {
        return -1;
    }
    else {
        return 0;
    }
}

void autocomplete(term** answer, int* n_answer, term* terms, int nterms, char* substr) {
    int lowest = lowest_match(terms, nterms, substr);
    int highest = highest_match(terms, nterms, substr);
    if (highest != -1 && lowest != -1) {
        *n_answer = highest - lowest + 1;
        *answer = (term*)malloc((highest - lowest + 1) * sizeof(term));
        int counter = 0;
        for (int i = lowest; i <= highest; i++) {
            strcpy((*answer)[counter].term, terms[i].term);
            (*answer)[counter].weight = terms[i].weight;
            counter += 1;
        }
        qsort(*answer, *n_answer, sizeof(term), cmpnumbers);
    }
    else {
        *answer = (term*)malloc((0) * sizeof(term));
        *n_answer = 0;
    }
}



