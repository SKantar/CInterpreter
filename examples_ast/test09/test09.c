#include <stdio.h>
int a = 2, b = 2;
int b;

int test(int a, int b){
    return a + b;
}

int main(int a, int b){
    int a;
    a = 2 + 3;
    if(a + 2) {
        a = 3 - 1;
    }else{
        b = 1;
    }

    if(a - 5)
        a = 2;
    else
        b = 3;

    return 0;
}
