#include <iostream>
#include <cstdio>
#include <locale>
#include <cstdlib>

using namespace std;

int main()
{
setlocale(LC_ALL, "Portuguese");

int mes;

cout << "\nDigite o n�mero (de 1 a 12) correspondente ao m�s desejado: ";
cin >> mes;

switch(mes)
{
    case 1: cout << "\nJaneiro\n\n";
        break;
    case 2: cout << "\nFevereiro\n\n";
        break;
    case 3: cout << "\nMar�o\n\n";
        break;
    case 4: cout << "\nAbril\n\n";
        break;
    case 5: cout << "\nMaio\n\n";
        break;
    case 6: cout << "\nJunho\n\n";
        break;
    case 7: cout << "\nJulho\n\n";
        break;
    case 8: cout << "\nAgosto\n\n";
        break;
    case 9: cout << "\nSetembro\n\n";
        break;
    case 10: cout << "\nOutubro\n\n";
        break;
    case 11: cout << "\nNovembro\n\n";
        break;
    case 12: cout << "\nDezembro\n\n";
        break;
    default: cout << "\nN�mero inv�lido!\n\n";

cout << "\n\n";
}


    system("pause");
    return 0;
}
