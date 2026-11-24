// MiniLang: programa invalido (laco for mal formado, sem a clausula de atualizacao)
//
// Resultado esperado: o lexer aceita todos os tokens; o parser rejeita com
//   Erro sintático na linha 7, coluna 19: esperado ';', encontrado ')'
// (a producao "para" exige atribuicao ";" expressao ";" atribuicao)
soma = 0;
for (i = 0; i < 10) {
    soma = soma + i;
}
print(soma);
