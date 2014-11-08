#include <iostream>
#include <locale>
#include <cstdlib>

using namespace std;

int main()
{
setlocale(LC_ALL, "Portuguese");

int tipoAutomovel, fimPlaca;

cout << "Digite o Tipo de Automóvel ( 1 - p/ carro e moto ) - ( 2 - p/ Caminhão ): \n\n";
cin >> tipoAutomovel;
cout << "Digite o número final da sua placa: \n\n";
cin >> fimPlaca;

if (tipoAutomovel == 1){
    switch(fimPlaca){
    case 1: cout << "\nAbril\n\n";
    break;
    case 2: cout << "\nMaio\n\n";
    break;
    case 3: cout << "\nJunho\n\n";
    break;
    case 4: cout << "\nJulho\n\n";
    break;
    case 5:;
    case 6: cout << "\nAgosto\n\n";
    case 7: cout << "\nSetembro\n\n";
    break;
    case 8: cout << "\nOutubro\n\n";
    break;
    case 9: cout << "\nNovembro\n\n";
    break;
    case 0: cout << "\nDezembro\n\n";
    break;
    }
}

else{
    switch(fimPlaca){
    case 1:;
    case 2: cout << "\nSetembro\n\n";
    break;
    case 3:;
    case 4:;
    case 5: cout << "\nOutubro\n\n";
    break;
    case 6:;
    case 7:;
    case 8: cout << "\nNovembro\n\n";
    break;
    case 9:;
    case 0: cout << "\nDezembro\n\n";
    break;
    }

}
cout << "\n\n";
    return 0;
}
