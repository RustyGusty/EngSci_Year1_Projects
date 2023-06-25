#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "autocomplete.h"
#include "test_cases.h"

void print_block(term* p_t, int n_terms) {
    for (int i = 0; i < n_terms; i++) {
        printf("%s of weight %lf\n", p_t[i].term, p_t[i].weight);
    }
}

double get_double(char* line) {
    return atof(line);
}

int main(void)
{
    /*printf("Running with ints:\n");
    two_ints res = my_test("TEST_INTS.txt");
    printf("Out of %d tests, you failed %d times.\n", res.total_count, res.total_count - res.count_correct);
    
    printf("\nRunning with floats:\n");
    res = my_test("TEST_FLOATS.txt");
    printf("Out of %d tests, you failed %d times.\n", res.total_count, res.total_count - res.count_correct);
    exit(0);*/
    
    struct term *terms;
    int nterms;

    read_in_terms(&terms, &nterms, "cities.txt");

    //print_block(terms, nterms);
    //exit(0);
    /*
    print_block(terms, nterms);

    const char* substr = "as";

    printf("The lowest match to %s is %d\n", substr, lowest_match(terms, nterms, substr));
    printf("The highest match to %s is %d\n", substr, highest_match(terms, nterms, substr));

    struct term* answers;
    int n_answers;

    autocomplete(&answers, &n_answers, terms, nterms, substr);
    print_block(answers, n_answers);
    
    */

    char* substr = "Tor";

    int low = lowest_match(terms, nterms, substr);
    int high = highest_match(terms, nterms, substr);
    printf("The range of values is from %d to %d\n", low, high);
    
    struct term *answer;
    int n_answer;
    autocomplete(&answer, &n_answer, terms, nterms, substr);
    print_block(answer, n_answer);
    printf("Number of matches: %d\n", n_answer);
    //free allocated blocks here -- not required for the project, but good practice
    free(terms);
    free(answer);

    return 0;
}

