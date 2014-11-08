#include <iostream>
#include <stdio.h>
#include <locale.h>
#include <stdlib.h>

using namespace std;

int main()
{
    setlocale(LC_ALL, "Portuguese");

    int Valor;

    do{
        printf ("Digite um valor ou -1 para sair! :" );
        scanf("%d", &Valor);
    }while(Valor != -1);

    return 0;
}
