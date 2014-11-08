#include <iostream>
#include <stdio.h>
#include <locale>
#include <cstdlib>

using namespace std;

int main()
{

    setlocale(LC_ALL, "Portuguese");

    int i, numero;

    for ( i = 1 ; i <= 1000 ; i++ ) {

    numero=(i%2);

    if (numero==0) {

    cout << i <<" ";

        }
    }
    system("pause");
    return 0;

}
