#include <stdio.h>

int reverse(int broj){
    int zbir = 0;
    while(broj>0){
        int k = broj%10;
        broj/=10;
        zbir = zbir*10+k;
    }
    return zbir;
}

int pom(int broj){
    broj/=10;
    broj = reverse(broj);
    broj/=10;
    return reverse(broj);
}
int main(){
    int n = 10;
    int zbir = 0;
    while(n != 0){
        scanf("%d", &n);
        zbir += pom(n);
    }
    printf("%d\n", zbir);
    return 0;
}
