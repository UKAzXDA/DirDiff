#!/bin/bash
helps() {
  echo "Uso: cpre [origem] [destino]"
  echo "Compara arquivos entre dois diretórios recursivamente e indica se são idênticos ou diferentes."
  echo
  echo "Parâmetros:"
  echo "  origem   Diretório base onde os arquivos serão buscados."
  echo "  destino  Diretório base de comparação."
  echo
  echo "By: @UKAzXDA"
  exit 0
}
cpre() {
echo 'KYU(){
if cmp -s "'$1'/$SUBE/$FILE" "'$2'/$SUBE/$FILE"; then
	echo "Indentico: $SUBE/$FILE"
	echo "Indentico: $SUBE/$FILE" >> Identico.txt
else
	echo "Diferente: $SUBE/$FILE"
	echo "Diferente: $SUBE/$FILE" >> Diferente.txt
fi
}' > cpre
find $1 -type f -exec sh -c '
  for filepath; do
    SUBE=$(dirname "$filepath")
    FILE=$(basename "$filepath")
    echo "SUBE=\"$SUBE\";FILE=\"$FILE\"; KYU"
  done
' sh {} + >> cpre
sed -i 's|SUBE="'$1'|SUBE="|g' cpre
sed -i 's|SUBE="\.|SUBE="|g' cpre
bash cpre
rm cpre
}

if [ "$#" -ne 2 ]; then
  helps
  exit 1
fi
