# Scripts Úteis Para Integração Contínua

Coleção de scripts úteis para integração contínua em projetos que utilizem Xcode.

* Requer python 3
* Hooks requerem git v2

## Como Utilizar

Clone o projeto para a pasta scripts na raiz do seu projeto.
E copie o pre-push.sample como pre-push na pasta .git/hooks

ex: PROJ-HOME -> /Users/alexandre/projetos/ios-project

```
$ cd  /Users/alexandre/projetos/ios-project
$ git clone git@github.com:garrefa/ci-scripts.git scripts
$ cp scripts/pre-push.sample .git/hooks/pre-push
```

## validate-pbx.py

- checa os targets significativos de um projeto (descarta target de teste)

- verifica quais classes adicionadas a algum dos targest não está presente nos outros

- exibe mensagem com a listagem de targets e classes ausentes.

## git-push-hook.sh

- script que chama o validate-pbx.py e baseado no resultado da validação exibe uma
mensagem de erro informando que o push pode potêncialmente quebrar os outros targets.

- esse script deve ser chamado pelo hook de pre-push do git.

## pre-push.sample

- script de exemplo para hook de pre-push no git.

- uma vez adicionado ao diretorio .git/hooks do projeto, esse script será executado
antes de cada push para determinar se o push é valido ou não baseado na validação.
