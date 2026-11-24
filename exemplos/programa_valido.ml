// MiniLang: programa valido com while, for e if/else
//
// Saida esperada (uma linha por print):
//   30                      <- y = 2 * (10 + 5)
//   10 9 8 7 6 5 4 3 2 1    <- while, de x = 10 ate x = 1
//   10                      <- soma = 0 + 1 + 2 + 3 + 4; entra no if (10 > 5)
x = 10;
y = 2 * (x + 5);
print(y);

while (x > 0) {
    print(x);
    x = x - 1;
}

soma = 0;
for (i = 0; i < 5; i = i + 1) {
    soma = soma + i;
}

if (soma > 5) {
    print(soma);
} else {
    print(0);
}
