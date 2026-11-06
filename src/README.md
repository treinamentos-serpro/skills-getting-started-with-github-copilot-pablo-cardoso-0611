# API de Atividades da Mergington High School

Uma aplicação FastAPI super simples que permite que estudantes visualizem e se inscrevam em atividades extracurriculares.

## Funcionalidades

- Visualizar todas as atividades extracurriculares disponíveis
- Inscrever-se em atividades
- Visualizar participantes e cancelar uma inscrição pelo ícone de lixeira no card

## Primeiros Passos

1. Instale as dependências:

   ```
   pip install fastapi uvicorn
   ```

2. Execute a aplicação:

   ```
   python app.py
   ```

3. Abra seu navegador e acesse:
   - Documentação da API: http://localhost:8000/docs
   - Documentação alternativa: http://localhost:8000/redoc

## Testes do backend

Na raiz do repositório, instale as dependências de testes:

```bash
python -m pip install -r requirements.txt
```

Execute a suíte com pytest:

```bash
python -m pytest tests -q
```

Os testes ficam em [tests/](../tests/) e usam o `TestClient` do FastAPI,
sem precisar iniciar um servidor. As fixtures criam dados isolados para cada
teste e restauram o estado original ao final, inclusive em caso de falha.
A cobertura inclui redirecionamento, listagem, inscrição e cancelamento,
validando respostas, alterações nos participantes e preservação dos dados
em erros. As regras atuais do backend não são alteradas.

## Endpoints da API

| Método | Endpoint                                                          | Descrição                                                                   |
| ------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Obtém todas as atividades com seus detalhes e contagem atual de participantes |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Inscreve-se em uma atividade                                                |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Cancela uma inscrição; retorna 404 se a atividade ou inscrição não existir |

## Modelo de Dados

A aplicação usa um modelo de dados simples com identificadores significativos:

1. **Activities** - Usa o nome da atividade como identificador:

   - Descrição
   - Horário
   - Número máximo de participantes permitidos
   - Lista de emails dos estudantes inscritos

2. **Students** - Usa email como identificador:
   - Nome
   - Série/Ano escolar

Todos os dados são armazenados em memória, o que significa que os dados serão resetados quando o servidor reiniciar.
