# Script automatización práctica parte 1 Nuriiii

## Añadimos las tags de apertura para el compilador sepa como tiene que interpretar este script. 

```shell
#!bin/bash
```

## Creamos la variable usuarios con todos los users que necesitamos crear 
```shell
usuarios=("dev1" "dev2" "dev3" "dev4" "qa1" "qa2" "qa3" "qa4" "admin1" "admin2" "director")
``` 

## Ahora podemos recorrer el array de usuarios con un bucle for para crearlos

```shell
for usuario in "${usuarios[@]}"; do
    sudo useradd -m -s /bin/bash "$user"
done

echo "Usuarios creados jeje"
```
|  Modificadores en uso  |     Función                     |
|------------------------|---------------------------------|
| -m                     | Crea directorio home            |
| -s                     | shell login usuario en /bin/bash|

## Igual que con los usuarios, podemos crear una variable que contenga el array de grupos que vamos a necesitar. 

```shell
grupos=("desarrollo" "calidad" "administracion" "direccion" "empresa")
```

## A mi me interesa asignar un GID manualmente a cada grupo asi que crearé una variable de GID.
```shell
gidGrupos=("1111" "2222" "3333" "4444" "5555")
```

## Con otro bucle for creamos todos los grupos

```shell
for i in "${!grupos[@]}"; do
    grupo="${grupos[$i]}"
    gidGrupo="${gidGrupos[$i]}"
    sudo groupadd "$grupo" --gid "$gidGrupo"
done

echo "Grupos creados jeje"
```

## Para la creación de directorios podemos hacerlo de una forma sencilla anidando directorios que tienen una raiz comun entre llaves 

```shell
sudo mkdir -p /srv/empresa/{desarrollo,calidad,administracion,direccion,empresa}

echo "Carpetitas creadas"
```

|  Modificadores en uso  |     Función                     |
|------------------------|---------------------------------|
| -p                     | Crea directorios con los directorios padre si no existen           | 

## A continuación deberemos cambiar los permisos de los directorios que hemos creado

```shell
sudo chown -R director:empresa /srv/empresa

#Reutilizamos la variable de grupos para crear otro for :) 

for group in "${groups[@]};" do
    sudo chown director:"$group" /srv/empresa/"$group"
done
```

## Ahora vamos a cambiar permisos de directorios

```shell
sudo chown -R director:empresa /srv/empresa
for group in "${groups[@]}"; do
        sudo chown director:"$group" /srv/empresa/"$group"
done
```

## Damos permisos sudo a director, admin1 y admin2

```shell
sudo usermod -aG sudo director
sudo usermod -aG sudo admin1
sudo usermod -aG sudo admin2
```
## Añadimos los permisos a las carpetas

```shell
sudo chmod -R 750 /srv/empresa
sudo chmod -R 640 /srv/empresa/*/*
```

## Creamos ficheros de prueba :D
```shell
for group in "${groups[@]}"; do
        sudo touch /srv/empresa"$group"/prueba_"$group".txt
done
``` 
## Mandamos mensaje de comprobación de que todo ha ido bien
```shell
echo "33"
```