
# Weather Data Capturer

  

**Contato**

- Email: lecsalarini@gmail.com

- GitHub: [https://github.com/salarini-e](https://github.com/salarini-e)

  

## Sobre o Projeto

  

Este projeto é um sistema de coleta e visualização de dados meteorológicos, desenvolvido em Django. O sistema permite coletar dados de diferentes estações meteorológicas, visualizá-los através de uma interface web amigável, e possibilita que os usuários sugiram novas estações para serem adicionadas ao sistema.

  

## Desenvolvimento Local

  

Para usuários linux

  

```shell

## setup a venv inside this project

python  -m  venv  .venv

## enter your venv

source  ./venv/bin/activate

## install the dependencies

python  -m  pip  install  -r  requirements.txt

## do the db migrations

python  manage.py  migrate

```

  

Inicia a aplicação

  

```shell

## run django server

python  manage.py  runserver

```

  

Rode sua primeira coleta de dados

  

```shell

curl  127.0.0.1:8000/get_data/  -s  -o  /dev/null

curl  127.0.0.1:8000/create_demo_sources/  -s  -o  /dev/null

```

  

Abra em seu navegador [localhost:8000](http://127.0.0.1:8000)

Você deve adicionar no cron a rota localhost:8000/get-dados/ a cada 15min

  

No cron adicione essa linha

```shell

*/15 * * * * curl -s http://<dominio>/get-dados/ > /dev/null 2>&1

```

Não esqueça de por o dóminio correto.

Por exemplo: https://cdm.esalarini.com.br/get-dados/ ou http://localhost:8000/get-dados/

  

## Funcionalidades Principais

  

-  **Coleta de Dados**: Coleta automática de dados meteorológicos de diversas fontes.

-  **Visualização de Dados**: Interface web para visualização dos dados coletados.

-  **Filtragem**: Possibilidade de filtrar dados por data, fonte e outros parâmetros.

-  **Sugestão de Estações**: Os usuários podem sugerir novas estações meteorológicas para serem adicionadas ao sistema.

-  **Gerenciamento de Sugestões**: Interface administrativa para aprovação ou rejeição de sugestões de estações.

  

## Estrutura do Projeto

  

O projeto está organizado nos seguintes aplicativos Django:

  

-  **data_scraper**: Responsável pela coleta de dados meteorológicos.

- Implementa Web Scraping para coletar dados automaticamente

- Define modelos para armazenamento de dados meteorológicos

- Gerencia as fontes de dados (estações)

- Processa sugestões de novas estações

-  **data_display**: Gerencia a exibição e visualização dos dados coletados.

- Interface de usuário para visualização de dados

- Exportação de dados para CSV

- Filtragem de dados por período e fonte

- Interface para sugerir e gerenciar novas estações

-  **authentication**: Lida com autenticação e autorização de usuários.

- Controle de acesso a funcionalidades administrativas

  

## Contribuindo

  

Este é um projeto open source e contribuições são bem-vindas. Para contribuir:

  

1. Faça um fork do repositório

2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)

3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)

4. Push para a branch (`git push origin feature/nova-feature`)

5. Crie um novo Pull Request

  

## Licença

  

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
