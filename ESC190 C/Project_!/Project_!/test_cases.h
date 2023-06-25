#if !defined(TEST_CASES_H)
#define TEST_CASES_H

typedef struct two_ints {
    int count_correct;
    int total_count;
} two_ints;

char* get_target_term(char* dest, int i);
two_ints test_read(term** p_terms, int* p_nterms, char* filename);
int my_pow10(int exp);
two_ints test_match(term* terms, int nterms, char* substr);
two_ints test_answer(term** p_answer, int* n_answers, term* terms, int nterms, char* substr);
two_ints my_test(char* filename);

#endif
