#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct student {
    char name[100];
    int age;
    }student;

// Q5
void change_int(int* p_a, int new_val) {
    *p_a = new_val;
}

// Q10
void change_p_int(int** p_p_a) {
    **p_p_a = 46;
}

// Q11
void make_new_p_int(int** p_p_a) {
    *p_p_a = (int*)malloc(sizeof(int));
}

// Q16
void change_arr(int* arr) {
    arr[2] = 8;
}

// Q27
void change_stud_name(student* p_s) {
    strcpy(p_s->name, "Jimmy");
}

// Q28
void change_stud_age(student* p_s) {
    p_s->age = 29;
}

// Q34
void make_new_p_student(student** p_p_s) {
    *p_p_s = (student*)malloc(sizeof(student));
}

// Q40
void change_stud_name_arr(student **p_arr) {
    strcpy((*p_arr + 2)->name, "Jill");
}

// Q43
void change_stud_name_arr2(student* arr) {
    strcpy((arr + 2)->name, "Jeremy");
}

void print_arr(int* arr, int size) {
    printf("{");
    for(int i = 0; i < size - 1; i++) {
        printf("%d, ", arr[i]);
    }
    printf("%d}", arr[size - 1]);
}

void print_student(student s) {
    printf("a %d-year-old student named %s", s.age, s.name);
}
// Pointer drills
int main(void) {
    // 1. Define an integer variable a and initialize it to 42
    int a = 42;
    printf("Q1: a is now %d\n\n", a);
    //2. Define a pointer to an integer variable and initialize it to the address of a
    int* p_a = &a;
    printf("Q2: &a is %p, p_a is %p\na is %d, *p_a is %d\n\n", &a, p_a, a, *p_a);

    //3. Using p_a and without directly using a, change the value of a to 43
    *p_a = 43;
    printf("Q3: a is now %d\n\n", a);
    //4. Change the value of the pointer p_a to something else. Make sure that
    // the value of a does not change

    int b = 3;
    p_a = &b;
    printf("Q4: &a is %p, p_a is %p\na is %d, *p_a is %d\n\n", &a, p_a, a, *p_a);

    //5. Define a function that takes in a pointer to an integer and changes the integer


    //6. Call the function from 5 and pass in the address of a. Make sure that the value of a changes
    change_int(&a, 13);
    printf("Q6: a is now %d\n\n", a);

    //7. Call the function named change_int without directly using a, but using p_a instead
    //p_a = &a; // said this before
    p_a = &a;
    change_int(p_a, 15);
    printf("Q7: a is now %d\n\n", a);

    //8. Define a variable that would store the address of p_a. 
    int** p_p_a;

    //9. make p_p_a point to p_a
    p_p_a = &p_a;
    printf("Q9: &p_a is %p, p_p_a is %p\n*p_a is %d, **p_a is %d\n\n", &p_a, p_p_a, *p_a, **p_p_a);

    // 10. Write a function that takes in a pointer to a pointer to an integer and changes the value of the 
    // integer to 46

    // 11. Write a function that takes in a pointer to a pointer to an integer and changes the value of the 
    // pointer to a new address where an integer can be stored. (You will need to use malloc)

    // 12. Call the function from (10) in order to change the value of a to 46. Do this using p_p_a, and using p_a
    change_p_int(p_p_a);
    printf("Q12: a is now %d\n", a);
    a = 0;
    printf("Resetting. a is now %d\n", a);
    change_p_int(&p_a);
    printf("a is now %d\n\n", a);

    // 13. Call the function from (11) in order to change the value of p_a to point to a new address. Don't use p_p_a
    printf("Q13: p_a was %p, ", p_a);
    make_new_p_int(&p_a);
    printf("But p_a is now %p\n\n", p_a);
    free(p_a);

    // 14. Call the function from (11) in order to change the value of p_p_a to point to a new address. Use p_p_a
    printf("Q14: p_a was %p, ", p_a);
    make_new_p_int(p_p_a);
    printf("But p_a is now %p\n\n", p_a);
    free(p_a);

    // 15. Declare an array of integers and initialize it to {5, 6, 7}
    int int_arr[3] = { 5, 6, 7 };

    // 16. Write a function that takes in a pointer to the first element of an array of integers and modifies the 
    //     element at index 2 to 8

    // 17. Call the function from (16) in order to change the value of the array from (15)
    printf("Q17: int_arr was "); print_arr(int_arr, 3);
    change_arr(int_arr);
    printf(" but it is now "); print_arr(int_arr, 3); printf("\n\n");

    // 18. Create a malloc-allocated block of memory that can store 3 integers. Store it in the variable
    //     p_block. Then use change_arr to change the value at index 2
    int* p_block = (int*)malloc(3 * sizeof(int));
    change_arr(p_block);

    // 19. Use change_int from (7) to change the value of the integer stored in the block of memory from (18)
    change_int(p_block, 3);
    change_int(p_block + 1, 6);
    printf("Q19: p_block is now "); print_arr(p_block, 3); printf("\n\n");
    free(p_block);

    // 20. Use change_int_ptr from (13) to change the value of p_block to point to a new address
    printf("Q20: p_block was %p", p_block);
    make_new_p_int(&p_block);
    printf(" but is now %p\n\n", p_block);
    free(p_block);
    

    // 21. Create a an object of type student and initialize it
    // typedef struct student{
    //    char name[1000];
    //    int age;
    //};
    student s1 = { "Jerry", 15 };

    // 22. Change the name of the student to "Jennifer"
    printf("Q22: s1 was "); print_student(s1);
    strcpy(s1.name, "Jennifer");
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 23. Change the age of the student to 21
    printf("Q23: s1 was "); print_student(s1);
    s1.age = 21;
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 24. Create a pointer p_s to the student and initialize it to the address of the student
    student* p_s1 = &s1;

    // 25. Change the name of the student to "Jenny", using p_s
    printf("Q25: s1 was "); print_student(s1);
    strcpy(p_s1->name, "Jenny");
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 26. Change the age of the student to 20, using p_s
    printf("Q26: s1 was "); print_student(s1);
    p_s1->age = 20;
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 27. Create a function that takes in a pointer to a student and changes the name to "Jenny"

    // 28. Create a function that takes in a pointer to a student and changes the age to 20

    // 29. Call the function from (27) in order to change the name of the student to "Jenny". Use s not p_s
    printf("Q29: s1 was "); print_student(s1);
    change_stud_name(p_s1);
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 30. Call the function from (28) in order to change the age of the student to 20. Use s not p_s
    printf("Q30: s1 was "); print_student(s1);
    change_stud_age(&s1);
    printf(" but is now "); print_student(s1); printf("\n\n");

    // 31. Create an array of 5 student objects
    student stud_arr[5];
    // 32. User the functions from change_name and change_age on the element at index 2 of the array
    change_stud_name(stud_arr + 2);
    change_stud_age(stud_arr + 2);
    printf("Q32: stud_arr[2] is "); print_student(stud_arr[2]); printf("\n\n");

    // 33. Create a malloc-allocated block of memory that can store 5 students. Store it in the variable p_block_s
    student* p_block_s = (student*)malloc(5 * sizeof(student));
    // 34. Make a function that takes in a pointer to an address of student, and sets that pointer
    //     to point to a new address where a student can be stored

    // 35. Call the function from (34) in order to change the value of p_block_s to point to a new address
    free(p_block_s);
    printf("Q35: p_block_s was %p", p_block_s);
    make_new_p_student(&p_block_s);
    printf(" but is now %p\n\n", p_block_s);
    free(p_block_s);

    // 36. Call the function from (27) in order to change the name of the student at index 2
    //     of the block of memory from (33). Use p_block_s
    p_block_s = (student*)malloc(5 * sizeof(student));
    change_stud_name(p_block_s + 2);
    p_block_s[2].age = 13;
    printf("Q36: p_block_s[2] is now "); print_student(p_block_s[2]); printf("\n\n");

    // 37. Create a variable p_p_s to store the address of p_block_s
    student** p_p_s = &p_block_s;

    // 38. Without calling any function except strcpy, and using only p_p_s, change the name of the 
    //     student at index 2 to "Jennifer"
    strcpy((*p_p_s)[2].name, "Jennifer");
    printf("Q37: p_block_s[2] is now "); print_student(p_block_s[2]); printf("\n\n");

    // 39. In the name of the second student in the block p_p_s, change the first letter to 'j'
    //     Propose four valid to do that with one line that don't involve calling a function
    strcpy((*p_p_s)[1].name, "hoy");
    (*p_p_s)[1].age = 17;

    p_block_s[1].name[0] = 'j';
    (*p_p_s)[1].name[0] = 'j';
    (p_block_s + 1)->name[0] = 'j';
    (*p_p_s + 1)->name[0] = 'j';

    //(*(p_p_s[1])).name[0] = 'j';
    //or

    (*p_p_s + 1)->name[0] = 'j';
    //or

    (* (*p_p_s + 1)).name[0] = 'j';

    //(p_p_s[1])->name[0] = 'j';
    printf("Q38: p_block_s[1] is now "); print_student(p_block_s[1]); printf("\n\n");

    // 40. Write a function that takes in a pointer to a the first addres address the addresses of
    //     students in a block, and changes the name of the student at index 2 to "Jenny"


    // 41. Call the function from (40) in order to change the name of the student at index 2.
    // User p_block_s
    
    change_stud_name_arr(&p_block_s);
    printf("Q41: p_block_s[2] is now "); print_student(p_block_s[2]); printf("\n\n");

    // 42. Call the function from (40) in order to change the name of the student at index 2.
    //     Use p_p_s
    strcpy(p_block_s[2].name, "hello");
    printf("Q42: Resetting. p_block_s[2] was "); print_student(p_block_s[2]);
    change_stud_name_arr(p_p_s);
    printf(" but is now "); print_student(p_block_s[2]); printf("\n\n");

    // 43. Write a function that takes in the first address of a student in a block of addresses
    //     of students, and changes the name of the student at index 2 to "Jenny"
    

    // 44. Call the function from (43) in order to change the name of the student at index 2.
    // User p_block_s
    change_stud_name_arr2(p_block_s);
    printf("Q41: p_block_s[2] is now "); print_student(p_block_s[2]); printf("\n\n");

    // 45. Call the function from (43) in order to change the name of the student at index 2.
    //     Use p_p_s
    strcpy(p_block_s[2].name, "hello");
    printf("Q42: Resetting. p_block_s[2] was "); print_student(p_block_s[2]);
    change_stud_name_arr2(*p_p_s);
    printf(" but is now "); print_student(p_block_s[2]); printf("\n\n");
    //free(p_a);
    free(p_block_s);
}