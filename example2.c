#include <stdio.h>

int main(){
    char d;
    char a, b, c;

    while((d = getchar()) != '\n'){
        if(d >= '0' && d <= '9'){
            a = b;
            b = c;
            c = d;
        }
    }
    printf("%c%c%c\n", a, b, c);
    return 0;
}
