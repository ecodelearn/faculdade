#include <stdio.h>
#include <stdlib.h>
#include <locale>
#include <string.h>


using namespace std;

int main()
{

   setlocale(LC_ALL, "Portuguese");

   char nome[10];
   printf("Digite o seu nome: ");
   scanf("%s", &nome);
   setbuf(stdin, NULL);

   printf("\n\nSeu nome é %s\n\n", nome);

   printf("\n\nDigite o seu nome: ");
   gets(nome);

   printf("\n\nSeu nome é %s\n\n", nome);

    return 0;
}
