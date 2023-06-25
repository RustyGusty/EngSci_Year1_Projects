/*
README:

INSTRUCTIONS FOR USE:
Should be good to go as is. Change parameters if you'd like
Compile it together with your c_img.c and seamcarving.c files and let loose!

----------------------------------------------------------------------------
Hello again, it's me.

I mean, this project can most likely be tested just by trying it on the ocean image and seeing the result.
But this will stress-test your recover_path and remove_seam functions.

The idea behind this is to forcefully create data that should give expected solutions, and then see if we
do indeed get the expected solutions. This follows Guerzhoy's debugging tips, but is probably not ideal
for this kind of project, as this function can't differentiate minor imperfections almost at all, only
fundamental mistakes. This is not ideal, since you very likely would have seen this if you did the picture,
but if you are a bit worried maybe this will help.

This was quite a fun little project. Essentially this randomly generates a path from top to bottom, 
and forces the energy through this path to all equal 0. Then, it fills everything else with
random values to (hopefully) get a perfect path.

From testing, you should expect around 1 fail about every 30,000 rows due to luck making a 0 energy directly next
to the path, which causes it to not be the only best path again. I could make it avoid this issue altogether but
that is not quite as fun now is it.

NOTE: If you do set print_fail = 1, the correct path will be identified by "1's"
*/

#include "seamcarving.h"
#include "c_img.h"

// Hopefully you're not doing this still and have it properly configured
// https://piazza.com/class/l7t44yznwpe5i9/post/820
/*
#include "c_img.c"
#include "seamcarving.c"
*/

#include <stdio.h> // printing
#include <stdlib.h> // malloc, rand, free
#include <time.h> // used for setting the seed for the rand() function
#include <math.h> // used for the final probability calculation

typedef struct rgb_img rgb_img; // Cause we're lazy!!!!

// Here's an alternate implementation of a header file: Literally just
// putting the function signatures on top so they can be used
// (Although not needed, it would show a warning and assume an int return
// type, so it's good to get rid of that)
void test_p2(int width, int height, int iterations, int print_fail);

int main(void){
	// Size of the test image (parameters should be above 4)
	int width = 10, height = 30;

	// Number of trials (10000 seeems like a good number fo the 10 x 30 image
	int iterations = 10000;

	// Toggles printing the image states on failures (0 = off, 1 = on)
	int print_fail = 1;
	test_p2(width, height, iterations, print_fail);
}

/*
Creates a random path through the images from top to bottom, starting and ending 
at random positions
*/
void generate_path(rgb_img* img, int** path) {
	*path = (int*)malloc(img->height * sizeof(int));
	(*path)[0] = rand() % img->width; // Random starting position within the range bound [0, width - 1]
	for (int i = 1; i < img->height; i++) {
		int dir = (rand() % 3) - 1; // Random integer -1, 0, or 1
		// Note that this function breaks if width == 1. So don't do that
		if ((*path)[i - 1] == 0 && dir == -1) // If going left at left edge, go right instead
			dir = 1;
		else if ((*path)[i - 1] == img->width - 1 && dir == 1) // If going right at right edge, go left instead
			dir = -1;
		// Move the previous position by 1, 0, or -1 to get the new position.
		(*path)[i] = (*path)[i - 1] + dir;
	}
}

// Only used for debugging, but feel free to call this guy if you'd like
void print_path(int* path, int size) {
	printf("{");
	for (int i = 0; i < size - 1; i++) {
		printf("%d, ", path[i]);
	}
	printf("%d}\n", path[size - 1]);
}

// Note: the wrap-arounds might cause problems at the top and bottom
/*
For example:
0 1 0 Z
X 0 1 0
X Z 0 1
Squares marked "Z" are 0 squares caused by the wrap around from the top and bottom rows
and cause multiple 0-energy zones in the top and bottom rows if the stars align.
Thus, those are not checked in the pathcmp or check_remove functions
*/

/*
Compares the two paths, returning 1 if they are the same, and printing an
error statement and returning 0 if they are different

Note: This is very likely to give spurious results. This is because it is reasonably likely
that multiple squares will have the 0 gradient. For example, If the board is:
1 0 X
1 0 Z
0 1 0
Where squares marked "Z" are randomly generated tiles that happen to be 0, then the gradient will be
0 X X
0 0 X 
X 0 X
Giving multiple paths, so your function may provide the (0, 1, 1) path instead of the (0, 0, 1) path.
This is actually pretty likely (0.01 % chance) since the gradient can only take values from 0 to 44, and it
only needs one tile to generate relatively low rgb values to get a spurious 0 gradient.
*/
int pathcmp(int* true_path, int* path, int size) {
	for (int i = 1; i < size - 1; i++) {
		if (true_path[i] != path[i]) {
			printf("path[%d] = %d when it should be %d\n", i, path[i], true_path[i]);
			return 0;
		}
	}
	return 1;
}

/*
Checks that all the added (1, 1, 1) tiles were deleted, and that all the resulting
res tiles are identical to the src tiles. Since the rest of the tiles are completely
random, there is a very small (1 in ten million) chance of a (1, 1, 1) tile randomly generating somewhere
else, but it is what it is. You should not get any spurious faults from this
*/
int check_remove(rgb_img* res, rgb_img* src) {
	// Idea: Loop through every single tile, and check for a (1, 1, 1) square. If found, print
	// an error statement and eventaull return 1 (still check everything though) Otherwise,
	// if no (1, 1, 1) squares were found, all the tiles were properly removed.
	int return_val = 0;
	for (int i = 1; i < res->height - 1; i++) {
		int seam_offset = 0; // Adds one to all future src checks (note the value directly after the seam is not checked)
		for (int j = 0; j < res->width; j++) {
			int one_count = 0; // If (1, 1, 1), then we have a problem
			int src_one_count = 0; // Sees if src had a seam at that point
			int discrepancy = 0; // 1 if a mismatch is found
			for (int col = 0; col <= 2; col++) {
				uint8_t res_val = get_pixel(res, i, j, col);
				uint8_t src_val = get_pixel(res, i, j, col);
				if (res_val == 1)
					one_count++;
				if (src_val == 1)
					src_one_count++;
				if (res_val != src_val)
					discrepancy = 1;
			}
			if (one_count >= 3) {
				printf("The pixel at (%d, %d) was not removed (probably)\n", i, j);
				return_val = 1;
			}
			if (src_one_count >= 3) {
				seam_offset = 1;
			}
			else if (discrepancy) {
				// Debug here if you want to see the true values
				printf("The pixel at (%d, %d) is wrong\n", i, j);
			}
		}
	}
	return return_val;
}

/*
The main testing function. Given a width and height, prepares a random img file
that should return a path according to the random true_path created, then
checks all the seamcarving.c functions to see if they work
*/
int p_test(int width, int height, int print_fail) {
	int return_val = 1;

	rgb_img* img;
	create_img(&img, height, width);

	// Fill img with random pixels
	for (int i = 1; i < height - 1; i++) {
		for (int j = 0; j < width; j++) {
			set_pixel(img, i, j, rand(), rand(), rand());
		}
	}

	// Create a random path
	int* true_path;
	generate_path(img, &true_path);

	// Set the energies at the path equal to 0 by setting adjacent tiles to (0, 0, 0)
	for (int i = 0; i < height; i++) {
		set_pixel(img, i, true_path[i], 1, 1, 1); // Will be used to check the remove_seam later

		// Handling horizontal wrapping
		if (true_path[i] == 0) {
			set_pixel(img, i, 1, 0, 0, 0);
			set_pixel(img, i, width - 1, 0, 0, 0);
		}
		else if (true_path[i] == width - 1) {
			set_pixel(img, i, 0, 0, 0, 0);
			set_pixel(img, i, width - 2, 0, 0, 0);
		}
		else {
			set_pixel(img, i, true_path[i] - 1, 0, 0, 0);
			set_pixel(img, i, true_path[i] + 1, 0, 0, 0);
		}
	}

	// Deal with vertical wrap around
	set_pixel(img, 0, true_path[height - 1], 0, 0, 0);
	set_pixel(img, height - 1, true_path[0], 0, 0, 0);

	// Prepare all the seamcarving.c functions
	rgb_img* grad;
	double* best;
	int* path;
	calc_energy(img, &grad);
	dynamic_seam(grad, &best);
	recover_path(best, grad->height, grad->width, &path);

	// If the path is not correct, then either print the two gradients or just an error statement
	if (!pathcmp(true_path, path, height)) {
		if (print_fail) {
			printf("The img was:\n");
			print_grad(img);
			printf("\nYour gradient was:\n");
			print_grad(grad);
			printf("\n");
		}
		else {
			printf("Error calculating gradient\n");
		}
		return_val = 0;
	}

	rgb_img* res;
	remove_seam(img, &res, path);
	if (check_remove(res, img)) {
		printf("Error removing seam.\n\n");
		return_val = 0;
	}

	free(true_path);
	free(best);
	free(path);
	destroy_image(img);
	destroy_image(grad);
	destroy_image(res);
	return return_val;

}

/*
Calls p_test iterations times and prints the stats of the trial
*/
void test_p2(int width, int height, int iterations, int print_fail) {
	if (width <= 4 || height <= 4) {
		printf("I don't think this will work with this small a width or height, but here goes.\n");
	}
	srand(time(NULL)); // Set the random seed

	int success_count = 0;
	for (int i = 0; i < iterations; i++) {
		if((i * 4 + 4) % iterations == 0){
			printf("-------------%d%% done------------------------\n", (i * 4 + 4) / iterations * 25);
		}
		if (p_test(width, height, print_fail)) {
			success_count++;
		}
	}

	printf("Out of %d tries, you got %d correct\n", success_count, iterations);

	// Using the normal approximation of the binomial distribution to see the probability of this score or better
	// The proper binomial distribution is too computing-inefficient, but the normal approximation is good
	// for tests with more than 10 iteartions
	double expected_val = (double)iterations / 2; // Assuming 50% probability
	double std = sqrt(iterations * 0.25); // stdev = sqrt(n * p * q) for a binomial distribution
	double z_score = (double)(success_count - 0.5 - expected_val) / std; // How many standard deviations above the mean is your score?
	double probability = 1 - 0.5 * erfc(-z_score * sqrt(0.5)); // probability of getting a number larger than this
	printf("The probability of you getting this score or better randomly (50-50) (aka the probability this was a fluke) is %g\n", probability);
}