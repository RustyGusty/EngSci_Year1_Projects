#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "autocomplete.h"
#include "test_cases.h"

/* Hello reader! Hope you're doing well.

    This file is good to run! Make sure it's in the same folder as autocomplete.c, autocomplete.h,
    test_cases.h, TEST_INTS.txt, TEST_FLOATS.txt

    NOTE: If it says something like "should be "001" but is "001"", then copy-paste the text file rather 
    than downloading it.

    NOTE 2: The function stops running tests once one error is hit (so that it doesn't cause problems down
    the line with invalid data), so that's why fixing one thing could make another mistake pop up.
   
    */

/*
What does this do? Well, the text file is 3-digit numbers with leading zeros, and the weights are just the inverse
of the number, allowing for easier checks that your code is doing well. You can write your own checks down in the
my_test function and I (should) have it set up to make sure everything works good!

This took way too long, and I don't know why it did tbh. Even ended up writing a shuffling function in C to randomly
scrambe the 3-digit terms. Goodness.
*/

/*
CHANGELOG:
-> Added comments to everything
-> Fixed wrong const declaration
-> Optimized get_target_term

-> Made code automatically work in VS Code
-> Added a float check with a differently-randomized set of terms
-> Added happy print statements when tests succeed
*/

char* get_target_term(char* dest, int i) {
    /* Given an integer, returns the string corresponding to i with leading
    such that dest has a 3-character string (+ '\0') */
    char temp[3]; // I'm not storing 3-character strings here, since no trailing zeros are needed
    if (i < 10) {
        // Like printf, but instead of printing it just stores the resulting string into a variable
        sprintf(dest, "00%d", i);
    }
    else if (i < 100) {
        sprintf(dest, "0%d", i);
    }
    else {
        sprintf(dest, "%d", i);
    }
    return dest;
}

two_ints test_read(term** p_terms, int* p_nterms, char* filename) {
    /* After running the read_in_terms function, first checks the number of terms returned. Then, 
    it checks every index and checks whether or not it is the correct term and weight. 
    
    At the end, *p_terms will be a pointer to a block of *p_nterms terms.
    */
    two_ints res = { 0, 0 };
    read_in_terms(p_terms, p_nterms, filename);

    // First, check the number of terms returned (to avoid invalid indexing)
    if (*p_nterms != 1000) {
        printf("Got %d terms, expected %d terms", *p_nterms, 1000);
        return res;
    }

    // Only 3-digit terms allowed
    char target_term[4];
    // Used to not doubly-increment on failed term and weights
    int case_passed = 1;
    for (int i = 0; i < *p_nterms; i++) {
        // At index i, the term should be i as a string with leading zeros if necessary
        get_target_term(target_term, i);
        
        if (strcmp((*p_terms)[i].term, target_term) != 0) {
            printf("At index %d, the term is %s but it should be %s\n", i, (*p_terms)[i].term, target_term);
            case_passed = 0; // Set fail flag
        }
        // The way it's organized, the weight for each term corresponds to 1000 - (int) term
        if ((*p_terms)[i].weight != (double)(1000 - i)) {
            printf("At index %d, the weight is %f but it should be %f\n", i, (*p_terms)[i].weight, (double)(1000 - i));
            case_passed = 0; // Set fail flag
        }
        res.total_count++;
        // Simple optimization: Adds 0 if a case was failed, otherwise adds 1. (less lines, less readability)
        res.count_correct += case_passed;
        // Reset the fail counter
        case_passed = 1;
    }
    return res;
}

int my_pow10(int exp) {
    // C doesn't have a nice exponentiation built-in, so make one myself. Returns 10^exp
    int res = 1;
    for (int i = 0; i < exp; i++) {
        res *= 10;
    }
    return res;
}

two_ints test_match(term* terms, int nterms, char* substr) {
    /*
    Runs your lowest_match and highest_match functions and compares them with the expected locations of those
    numbers.
    */

    // sz holds the expected number of terms in answer (100 for 1-digit substr, 10 for 2-digit substr, 1 for 3-digit substr)
    int substr_len = strlen(substr);
    int sz = my_pow10(3 - substr_len);

    // Lower: substr * size
    // Higher: lower + size (minus 1 for fencepost issues)
    // e.g. if "90", then start at index 900 for "900", "901", ..., "909"
    int expected_lower = atoi(substr) * sz;
    int expected_higher = expected_lower + sz - 1;

    // Start assuming all correct, and decrement if things are wrong (Good efficiency, poor readability)
    two_ints res = { 2, 2 };
    int low = lowest_match(terms, nterms, substr);
    if (low != expected_lower) {
        printf("Lowest match was %d, expected %d", low, expected_lower);
        res.count_correct--;
    }
    int high = highest_match(terms, nterms, substr);
    if (high != expected_higher) {
        printf("Highest match was %d, expected %d", high, expected_higher);
        res.count_correct--;
    }
    return res;
}

two_ints test_answer(term** p_answer, int* n_answers, term* terms, int nterms, char* substr) {
    /* Runs your autocomplete function on the given substr and compares them with the expected answer. */
    two_ints res = { 0, 0 };
    char target_term[4];

    autocomplete(p_answer, n_answers, terms, nterms, substr);

    // Same reasoning as in test_match
    int substr_len = strlen(substr);
    int expected_sz = my_pow10(3 - substr_len);
    if (*n_answers != expected_sz) {
        printf("Got %d answers, expected %d answers\n", *n_answers, expected_sz);
    }

    // The offset: i = 0 should correspond to the starting value, so get that starting value from substr
    int offset;

    // atoi discards leading 0's, but we need to use those leading 0's to determine the offest

    // If 2-digit or greater number starting with only 1 zero, then multiply the value by 10
    // "05" should start at index 50 to get "050", "051", etc.
    if (substr[0] == '0' && substr[1] != '0' && substr[1] != '\0') {
        offset = atoi(substr) * 10;
    }
    // If starts with a zero, and is either a 1-digit number, or has it's second digit as 0 also,
    // then just return the atoi of the substr
    // "005" should return 5, "00" should return 0
    else if (substr[0] == '0') {
        offset = atoi(substr);
    }
    // If doesn't start with a zero, then do as normal
    // "50" should return 50 * 10 = 500 to get "500", "501", etc.
    else {
        offset = atoi(substr) * expected_sz;
    }

    // Iterate through all answers and compare them with the expected target
    for (int i = 0; i < *n_answers; i++) {
        // i + offset represents what the index should be.
        // Not checking weight (already checked at read_in_terms)
        get_target_term(target_term, i + offset);
        if (strcmp((*p_answer)[i].term, target_term) != 0) {
            printf("At index %d, the term is %s but it should be %s\n", i, (*p_answer)[i].term, target_term);
            res.count_correct--;
        }
        res.count_correct++;
        res.total_count++;
    }
    return res;
}

// Personalize tests here!
two_ints my_test(char* filename) {
    /* Runs all 3 tests, returning early if ever a failure occurs.
    The return result is the number of tests administered, and the number correct that was gotten. 
    */
    struct term* terms;
    int nterms;
    two_ints res = { 0, 0 }; // Holds count_correct and total_count

    two_ints foo = test_read(&terms, &nterms, filename); // foo is the same as temp. 
    res.count_correct += foo.count_correct;
    res.total_count += foo.total_count;
    if (foo.count_correct != foo.total_count) { // If there was a fail, free all pertinent memory and return early.0
        printf("Fail at reading file\n");
        free(terms);
        return res;
    }
    printf("Reading file success :)\n");

    // PERSONALIZE: Change match_input to any 3-digit number or smaller
    char* match_input = "04";
    foo = test_match(terms, nterms, match_input);
    res.count_correct += foo.count_correct;
    res.total_count += foo.total_count;
    if (foo.count_correct != foo.total_count) {
        printf("Fail at finding matches\n");
        free(terms);
        return res;
    }
    printf("Finding matches success xD\n");

    struct term* answers; int nanswers;
    // Add your own test numbers! (3-digit number at most)
    char test_cases[][4] = {"001", "50", "00", "0", "93", "420", "9"}; // ... you can add as many numbers as you'd like here
    // It's an array of char[4] value, essentailly an array of strings. 
    int len = sizeof(test_cases) / sizeof(char[4]);
    // Iterate sequentially through each test case
    for (int i = 0; i < len; i++) {
        foo = test_answer(&answers, &nanswers, terms, nterms, test_cases[i]);
        res.count_correct += foo.count_correct;
        res.total_count += foo.total_count;
        free(answers);
        if (foo.count_correct != foo.total_count) {
            printf("Fail at autocorrect to '%s'\n", test_cases[i]);
            free(terms);
            return res;
        }
    }
    printf("Getting answers success :O\n");
    free(terms);
    return res;
}

int main1(void) {
    printf("Running with ints:\n");
    two_ints res = my_test("TEST_INTS.txt");
    printf("Out of %d tests, you failed %d times.\n", res.total_count, res.total_count - res.count_correct);

    printf("\nRunning with floats:\n");
    res = my_test("TEST_FLOATS.txt");
    printf("Out of %d tests, you failed %d times.\n", res.total_count, res.total_count - res.count_correct);
    exit(0);
}
