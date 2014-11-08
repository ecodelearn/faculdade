
#include <iostream>

int main() {
 int n = 100;
int v1, v2;
cin >> v1;
cin >> v2;
if( ((n*v1)/v2) > 100 && ((n*v2)/v1) < 50) 
 cout << "Valores corretos";
else
 cout << "Valores incorretos";
}
