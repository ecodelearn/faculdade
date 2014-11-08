#include <iostream>
#include <stdio.h>
#include <locale>
#include <stdlib.h>


using namespace std;

int main()
{
    setlocale(LC_ALL, "Portuguese");

    int A;

    for( A = 0; A <= 1000 ; A++ ){
        printf("%d\n", A);
    }

    system ("pause");
    return 0;
}
