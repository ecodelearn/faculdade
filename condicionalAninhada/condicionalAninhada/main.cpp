#include <iostream>
#include <cstdio>
#include <locale>

using namespace std;

int main()
{

setlocale(LC_ALL, "Portuguese");

int num1, num2, num3;
cout << "\nN�mero 1 :";
cin >> num1;
cout << "\nN�mero 2 :";
cin >> num2;
cout << "\nN�mero 3 :";
cin >> num3;
cout << "\n\n";

if (num1 > num2)
{
    if (num1 > num3)
    {
        if (num2 > num3)

            cout << num3 << " - " << num2 << " - " << num1;
        else
            cout << num2 << " - " << num3 << " - " << num1;
    }
    else
    {
        cout << num2 << " - " << num1 << " - " << num3;
    }
}
else
{
    if (num2 > num3)
    {
        if (num1 > num3)
            cout << num3 << " - " << num1 << " - " << num2;
        else
            cout << num1 << " - " << num3 << " - " << num2;
    }
    else
    {
        cout << num1 << " - " << num2 << " - " << num3;
    }
}
cout << "\n";
    return 0;
}
