# Lab 02 - IAM + S3 + EC2

## Qué construí

Exploración de permisos IAM, creación de bucket S3 con versionado y despliegue de servidor web Apache en EC2 con configuración automática via User Data.

## Arquitectura

```
Internet → EC2 (pub, sg HTTP:80 + SSH:22) → Apache web server
                    ↓ IAM Instance Profile
                   S3 Bucket (versionado habilitado)
```

## Servicios usados

`IAM` `S3` `EC2` `Security Groups`

## Lo que hice

**IAM**
- Exploré el rol LabRole y sus políticas AWS Managed adjuntas
- Analicé el JSON de políticas IAM (Effect, Action, Resource)
- Entendí por qué el Learner Lab bloquea `iam:CreateUser` e `iam:CreateRole` - principio de mínimo privilegio en acción

**S3**
- Creé bucket `lab-guzman-clase2` en us-east-1 con Block Public Access total
- Habilité versionado y verifiqué que una eliminación con versionado activo genera un Delete Marker en lugar de borrar definitivamente
- Subí y modifiqué un archivo para confirmar 2 versiones independientes

**EC2**
- Lancé instancia `web-server-clase2` (Amazon Linux 2023, t3.micro) en subnet pública
- User Data instaló Apache automáticamente antes del primer login
- Verifiqué desde EC2 Instance Connect que el Instance Profile permite acceso a S3 sin credenciales manuales

## Resultados reales

| Verificación | Resultado |
|---|---|
| Bucket | `lab-guzman-clase2` |
| Versiones del archivo modificado | 2 |
| IP pública de la instancia | `3.94.81.4` |
| Servidor web responde en http://IP | `Servidor ip-172-31-35-102.ec2.internal` |
| AZ de la instancia | `use1-az6` |
| ARN del rol en la instancia | `arn:aws:sts::563267999368:assumed-role/voclabs/user4948892=Tomas_Guzman` |
| `aws s3 ls` lista el bucket | Sí |

## Conceptos clave

- **Instance Profile**: permite que EC2 asuma un rol IAM y obtenga credenciales temporales via Instance Metadata Service, sin hardcodear keys
- **User Data**: script que se ejecuta una sola vez al primer arranque, antes de cualquier conexión
- **S3 Versioning + Delete Marker**: eliminar un objeto con versionado activo no lo borra, agrega un marcador. Las versiones anteriores siguen disponibles

## Script User Data usado

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Servidor $(hostname -f)</h1>" > /var/www/html/index.html
```
