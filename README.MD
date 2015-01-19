# Scripts Úteis Para Integração Contínua

Coleção de scripts úteis para integração contínua em projetos que utilizem Xcode.

* Requer python 3
* Hooks requerem git v2

## Como Utilizar

Clone o projeto para a pasta scripts na raiz do seu projeto, copie o pre-push.sample
como pre-push na pasta .git/hooks

ex: PROJ-HOME = /Users/alexandre/projetos/my-ios-project

```
$ cd  /Users/alexandre/projetos/my-ios-project
$ git clone git@github.com:garrefa/ci-scripts.git scripts
$ cp scripts/pre-push.sample .git/hooks/pre-push
```

## validate-pbx.py

- checa os targets significativos de um projeto (descarta target de teste)

- verifica quais classes adicionadas a algum dos targest não está presente nos outros

- exibe mensagem com a listagem de targets e classes ausentes.

## pre-push.sample

- script de exemplo para hook de pre-push no git.

- uma vez adicionado ao diretorio .git/hooks do projeto, esse script será executado
antes de cada push para determinar se o push é valido ou não baseado na validação.

- caso exista erro de validação, exibe uma mensagem informando que o push pode potencialmente quebrar os outros targets e oferece ao usuário a opção de continuar ou não.
