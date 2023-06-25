#include "seamcarving.h"
#include "c_img.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>


typedef struct rgb_img rgb_img;

void test(int iterations);
void print_img(rgb_img* im);

int main1(void) {
	test_p2(30, 10, 10000, 1);
}