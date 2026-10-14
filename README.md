# Sistema de Gestão de Demandas

Aplicação web desenvolvida em Python para cadastrar, consultar e acompanhar demandas internas, com classificação automática de prioridade, indicadores de acompanhamento e exportação de dados para análise no Power BI.

O projeto foi estruturado para separar a interface, a lógica da aplicação, o armazenamento dos dados e a camada de análise, pensando em sua escalabilidade e facilidade de implementar novas funções. Funções básicas de CRUD não foram adicionadas(como o DELETE e UPDATE já que o documento explicitava que não seria necessário quaisquer funcionalidades além do requisitado).


## 1. Tecnologias utilizadas

| Tecnologia | Responsabilidade |
|---|---|
| Python | Linguagem principal e implementação das regras de negócio. |
| Flask | Framework responsável pelas rotas e pela integração entre a lógica e as páginas web. |
| SQLite | Banco de dados relacional utilizado para persistir as demandas. |
| HTML e CSS | Estrutura das páginas e dos formulários + visualização. |
| JavaScript | Interações da interface, incluindo o comportamento do modal. |
| CSV | Formato de exportação dos dados para análise externa. |
| Docker | Conteinerização da aplicação para padronizar sua execução. |
| Docker Compose | Configuração dos serviços, portas, volumes e política de reinicialização. |

## 2. Como a solução foi estruturada

**Interface**: Desenvolvida com HTML e CSS básico a fim de permitir o cadastro e visualização das demandas.

**Backend**: Implementado em Python com Flask, centraliza as rotas, valida os campos obrigatórios, define automaticamente a prioridade e gera o relatório CSV. Além disso, seu ecossistema facilita a integração com ferramentas de análise de dados, como o Power BI, tornando-o adequado tanto para a aplicação quanto para possíveis evoluções.

**Armazenamento de dados** : Escolhi o SQLite por ser um banco de dados relacional leve e que não exige instalação e configuração de um servidor separado. O projeto possui um escopo reduzido e não demanda acesso simultâneo em larga escala, simplificando a implantação e a manutenção, mantendo os dados persistidos em um único arquivo (database.db). Além disso, permite utilizar consultas SQL para gerar os indicadores do dashboard e os dados exportados para o Power BI.

**Desafio opcional**: Inicialmente, gostaria de ter criado uma pequena API que fizesse integração e atualização simultânea com o Power BI, mas devido ao tempo decidi implementar uma solução mais simples que permite a visualização em Excel e Power BI, não deixando de atender aos requisitos do desafio.


## 3. Como a regra de prioridade foi implementada

A prioridade é definida automaticamente por palavras-chave na descrição. A busca ignora diferenças entre maiúsculas e minúsculas e variações de acentuação. Além disso, a expressão regular identifica apenas palavras completas, evitando falsos positivos como “terror”. Se encontrar “urgente” ou “erro”, a prioridade será Alta; caso contrário, será Normal.

## 4. Principais decisões

**Front-end**: Optei por HTML e CSS, priorizando uma estrutura simples, funcional e fácil de manter.

**Back-end**: Escolhi Python por já ter experiência com tratamento de dados e extração de informações utilizando a linguagem. 

**Framework**: Flask, por ser apropriado para desenvolvimento Python. 

**Dados**: SQLite por ser leve, não exigir um servidor de banco de dados separado e atender às necessidades do projeto, simplificando a configuração e a execução da aplicação.

**Desafio opcional**: Implementei a exportação dos dados em CSV, permitindo consulta no Excel e importação no Power BI para análises e criação de relatórios. 

**IA**: Apoio na geração de 20 registros fictícios para popular a tabela e na definição de uma identidade visual básica para a interface, especialmente na escolha de cores.

**Containerização**: Embora não tenha sido requisitado, adicionei o Docker como melhoria extra voltada para a portabilidade e facilidade de execução. 



## 5. (Extra) Ordem do fluxo
O fluxo principal da aplicação segue esta sequência:

1. O usuário acessa a aplicação pelo navegador.
2. O Flask recebe a requisição e executa a rota correspondente.
3. Para cadastrar uma demanda, a aplicação valida e processa os dados recebidos.
4. A demanda é gravada no banco SQLite.
5. Nas consultas, o sistema recupera os registros armazenados e apresenta as informações na interface.
6. Quando solicitado, o sistema consulta os dados e gera um arquivo CSV.
7. O arquivo exportado pode ser utilizado como fonte de dados no Power BI.
