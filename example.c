#include <stdio.h>
#include <math.h>
int test(int a){
    printf("%d\n", a);
    return a;
}
int b = 1 + 2;

int main(){
   int a = 2;
   int c = a + 3 - 1;
   scanf("%d %d", &a, &b);
   if(5 + 3 > 6){
        c = 1;
        c = c + 1;
   }
   else
   {
        c = -2;
   }
   int i = 0;

   while(i < 10){
      printf("%d\n", i);
      i = i + 1;
   }

   printf("%.2f", sqrt(9));
   return 0;
}