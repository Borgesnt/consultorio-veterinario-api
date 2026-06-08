# Sistema Clínica Veterinária — Trabalho 4 (Sistemas Distribuídos)

**Universidade Federal do Ceará — Campus Quixadá**
**Disciplina:** Sistemas Distribuídos
**Código:** QXD0043
**Professor:** Rafael Braga

**Discentes:** Alfredo Borges do Nascimento Neto | Gessyca de Oliveira Cunha

**Trabalho 4:** Comunicação Indireta
**Abordagem Escolhida:** Filas de Mensagens (Message Queue)
**Tema:** Clínica Veterinária
**Linguagem:** Python 3
**Tecnologias:** Flask, RabbitMQ, Docker, JSON, Bootstrap

---

# 1. Visão Geral

Este projeto representa a evolução da arquitetura distribuída desenvolvida nos trabalhos anteriores.

Nos Trabalhos 2 e 3 a comunicação era realizada diretamente entre Cliente e Servidor através de RMI e API REST.

Neste Trabalho 4 foi introduzido um mecanismo de **Comunicação Indireta** utilizando **Filas de Mensagens (Message Queues)** através do RabbitMQ.

O objetivo é reduzir o acoplamento entre os componentes do sistema e demonstrar:

* Desacoplamento Espacial
* Desacoplamento Temporal
* Processamento Assíncrono
* Resiliência a Falhas

---

# 2. Arquitetura do Sistema

O sistema é composto pelos seguintes componentes:

```text
Cliente Python
       |
       v
    API Flask
       |
       v
+----------------+
|   RabbitMQ     |
| clinica_queue  |
+----------------+
       |
       v
   Consumer
       |
       v
   data.json
       |
       v
 Dashboard Web
```

---

# 3. Fluxo de Funcionamento

## Cadastro de Animal

1. O cliente envia uma requisição para:

```http
POST /animais
```

2. A API recebe os dados.

3. A API NÃO salva diretamente.

4. A API publica uma mensagem na fila RabbitMQ.

5. O Consumer recebe a mensagem.

6. O Consumer salva o animal no arquivo:

```text
data.json
```

7. O Dashboard exibe os dados atualizados.

---

## Registro de Consulta

O fluxo é semelhante:

```http
POST /consultas
```

A consulta é enviada para a fila e processada posteriormente pelo Consumer.

---

# 4. Comunicação Indireta

O sistema utiliza RabbitMQ como intermediário.

O produtor (API Flask) não conhece:

* IP do consumidor
* Porta do consumidor
* Estado do consumidor

Ele apenas publica mensagens na fila.

O consumidor pode estar:

* Online
* Offline
* Reiniciando

As mensagens permanecem armazenadas até serem processadas.

---

# 5. Desacoplamento Espacial

O produtor não conhece o consumidor.

A API apenas envia mensagens para:

```text
clinica_queue
```

Sem saber quem irá consumi-las.

---

# 6. Desacoplamento Temporal

Caso o Consumer esteja desligado:

```text
Cliente -> API -> RabbitMQ
```

A mensagem permanece armazenada.

Quando o Consumer voltar:

```text
RabbitMQ -> Consumer
```

A mensagem será processada.

---

# 7. Estrutura do Projeto

```text
consultorio-veterinario-api/

├── client-python/
│   └── client.py
│
├── client-javascript/
│   └── client.js
│
├── consumer/
│   └── consumer.py
│
├── server/
│   ├── app.py
│   │
│   ├── mq/
│   │   └── producer.py
│   │
│   ├── utils/
│   │   └── database.py
│   │
│   ├── templates/
│   │   └── dashboard.html
│   │
│   └── models.py
│
├── data.json
│
├── docker-compose.yml
│
└── venv/
```

---

# 8. Principais Componentes

## app.py

API Flask responsável por:

* Receber requisições HTTP
* Publicar mensagens na fila
* Disponibilizar Dashboard
* Disponibilizar endpoints REST

---

## producer.py

Responsável por publicar mensagens no RabbitMQ.

Exemplo:

```json
{
  "acao": "cadastrar_animal",
  "dados": {
    "nome": "Bob",
    "idade": 5,
    "tipo": "Cachorro"
  }
}
```

---

## consumer.py

Responsável por:

* Ler mensagens da fila
* Processar mensagens
* Atualizar data.json
* Registrar eventos
* Incrementar estatísticas

---

## dashboard.html

Interface Web para visualização do sistema.

Exibe:

* Total de animais
* Total de consultas
* Mensagens processadas
* Histórico de eventos
* Lista de animais
* Lista de consultas

---

## data.json

Banco de dados simplificado do projeto.

Armazena:

```json
{
  "animais": [],
  "consultas": [],
  "mensagens_processadas": 0,
  "eventos": []
}
```

---

# 9. Instalação

## Clonar projeto

```bash
git clone <repositorio>
cd consultorio-veterinario-api
```

---

## Criar ambiente virtual

```bash
python3 -m venv venv
```

---

## Ativar ambiente virtual

Linux:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

---

## Instalar dependências

```bash
pip install flask pika requests
```

---

# 10. Executando RabbitMQ

Subir RabbitMQ:

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

---

Painel RabbitMQ:

```text
http://localhost:15672
```

Usuário:

```text
guest
```

Senha:

```text
guest
```

---

# 11. Executando o Sistema

## Terminal 1

RabbitMQ

```bash
docker compose up -d
```

---

## Terminal 2

Consumer

```bash
python consumer/consumer.py
```

Saída esperada:

```text
🐰 CONSUMIDOR CLÍNICA VETERINÁRIA
Aguardando mensagens...
```

---

## Terminal 3

API Flask

```bash
cd server
python app.py
```

Saída esperada:

```text
Running on http://127.0.0.1:5000
```

---

## Terminal 4

Cliente Python

```bash
python client-python/client.py
```

ou

Cliente JavaScript

```bash
cd client-javascript

npm install

node client.js
```

---

# 12. Dashboard

Abrir navegador:

```text
http://localhost:5000/dashboard
```

O Dashboard mostra:

* Quantidade de animais
* Quantidade de consultas
* Quantidade de mensagens processadas
* Eventos da fila
* Animais cadastrados
* Consultas registradas

Atualização automática a cada 3 segundos.

---

# 13. Demonstração do Trabalho

Para demonstrar desacoplamento temporal:

1. Pare o Consumer.

2. Cadastre um animal.

3. Verifique no RabbitMQ que a mensagem está armazenada.

4. Inicie novamente o Consumer.

5. Observe a mensagem sendo processada.

Isso comprova que:

* Nenhuma mensagem foi perdida.
* O produtor continuou funcionando.
* O sistema é resiliente a falhas.

---

# 14. Conclusão

O sistema atende aos requisitos do Trabalho 4 ao implementar Comunicação Indireta através de Filas de Mensagens utilizando RabbitMQ.

A solução demonstra:

* Comunicação Assíncrona
* Desacoplamento Espacial
* Desacoplamento Temporal
* Persistência de Mensagens
* Resiliência a Falhas
* Integração com API REST

mantendo o contexto de uma Clínica Veterinária distribuída.

