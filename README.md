# T2 - Simulação e Métodos Analíticos 25/01

Este modelo representa as três filas de atendimento em um determinado cinema: bilheteria, compra de lanches e controle de entrada. Abaixo, descreve-se o funcionamento de cada uma delas:

Bilheteria: Todos os clientes que desejam acessar o cinema iniciam pela bilheteria. Eles chegam em intervalos de 2 a 3 minutos. A bilheteria conta com dois funcionários para o atendimento ao público, e a fila não possui limite de tamanho. Cada atendimento leva entre 2 e 3 minutos. Após a compra dos ingressos: 80% dos clientes se dirigem à compra de lanches, 10% saem do cinema e 10% vão diretamente ao controle de entrada.

Compra de lanches: O quiosque de lanches é atendido por dois funcionários e a fila tem capacidade máxima de 10 pessoas. Cada atendimento leva de 5 a 6 minutos. Após o atendimento: 20% dos clientes voltam à fila para comprar mais produtos, 10% saem do cinema, 20% voltam à bilheteria e 50% seguem para o controle de entrada.

Controle de entrada: A última fila é destinada ao controle de entrada para as salas do cinema.
O atendimento é realizado por um funcionário, a fila comporta até oito pessoas, e cada atendimento leva de 3 a 4 minutos. Após a validação dos ingressos: 90% dos clientes seguem para as salas do cinema e 10% retornam à bilheteria.

📄 [Modelo da Simulação](./docs/simulacao_cinema.pdf)

## Simulação

A simulação para a primeira análise foi definida com a utilização de 100.000 números pseudoaleatórios e semente com valor “123”. O primeiro cliente está agendado para chegar ao cinema no tempo 2,0 minutos. 

### Análise Situação Inicial

Fila: F1
Atendimento: 2 ... 3
---------------------------------------
Estado          Probabilidade
0               4.66%
1               66.46%
2               25.30%
3               3.40%
4               0.18%
5               0.00%
Perdas: 0
Resultado da Fila 1: G/G/1, chegadas entre 2..4, atendimento entre 1..2
   - População média:       1.2798
   - Vazão:                 0.4969
   - Utilização:            0.6211
   - Tempo de resposta:     2.5757
   - Perdas:                0
   - Estados (%):           {0: 4.66, 1: 66.46, 2: 25.3, 3: 3.4, 4: 0.18, 5: 0.0}

Pode-se observar que a primeira fila atende bem ao público, permanecendo mais da metade do tempo com apenas uma pessoa na fila.

Fila: F2
Atendimento: 5 ... 6
---------------------------------------
Estado          Probabilidade
0               0.01%
1               0.01%
2               0.02%
3               0.04%
4               0.11%
5               0.29%
6               0.96%
7               3.46%
8               14.91%
9               39.09%
10              41.10%
Perdas: 4198
Resultado da Fila 2: G/G/2/5, atendimento entre 4..8
   - População média:       9.1407
   - Vazão:                 0.3636
   - Utilização:            0.9998
   - Tempo de resposta:     25.1411
   - Perdas:                4198
   - Estados (%):           {0: 0.01, 1: 0.01, 2: 0.02, 3: 0.04, 4: 0.11, 5: 0.29, 6: 0.96, 7: 3.46, 8: 14.91, 9: 39.09, 10: 41.1} 

Na análise da segunda fila, observa-se uma situação bem diferente da fila anterior. Ela está significativamente sobrecarregada, com a perda de 4.198 clientes. Como uma parte importante da receita do cinema está associada à venda de lanches, é essencial analisar soluções para esse gargalo. Além disso, nota-se que em 80% do tempo a fila está cheia, com 9 ou 10 clientes.

Fila: F3
Atendimento: 3 ... 4
---------------------------------------
Estado          Probabilidade
0               19.49%
1               34.71%
2               24.78%
3               11.97%
4               5.50%
5               2.06%
6               0.89%
7               0.50%
8               0.11%
Perdas: 7
Resultado da Fila 3: G/G/2/10, atendimento entre 5..15
   - População média:       1.6217
   - Vazão:                 0.2300
   - Utilização:            0.8051
   - Tempo de resposta:     7.0497
   - Utilização:            0.8051
   - Tempo de resposta:     7.0497
   - Utilização:            0.8051
   - Tempo de resposta:     7.0497
   - Perdas:                7
   - Estados (%):           {0: 19.49, 1: 34.71, 2: 24.78, 3: 11.97, 4: 5.5, 5: 2.06, 6: 0.89, 7: 0.5, 8: 0.11}

A fila 3 apresenta um número muito menor de perdas, e a quantidade de clientes na fila possui uma boa distribuição ao longo do tempo.

Tempo Total: 38677.40463613602

O tempo total de simulação foi de 38.677 minutos, aproximadamente 645 horas (cerca de 27 dias).

### Análise Proposta 1

Na primeira simulação, observamos que o principal gargalo no atendimento ao cliente está na lanchonete. Para esta nova simulação, foi adicionado mais um atendente nesse setor, com o objetivo de observar como esse ajuste afeta o desempenho do sistema.

Fila: F1
Atendimento: 2 ... 3
---------------------------------------
Estado          Probabilidade
0               4.04%
1               58.42%
2               30.32%
3               6.41%
4               0.75%
5               0.05%
6               0.00%
Perdas: 0
Resultado da Fila 1: G/G/1, chegadas entre 2..4, atendimento entre 1..2
   - População média:       1.4157
   - Vazão:                 0.5340
   - Utilização:            0.6675
   - Tempo de resposta:     2.6513
   - Perdas:                0
   - Estados (%):           {0: 4.04, 1: 58.42, 2: 30.32, 3: 6.41, 4: 0.75, 5: 0.05, 6: 0.0}


A primeira fila permaneceu inalterada e continua operando de forma eficiente, sem perdas.

Fila: F2
Atendimento: 5 ... 6
---------------------------------------
Estado          Probabilidade
0               0.28%
1               2.59%
2               8.31%
3               13.93%
4               14.65%
5               13.49%
6               12.44%
7               11.16%
8               10.79%
9               8.17%
10              4.17%
Perdas: 340
Resultado da Fila 2: G/G/2/5, atendimento entre 4..8
   - População média:       5.4145
   - Vazão:                 0.5194
   - Utilização:            0.9522
   - Tempo de resposta:     10.4250
   - Perdas:                340
   - Estados (%):           {0: 0.28, 1: 2.59, 2: 8.31, 3: 13.93, 4: 14.65, 5: 13.49, 6: 12.44, 7: 11.16, 8: 10.79, 9: 8.17, 10: 4.17}

Com a adição de um atendente, a fila 2 apresentou uma redução significativa de perdas: 3.858 clientes a menos, representando uma melhoria de aproximadamente 91%.
Apesar de ainda registrar 340 perdas, a situação é muito mais equilibrada, com cerca de 66% do tempo a fila variando entre 3 e 7 pessoas — uma distribuição muito mais saudável em comparação à simulação anterior.

Fila: F3
Atendimento: 3 ... 4
---------------------------------------
Estado          Probabilidade
0               0.63%
1               1.63%
2               2.91%
3               5.36%
4               9.76%
5               15.01%
6               20.74%
7               28.52%
8               15.44%
Perdas: 1118
Resultado da Fila 3: G/G/2/10, atendimento entre 5..15
   - População média:       5.8523
   - Vazão:                 0.2839
   - Utilização:            0.9937
   - Tempo de resposta:     20.6122
   - Perdas:                1118
   - Estados (%):           {0: 0.63, 1: 1.63, 2: 2.91, 3: 5.36, 4: 9.76, 5: 15.01, 6: 20.74, 7: 28.52, 8: 15.44}

Tempo Total: 32469.65986913765


A fila 3, que anteriormente apresentava apenas 7 perdas, sofreu um aumento expressivo, agora totalizando 1.118 perdas — um crescimento de mais de 160 vezes. Esse agravamento se deve, provavelmente, ao aumento da demanda gerado pela melhoria na fila 2. O único atendente na fila 3 não consegue mais absorver o fluxo resultante. 

Para a próxima proposta, será necessário considerar a adição de mais um funcionário na fila 3, a fim de reduzir a nova sobrecarga observada. É importante destacar que, se os clientes desistirem de assistir ao filme devido ao tempo de espera, há uma grande chance de que não retornem ao cinema futuramente, o que representa uma perda significativa de receita recorrente para o negócio.

Além disso, mesmo com a melhoria apresentada na fila 2, ainda se observa um número considerável de perdas. Portanto, recomenda-se também a adição de um segundo funcionário extra na fila 2, visando minimizar ainda mais esse impacto e garantir maior eficiência no atendimento.


### Análise Proposta 2

Fila: F1
Atendimento: 2 ... 3
---------------------------------------
Estado          Probabilidade
0               3.78%
1               56.43%
2               31.31%
3               7.44%
4               1.00%
5               0.05%
Perdas: 0
Resultado da Fila 1: G/G/1, chegadas entre 2..4, atendimento entre 1..2
   - População média:       1.4558
   - Vazão:                 0.5440
   - Utilização:            0.6801
   - Tempo de resposta:     2.6760
   - Perdas:                0
   - Estados (%):           {0: 3.78, 1: 56.43, 2: 31.31, 3: 7.44, 4: 1.0, 5: 0.05}

A primeira fila permaneceu inalterada e continua operando de forma eficiente, sem perdas.

Fila: F2
Atendimento: 5 ... 6
---------------------------------------
Estado          Probabilidade
0               0.92%
1               7.22%
2               22.27%
3               30.35%
4               21.68%
5               10.53%
6               4.23%
7               1.79%
8               0.67%
9               0.26%
10              0.07%
Perdas: 8
Resultado da Fila 2: G/G/2/5, atendimento entre 4..8
   - População média:       3.2857
   - Vazão:                 0.5450
   - Utilização:            0.7494
   - Tempo de resposta:     6.0284
   - Perdas:                8
   - Estados (%):           {0: 0.92, 1: 7.22, 2: 22.27, 3: 30.35, 4: 21.68, 5: 10.53, 6: 4.23, 7: 1.79, 8: 0.67, 9: 0.26, 10: 0.07}

Com a adição de mais dois atendentes ao longo das simulações, a fila 2 teve uma queda expressiva nas perdas, saindo de 4.198 para apenas 8 clientes perdidos. A distribuição de atendimento também se estabilizou, com a maior parte do tempo concentrada entre 2 a 4 pessoas na fila, indicando um fluxo bem gerenciado.

Fila: F3
Atendimento: 3 ... 4
---------------------------------------
Estado          Probabilidade
0               22.97%
1               39.50%
2               26.46%
3               9.13%
4               1.73%
5               0.20%
6               0.01%
Perdas: 0
Resultado da Fila 3: G/G/2/10, atendimento entre 5..15
   - População média:       1.2781
   - Vazão:                 0.3273
   - Utilização:            0.5729
   - Tempo de resposta:     3.9045
   - Perdas:                0
   - Estados (%):           {0: 22.97, 1: 39.5, 2: 26.46, 3: 9.13, 4: 1.73, 5: 0.2, 6: 0.01}

Tempo total de simulação: 30893.04

A fila 3, que havia se tornado o novo gargalo após a melhoria da fila 2, foi ajustada com a adição de um segundo atendente, resultando em eliminação total das perdas. A distribuição do atendimento também indica um excelente desempenho, com cerca de 89% do tempo operando com no máximo dois clientes na fila.
