                #include <stdio.h>

                int reverse(int broj){
                    int zbir = 0;
                    while(broj > 0){
                        printf("%d\n", broj);
                        int k = broj%10;
                        printf(" k => %d\n", k);
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
                    int n;
                    int broj = 123;
                    broj = pom(broj);
                    printf("%d", broj);
                    return 0;
                }