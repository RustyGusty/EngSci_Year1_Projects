#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "seamcarving.h"
#include "math.h"

typedef struct rgb_img rgb_img;

int x_energy(rgb_img* im, int y, int x, int color) {
	int target_left = x - 1;
	if (target_left < 0)
		target_left = im->width - 1;
	
	int target_right = x + 1;
	if (target_right >= im->width)
		target_right = 0;

	return get_pixel(im, y, target_left, color) - get_pixel(im, y, target_right, color);
}

int y_energy(rgb_img* im,int y, int x, int color) {
	int target_up = y - 1;
	if (target_up < 0)
		target_up = im->height - 1;

	int target_down = y + 1;
	if (target_down >= im->height)
		target_down = 0;

	return get_pixel(im, target_up, x, color) - get_pixel(im, target_down, x, color);
}

int pixel_energy(rgb_img* im, int y, int x) {
	int res = 0;
	
	for (int i = 0; i < 3; i++) {
		int x_e = x_energy(im, y, x, i);
		int y_e = y_energy(im, y, x, i);
		res += x_e * x_e + y_e * y_e;
	}
	return (int) sqrt(res);
}

// 50 minutes, including understanding the functions and everyfin)
void calc_energy(struct rgb_img* im, struct rgb_img** grad) {
	create_img(grad, im->height, im->width);
	for (int row = 0; row < im->height; row++) {
		for (int col = 0; col < im->width; col++) {
			uint8_t energy = pixel_energy(im, row, col) / 10;
			set_pixel(*grad, row, col, energy, energy, energy);
		}
	}
}

void compute_row(rgb_img* grad, double* best_arr, int y) {
	for (int i = 0; i < grad->width; i++) {
		double min_from_above = 0;
		if (y != 0) {
			min_from_above = best_arr[(y - 1) * grad->width + i];
			double opt;
			// Left check
			if (i > 0) {
				opt = best_arr[(y - 1) * grad->width + i - 1];
				if (opt < min_from_above)
					min_from_above = opt;
			}
			// Right check
			if (i < grad->width) {
				opt = best_arr[(y - 1) * grad->width + i + 1];
				if (opt < min_from_above)
					min_from_above = opt;
			}
		}
		best_arr[y * grad->width + i] = min_from_above + get_pixel(grad, y, i, 0);
	}
}

// 20 minutes
void dynamic_seam(struct rgb_img* grad, double** best_arr) {
	*best_arr = (double*)malloc(sizeof(double) * grad->height * grad->width);
	for (int i = 0; i < grad->height; i++) {
		compute_row(grad, *best_arr, i);
	}
}

int min_ind_row(double* best, int row, int width) {
	double min_value = best[row * width];
	int min_index = 0;
	for (int i = 0; i < width; i ++) {
		if (best[row * width + i] < min_value) {
			min_value = best[row * width + i];
			min_index = i;
		}
	}
	return min_index;
}

int min_ind_adj(double* best, int row, int col, int width) {
	// Row is the row being looked at, col is the position of the previous best
	double min_value = best[row * width + col];
	int min_index = col;
	for (int i = col-1; i <= col + 1; i+=2) {
		if (i < 0 || i >= width)
			continue;
		if (best[row * width + i] < min_value) {
			min_value = best[row * width + i];
			min_index = i;
		}
	}
	return min_index;
}

// 10 minutes
void recover_path(double* best, int height, int width, int** path) {
	*path = (int*)malloc(sizeof(int) * height);

	(*path)[height - 1] = min_ind_row(best, height - 1, width);
	for (int row = height - 2; row >= 0; row--) {
		(*path)[row] = min_ind_adj(best, row, (*path)[row + 1], width);
	}
}

void cpy_rgb(rgb_img* im, rgb_img* dest, int y, int x, int cur_index) {
	uint8_t rgb[3];
	for (int i = 0; i < 3; i++) {
		rgb[i] = get_pixel(im, y, x, i);
	}
	set_pixel(dest, y, cur_index, rgb[0], rgb[1], rgb[2]);
}

// 20 Minutes
void remove_seam(struct rgb_img* src, struct rgb_img** dest, int* path) {
	create_img(dest, src->height, src->width - 1);
	for (int i = 0; i < src->height; i++) {
		int cur_index = 0;
		for (int j = 0; j < src->width; j++) {
			if (j != path[i]) {
				cpy_rgb(src, *dest, i, j, cur_index);
				cur_index += 1;
			}
		}
	}
}

void print_img(rgb_img* im) {
	for (int i = 0; i < im->height; i++) {
		for (int j = 0; j < im->width; j++) {
			printf("%d %d %d\t", get_pixel(im, i, j, 0), get_pixel(im, i, j, 1), get_pixel(im, i, j, 2));
		}
		printf("\n");
	}
	printf("\n");
}

void test(int iterations) {
	struct rgb_img* im;
	struct rgb_img* cur_im = 0;
	struct rgb_img* grad;
	double* best;
	int* path;

	read_in_img(&im, "HJoceanSmall.bin");
	for (int i = 0; i < iterations; i++) {
		printf("i = %d\n", i);
		calc_energy(im, &grad);
		dynamic_seam(grad, &best);
		recover_path(best, grad->height, grad->width, &path);
		remove_seam(im, &cur_im, path);

		/*
		char filename[200];
		sprintf(filename, "img%d.bin", i);
		write_img(cur_im, filename);
		*/

		destroy_image(im);
		destroy_image(grad);
		free(best);
		free(path);
		im = cur_im;
	}
	
	char filename[200];
	sprintf(filename, "img%d.bin", iterations);
	write_img(cur_im, filename);
	destroy_image(im);
}