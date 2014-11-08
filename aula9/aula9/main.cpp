#include <iostream>
#include <stdio.h>
#include <locale.h>
#include <stdlib.h>
#include <ctype.h>


using namespace std;

int main()
{
    setlocale(LC_ALL, "Portuguese");

    char caracter;
    printf("Digite um caracter: ");
    scanf("%c", &caracter);

    //caracter=tolower(caracter);

// imprime caracter na tabela ascii converte char pra inteiro

    printf("Caracter: %c - Valor da tabela ascii é: %d\n\n", caracter, caracter);

    printf("Digite o Valor ascii do caracter: ");
    scanf("%d", &caracter);

    printf("Caracter: %c - Valor da tabela ascii é: %d\n", caracter, caracter);

    /*
        if(tolower(caracter)=='b') {
        printf("\n\nDigitou a letra b!\n\n");
    }
    else {
        printf("\n\nDigitou outro caracter!\n\n");

    }

    //printf("\n\nCaracter digitado: -%c-\n\n", caracter);

    */

    /*
    if(caracter=='b' || caracter=='B') {
        printf("\n\nDigitou a letra b!\n\n");
    }
    else {
        printf("\n\nDigitou outro caracter!\n\n");

    } */
    return 0;
}
