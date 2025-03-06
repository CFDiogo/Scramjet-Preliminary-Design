# README - Dimensionamento Preliminar de Scramjet

## Descrição
Este código realiza o dimensionamento preliminar de um motor scramjet, considerando as etapas de compressão, reflexão, combustão e exaustão. Ele solicita parâmetros ao usuário e executa cálculos baseados em métodos aerodinâmicos e termodinâmicos para determinar propriedades do fluxo ao longo das diferentes seções do motor.

## Estrutura do Código
O código é dividido nas seguintes etapas principais:

1. **Entrada de Dados**:
   - Número de rampas de compressão
   - Ângulos de cada rampa

2. **Compressão**:
   - Cálculo dos ângulos beta usando o método de Newton-Raphson
   - Determinação das propriedades termodinâmicas após cada rampa

3. **Reflexão**:
   - Determinação da reflexão do fluxo considerando o ângulo total das rampas
   - Cálculo das propriedades do fluxo refletido

4. **Combustão**:
   - Cálculo da adição de calor pela teoria de Rayleigh
   - Determinação do calor necessário para atingir a condição desejada de Mach

5. **Exaustão**:
   - Determinação do Mach e ângulo de Prandtl-Meyer na saída
   - Cálculo do comprimento da câmara de exaustão

## Dependências
O código utiliza as seguintes bibliotecas:
- `pandas` para manipulação de dados
- `math` para operações matemáticas
- `matplotlib.pyplot` para visualização (se necessário)
- `functions.py` (arquivo externo com funções auxiliares)
- `variables.py` (arquivo externo contendo variáveis e constantes do problema)

## Como Executar
1. Certifique-se de que os arquivos `functions.py` e `variables.py` estão na mesma pasta que o script principal.
2. Execute o código em um ambiente Python compatível.
3. Insira os valores solicitados pelo terminal.
4. O resultado será salvo no arquivo `output.txt`, contendo as propriedades calculadas em cada etapa do processo.

## Saída do Programa
O código gera um arquivo `output.txt` contendo os dados de:
- Propriedades termodinâmicas na compressão e reflexão
- Cálculos de combustão
- Propriedades do escoamento na exaustão

## Possíveis Melhorias
- Implementar interface gráfica para facilitar a entrada de dados
- Permitir leitura de parâmetros a partir de um arquivo de entrada

## Autor
Código desenvolvido por **Felipe Diogo Moura Silva**.

