#include <stdio.h>

int main(){
    int i = 2;
    printf("%d\n", i++);
    printf("%d\n", ++i);
    printf("%d\n", !i);
    printf("%d\n", !(!i));
    printf("%d\n", (int)2.1);
    printf("%d", 2 != 2);

    return 0;
}