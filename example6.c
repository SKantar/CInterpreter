#include <stdio.h>

int test(int a)
{
    printf("%d\n",a);
    return a;
}
int test3(int a)
{
    printf("%d\n",a);
    return a;
}
void test1(int b)
{
    printf("%d\n",b);
}

int main()
{
    int bb = 5443;
    test1(55);
    test1(bb);
    return 0;
}
