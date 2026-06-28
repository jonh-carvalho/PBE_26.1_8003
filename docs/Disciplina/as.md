---
id: as
title: Avaliação Substitutiva(AS)
---

## **Desenvolvimento de API REST com Django + Metodologia RUP/UP**

### **Tema:** "FitLife — Plataforma de Treinos e Bem-Estar"

**Duração Estimada:** (3h 40min)

**Resumo:** A funcionalidade 'Registro de Treino Completo e Progresso' permite que usuários da plataforma FitLife registrem os detalhes de um treino realizado, associando-o a uma *Playlist* específica e detalhando cada exercício efetuado. O sistema deve calcular métricas de progresso baseadas na recorrência e intensidade dos treinos registrados.

**Objetivo:** Permitir o acompanhamento contínuo da jornada fitness do usuário (engajamento) e fornecer dados estruturados para que ele visualize sua evolução (progresso). A funcionalidade visa aumentar a retenção ao manter o usuário motivado com *insights* de melhoria.

**Jornadas do Usuário:**

1.  Criar um novo registro de treino após a execução (Registro Pontual).
2.  Visualizar o histórico consolidado de treinos e identificar progressões/regressões.

**Regras de Negócio:**

1.  **Associação Obrigatória:** Todo treino deve estar associado a um Usuário autenticado e a uma Playlist existente.
2.  **Cálculo de Volume:** O sistema deve calcular o volume total por exercício no registro: $Volume = Repetição \times Carga$.
3.  **Progressão Mínima:** Para que a visualização de progresso funcione, um treino deve conter pelo menos 1 série completa registrada.
4.  **Limitação de Edição:** Treinos podem ser editados até 24 horas após o registro inicial para correção de dados (caso contrário, são considerados "finalizados").
---


# **Fases de Desenvolvimento e Entrega**

## **0. Configuração Inicial (30 minutos)**
**(Objetivo: Estabelecer o alicerce técnico, metodológico e documental.)**

### **Atividades Mandatórias:**
*   Clonar o repositório inicial fornecido pelo avaliador ([repositório start](https://github.com/jonh-carvalho/PBE_26.1_8003_AS)).
        *(Lembrete: Confirmar permissão de colaborador via convite).*

*   Configurar ambiente local: 
    * Python + Virtualenv 
    * Instalação das dependências do projeto.

*   Criar **Site de Documentação (MkDocs):**
    
    * Iniciar o repositório com 'mkdocs new .'
    * Estrutura inicial descrevendo o escopo geral do projeto no README/Homepage.
    * Publicar a documentação básica no GitHub Pages (`mkdocs gh-deploy`).

*   Configurar **GitHub Project (Kanban) e Workflow:**
    * Colunas sugeridas: `Backlog` $\rightarrow$ `Análise/Modelagem` $\rightarrow$ `Em desenvolvimento` $\rightarrow$ `Testando` $\rightarrow$ `Concluído`.
    * **Workflow Rigoroso:** Criar **Issues** para cada componente principal (Modelo, Serializer, View, Endpoint API, Documentação). Cada Issue deve ser imediatamente associada a um *card* no GitHub Project, definindo prioridade e fluxo esperado.

### **Entregáveis Mínimos:**
1.  Repositório Git com estrutura de projeto inicializada.
2.  Site MkDocs publicado no GitHub Pages (Página Home).
3.  GitHub Project configurado e *todos* os itens do escopo mapeados em Issues ativas.


---

## **1. Concepção: Levantamento de Requisitos e Escopo (30 minutos)**
**(Objetivo: Formalizar o entendimento do problema e mapear as fronteiras do sistema.)**

### **Atividades:**
* **Descrição Funcional:** Documentação detalhada no MkDocs, abordando "Quem?", "O quê?" e "Porquê?".
* **Requisitos:** Levantamento completo de Requisitos Funcionais (RF) e Não Funcionais (RNF). Os RNF devem cobrir segurança, performance básica e usabilidade.
* **Atores e Casos de Uso:** Identificação dos Atores Principais (Usuário, Sistema). Descrição textual robusta de 3 casos de uso críticos.
    *(Opcional: Diagrama UML de Caso de Uso como reforço).*

### **Entregáveis Obrigatórios:**
*  Documentos MkDocs atualizados com RF, RNF e Casos de Uso formalizados: 
    * `docs/_Iniciação/5w2h.md`
    * `docs/_Iniciação/Documento_de_visao.md`)


---

## **2. Elaboração: Projeto Arquitetural e Modelagem (50 minutos)**
**(Objetivo: Criar o *contrato* técnico que guiará a construção, minimizando ambiguidades.)**

### **Atividades:**
*   **Modelagem de Dados:** Criação do Diagrama de Classes (PlantUML), definindo entidades principais e seus relacionamentos obrigatórios.
    *   *(Relacionamentos chave: Usuário $\leftrightarrow$ Playlist $\leftrightarrow$ Treino $\leftrightarrow$ Exercícios).*
*   **APIs Contracts:** Definição clara, em formato OpenAPI/Swagger conceitual, de todos os *endpoints necessários* (verbos HTTP e parâmetros esperados).
*   **Arquitetura no Código:** Documentar o *raciocínio arquitetural* no MkDocs. Como Django/DRF será estruturado? Qual o fluxo de middleware?

### **Entregáveis Obrigatórios:**
1.  Documento MkDocs (`docs/__Elaboração/index.md`) contendo a visão geral da arquitetura.
2.  Diagrama de Classes (via `diagrama_de_classes.md`).
3.  **Artefato de Aprovação:** O conjunto de endpoints e o Diagrama de Classes devem ser revisados e aceitos (simbolicamente, pelo avaliador) como base para a construção.


---

## **3. Construção: Implementação Técnica da API (1 hora e 40 minutos)**

**(Objetivo: Transformar o plano em um sistema funcional, seguindo boas práticas de engenharia de software.)**

### **Atividades:**

* **Implementação Estruturada:** Desenvolvimento iterativo (preferencialmente focado em funcionalidades atômicas).
* **Modelagem e Migrações** (`models` $\rightarrow$ `serializers`).
* **Lógica de Negócios** (`views`) 
* **Rotas API** configuradas com Swagger/Redoc automática.
* **Qualidade do Código:** CRUD básico
* **Controle de Versão:** Manter commits atômicos e referenciar os Issues correlatos em cada commit significativo (`git commit -m "feat: Implementa [issue-XXX] - Criação do Model X"`).

### **Entregáveis Obrigatórios:**
1.  Código funcional no repositório Git.
2.  Endpoints testados localmente, demonstrando fluxo de dados correto (Happy Path).
3.  Documentação Swagger gerada e validada contra os endpoints implementados.


---

## **4. Transição: Refinamento e Entrega Final (10 minutos)**
**(Objetivo: Simular o processo de QA/UAT e preparar a apresentação final.)**

### **Atividades:**

*   **Finalização da Documentação (MkDocs):** Criar um guia de uso conciso, focado no consumidor da API (Ex: "Como integrar o endpoint X?").
*   **Entrega Final:** Preparar uma **Demonstração Viva (Walkthrough)** do sistema, apresentando os 3-5 fluxos mais importantes e explicando como foram resolvidos os problemas encontrados durante os testes.

### **Entregáveis Obrigatórios:**
1.  Site MkDocs atualizado com o Guia de Uso da API.
2.  Código no GitHub demonstrando a robustez das funcionalidades e histórico de commits seguindo as Issues.


---

## **Modelo de Checklist Geral de Entrega**

| Item                              | Obrigatório | Entregue |
| --------------------------------- | ----------- | -------- |
| Ambiente de desenvolvimento OK    | ✔️          | ⬜        |
| Clone do repositório inicial      | ✔️          | ⬜        |
| GitHub Project configurado        | ✔️          | ⬜        |
| Issues criadas e usadas           | ✔️          | ⬜        |
| Site MkDocs publicado             | ✔️          | ⬜        |
| Descrição do problema             | ✔️          | ⬜        |
| Requisitos funcionais e não func. | ✔️          | ⬜        |
| Casos de uso                      | ✔️          | ⬜        |
| Diagrama de Classes               | ✔️          | ⬜        |
| Definição dos endpoints           | ✔️          | ⬜        |
| Models implementados              | ✔️          | ⬜        |
| Serializers implementados         | ✔️          | ⬜        |
| Views e URLs                      | ✔️          | ⬜        |
| Admin configurado                 | ✔️          | ⬜        |
| Swagger funcionando               | ✔️          | ⬜        |
| README completo                   | ✔️          | ⬜        |

---

## **Modelo de Critérios Detalhados de Avaliação (Rubricas de Correção)**

### **A. Planejamento & Documentação (Peso Máximo Sugerido: 35 Pontos)**
**(Verifica adesão metodológica: Fases 0, 1 e 2)**

| Competência Avaliada | Critério de Proficiência (Máx. Pontos) | Descrição Detalhada Esperada | PONTUAÇÃO ATRIBUÍDA |
| :--- | :--- | :--- | :---: |
| **Estruturação do Workflow (F0)** | 10 pontos | Demonstração de um fluxo completo e automatizado no Git/GitHub (Issues $\rightarrow$ Projects $\rightarrow$ PRs). | / 10 |
| **Qualidade dos Requisitos (F1)** | 15 pontos | Diferenciação clara entre RF, NFR (segurança, performance) e inclusão de critérios de sucesso mensuráveis. | / 15 |
| **Modelagem Arquitetural (F2)** | 10 pontos | Diagrama robusto com justificativa arquitetural explícita (Por que Django REST? Como o *backend* interage?). | / 10 |

### **B. Execução Técnica & Implementação (Peso Máximo Sugerido: 40 Pontos)**
**(Verifica aderência técnica e qualidade de código: Fase 3)**

| Competência Avaliada | Critério de Proficiência (Máx. Pontos) | Descrição Detalhada Esperada | PONTUAÇÃO ATRIBUÍDA |
| :--- | :--- | :--- | :---: |
| **Estrutura do Código** | 15 pontos | Uso correto dos módulos Django/DRF; código modularizado, seguindo princípios SOLID e PEP8. | / 15 |
| **Funcionalidade (Endpoints)** | 15 pontos | Todos os *endpoints* críticos implementados com sucesso (CRUD completo) e documentação OpenAPI correta. | / 15 |
| **Testabilidade** | 10 pontos | Presença de testes unitários/integração cobrindo o fluxo principal do negócio (TDD é um diferencial). | / 10 |

### **C. Transição, Testes e Apresentação (Peso Máximo Sugerido: 25 Pontos)**
**(Verifica capacidade de entrega sob pressão: Fase 4)**

| Competência Avaliada | Critério de Proficiência (Máx. Pontos) | Descrição Detalhada Esperada | PONTUAÇÃO ATRIBUÍDA |
| :--- | :--- | :--- | :---: |
| **Robustez dos Testes** | 10 pontos | Capacidade de identificar e reportar *bugs* ou falhas lógicas durante o teste (não apenas funcionalidade que funciona). | / 10 |
| **Documentação Final (User Guide)** | 5 pontos | Guia de uso conciso, focado no consumidor da API, com exemplos de requisições/payloads. | / 5 |
| **Performance na Apresentação** | 10 pontos | Transmissão clara, objetiva e convincente do raciocínio técnico durante a demonstração (capacidade de defesa do projeto). | / 10 |

