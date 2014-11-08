#include <cstdlib>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{

 int x,y;
 
 cout << "\n Teste para saber se o paralelograma eh um retangulo ou um quadrado\n\n\n"; 
 cout << "\n Entre com a altura: ", cin >> x;
 cout << "\n Entre com a largura: ", cin >> y;
 
 if (x == y)
    cout << "\n\n\n\t O paralelogramo eh um quadrado!\n\n\n";
 else
    cout << "\n\n\n\t O paralelogramo eh um retangulo!\n\n\n";

    system("PAUSE");
    return EXIT_SUCCESS;
}
