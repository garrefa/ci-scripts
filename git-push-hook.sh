#!/bin/sh

############################################################################
# Script de hook para validações de pré git push                           #
############################################################################
# Desenvolvido por : Alexandre Garrefa                                     #
# alexandre.garrefa@concretesolutions.com.br                               #
# Criado em  : 14/01/2015                                                  #
############################################################################

WORKING_DIR="$(dirname $0)"
python3 "$WORKING_DIR/validate-pbx.py"

if [ $? -gt 0 ]
then  
    read -p "Cara, esse seu push vai foder a porra toda. Confirma? [s|n] " -n 1 -r < /dev/tty
    echo
    if echo $REPLY | grep -E '^[Ss]$' > /dev/null
    then
        exit 0 # push will execute
    fi
    exit 1 # push will not execute
else  
    exit 0 # push will execute
fi  
