#include <stdio.h>
#include <math.h>
#include "c_img.h"
#include "seamcarving.h"

void calc_energy(struct rgb_img *im, struct rgb_img **grad){ 
    create_img(grad, im->height, im->width);
    for (int y = 0; y < im->height; y++){ 
        for (int x = 0; x < im->width; x++){
            int rX, rY, gX, gY, bX, bY; 

            int back = x - 1;
            int front = x + 1;
            int top = y - 1;
            int bot = y + 1;
            if (y == 0){
                top = im->height - 1;
            }
            if (y == im->height - 1){
                bot = 0;
            }
            if (x == 0){
                back = im->width - 1;
            }
            if (x == im->width -1){
                front = 0;
            }

            rX = get_pixel(im, y, back, 0) - get_pixel(im, y, front, 0);
            rY = get_pixel(im, top, x, 0) - get_pixel(im, bot, x, 0); 
            gX = get_pixel(im, y, back, 1) - get_pixel(im, y, front, 1);
            gY = get_pixel(im, top, x, 1) - get_pixel(im, bot, x, 1); 
            bX = get_pixel(im, y, back, 2) - get_pixel(im, y, front, 2);
            bY = get_pixel(im, top, x, 2) - get_pixel(im, bot, x, 2); 
 
            int energy = (uint8_t)(sqrt(pow(rX, 2) + pow(rY, 2) + pow(gX, 2)+ pow(gY, 2) + pow(bX, 2) + pow(bY, 2))/10);
            set_pixel(*grad, y, x, energy, energy, energy);
        }
    }
}

double min(double a, double b){
    if (a>b){
        return b;
    }
    return a;
}

void dynamic_seam(struct rgb_img *grad, double **best_arr){
    *best_arr = (double *)malloc((grad->height)*(grad->width)*(sizeof(double)));
    if (grad->width == 1){
        for (int y = 0; y<grad->height; y++){
            (*best_arr)[y*grad->width] = (double) get_pixel(grad, y, 0, 0);
        }
    }
    for (int y = 0; y<grad->height; y++){
        for (int x = 0; x<grad->width; x++){
            if (y == 0){
                (*best_arr)[y*grad->width+x] = (double) get_pixel(grad, y, x, 0);
            }
            else {
                if (x == 0){
                    (*best_arr)[y*grad->width+x] = (double) (get_pixel(grad, y, x, 0)) + (min((*best_arr)[(y-1)*grad->width+x],(*best_arr)[(y-1)*grad->width+x+1])); 
                }
                else if (x == grad->width - 1){
                    (*best_arr)[y*grad->width+x] = (double) (get_pixel(grad, y, x, 0))+ (min((*best_arr)[(y-1)*grad->width+x],(*best_arr)[(y-1)*grad->width+x-1])); 
                }
                else {
                    (*best_arr)[y*grad->width+x] = (double) (get_pixel(grad, y, x, 0)) + (min(min((*best_arr)[(y-1)*grad->width+x],(*best_arr)[(y-1)*grad->width+x-1]), (*best_arr)[(y-1)*grad->width+x+1])); 
                }
            }
        }
    }
}

double minPosition(double a, int positionA, double b, double positionB){
    if (a>b){
        return positionB;
    }
    return positionA;
}

void recover_path(double *best, int height, int width, int **path){
    *path = (int *)malloc(height * sizeof(int));
    int y = height - 1;
    int current = 0;
    if (width == 1){
        if (height == 1){
            (*path)[0] = 0;
            return;
        }
        else{
            for (int i = 0; i<height; i++){
                (*path)[i] = 0;
            }
            return;
        }
    }
    while (y>0){ 
        if (y ==  height - 1){
            for (int x = 0; x<width; x++){
                if (best[y*width+x]<best[y*width+current]){
                    current = x;
                }
            }
            (*path)[y] = current;
        }
        if (height == 1){
            return;
        }
        if (current == 0){
            (*path)[y-1] = minPosition((best)[(y-1)*width+current], current,(best)[(y-1)*width+current + 1], current+1);
            current =  minPosition((best)[(y-1)*width+current], current,(best)[(y-1)*width+current + 1], current+1);
        }
        else if (current == width -1){
            (*path)[y-1] = minPosition((best)[(y-1)*width+current], current,(best)[(y-1)*width+current - 1], current-1);
            current = minPosition((best)[(y-1)*width+current], current,(best)[(y-1)*width+current - 1], current-1);
        }
        else {
            int temp =  minPosition((best)[(y-1)*width+current], current,(best)[(y-1)*width+current - 1], current-1);
            (*path)[y-1] = minPosition((best)[(y-1)*width+current+1], current+1,(best)[(y-1)*width+temp], temp);
            current = minPosition((best)[(y-1)*width+current+1], current+1,(best)[(y-1)*width+temp], temp);
        }
        y-=1;
    }
}

void remove_seam(struct rgb_img* src, struct rgb_img **dest, int* path){
    create_img(dest, src->height, src->width-1);
    for (int y = 0; y<src->height; y++){
        for (int x = 0; x<src->width; x++){
            if (path[y] == x){
                x++;
                if (x == src->width){
                    break;
                }
            }
            if (x>path[y]){
                set_pixel(*dest, y, x-1, get_pixel(src, y,x,0), get_pixel(src, y,x,1),get_pixel(src, y,x,2));
            }
            else {
                set_pixel(*dest, y, x, get_pixel(src, y,x,0), get_pixel(src, y,x,1),get_pixel(src, y,x,2));
            }
        }
    }
}

