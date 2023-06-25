#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef char my_str[4];

void create_array(my_str* p_arr) {
	for (int d1 = 0; d1 < 10; d1++) {
		for (int d2 = 0; d2 < 10; d2++) {
			for (int d3 = 0; d3 < 10; d3++) {
				(*p_arr)[0] = '0' + d1;
				(*p_arr)[1] = '0' + d2;
				(*p_arr)[2] = '0' + d3;
				(*p_arr)[3] = '\0';
				p_arr++;
			}
		}
	}
}

void shuffle_array(my_str* p_arr, int nterms) {
	my_str temp;
	srand(5);
	for (int i = nterms - 1; i > 0; i--) {
		int ind = rand() % (i + 1);
		strcpy(temp, p_arr[i]);
		strcpy(p_arr[i], p_arr[ind]);
		strcpy(p_arr[ind], temp);
	}
}

void write_to_file(my_str* arr, int nterms) {
	FILE* fp = fopen("TEST_FLOATS.txt", "w");
	if (fp == NULL) {
		printf("No file found");
		exit(-1);
	}
	fprintf(fp, "%d\n", nterms);
	for (int i = 0; i < nterms - 1; i++) {
		fprintf(fp, "    %d.0\t%s\n", 1000 - atoi(arr[i]), arr[i]);
	}
	fprintf(fp, "   %d.0\t%s", 1000 - atoi(arr[999]), arr[999]);
	fclose(fp);
}

int randomize(){
	int nterms = 1000;
	my_str arr[1000];
	my_str* p_arr = arr;
	
	create_array(p_arr);
	shuffle_array(p_arr, nterms);
	write_to_file(p_arr, nterms);

	return 0;
}