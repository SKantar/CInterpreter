#include <stdio.h>

int min(int a, int b){
    return a < b ? a : b;
}

int main(){
    int n, i, j;
    double z = 3;
    scanf("%d", &n);
    int k = n / 2 + 1, t = 1;
    char c = 'A';
    for(i = 0; i < n; i ++){
        for(j = 0; j < n; j++){
            if(t == 1){
                if(j >= n - k || (j == 0 && k == 1)){
                    printf(".");
                }else{
                    printf("%c", c);
                }
            }else{
                if(j < k){
                    printf(".");
                }else{
                    printf("%c", c);
                }

            }
        }

        if(t == 1)
            k--;
        else
            k++;


        if(k == 0){
            t = 0;
            k = 2;
        }

        c += 1;
        printf("\n");
    }
    return 0;
}
