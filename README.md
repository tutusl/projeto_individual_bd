# Banco de Dados - Projeto Individual
Este repositório é destinado para o projeto individual da disciplina Banco de Dados do aluno Arthur Silva Lopes - 18/0030353

## Descrição
Este projeto consiste em um sistema de avaliação de professores, no qual foi desenvolvido um banco de dados SQL juntamente com uma aplicação Flask. Através dessa aplicação, os usuários podem realizar o cadastro, fazer login, criar avaliações, editar avaliações, atualizar seus dados pessoais, reportar uma avaliação e, caso tenham privilégios de administrador, visualizar todos os usuários, excluir usuários, excluir avaliações e verificar os relatórios de avaliações.

## Configuração do Banco de Dados
Para iniciar o banco de dados, siga as etapas abaixo:

1. Navegue até a pasta `databases`
```
cd databases
```
2. Utilize o comando `sudo docker-compose up` para iniciar o contêiner do banco de dados.
```
sudo docker-compose up
```
3. Conecte ao banco de dados no seu SGBD de preferência.
```
<user>: user 
<password>: 1234
<database name>: evaluatedb
<hostname>: localhost
<port>: 3306
```
4. Encontre os scripts necessários para a criação e população do banco na pasta `scripts`.
5. Rode os scripts
   

## Configuração da Aplicação
1. Navegue até a pasta `backend`
```
cd backend
```
2. Utilize o comando `pip install -r requirements.txt`. É recomendado o uso de venv.
```
pip install -r requirements.txt
```
3. Para iniciar a aplicação, utilize o comando `flask run`
```
flash run
```
4. Por fim, acesse o site *`http://127.0.0.1:5000/login`*
