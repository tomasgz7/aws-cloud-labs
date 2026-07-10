# Lab 04 - Lab Integrador: VPC + EC2 + S3 + IAM

## Qué construí

Arquitectura web mínima integrando los tres servicios anteriores: instancia EC2 en la VPC personalizada del Lab 03, con servidor Apache automático y acceso a S3 via IAM Instance Profile - sin credenciales manuales.

## Arquitectura

```
Internet → lab-igw → pub-a (10.0.1.0/24)
                          |
                    EC2: web-server-clase4 (t2.micro)
                    sg: HTTP:80 + SSH:22
                          |
                    IAM Instance Profile (LabInstanceProfile)
                          |
                    S3: lab-guzman-clase4 (versionado ON)
```

## Servicios usados

`VPC` `EC2` `S3` `IAM Instance Profile` `Security Groups`

## Lo que hice

- Verifiqué la VPC del Lab 03 antes de empezar (lab-vpc, pub-a, lab-igw, rt-public)
- Creé bucket `lab-guzman-clase4` con versionado habilitado y verifiqué Delete Markers
- Lancé EC2 `web-server-clase4` en pub-a de lab-vpc con LabInstanceProfile asignado
- Verifiqué acceso EC2 → S3 sin credenciales: `aws s3 ls` desde Instance Connect listó el bucket
- Ejecuté lectura y escritura desde EC2 al bucket usando AWS CLI

## Resultados reales

| Verificación | Resultado |
|---|---|
| IP pública de la instancia | `54.236.15.239` |
| Servidor web en http://IP | `Hola desde ip-10-0-1-194.ec2.internal — Clase 4` |
| AZ de la instancia | `us-east-1a (use1-az6)` |
| ARN del rol | `arn:aws:sts::563267999368:assumed-role/voclabs/user4948892=Tomas_Guzman` |
| `aws s3 ls` lista el bucket | Sí |
| Escritura desde EC2 a S3 | Archivo `desde-ec2.txt` subido correctamente |
| Políticas adjuntas al LabRole | 7 |
| ¿Hay algún `Effect: Deny`? | Sí, para `iam:GetPolicy` |

## Análisis IAM

El LabRole tiene 7 políticas adjuntas. Se encontró un `Effect: Deny` explícito para `iam:GetPolicy`, lo que impide leer el detalle de las políticas internas del sandbox — principio de mínimo privilegio aplicado.

El bloqueo de `iam:CreateUser` e `iam:CreateRole` evita que los alumnos generen credenciales persistentes o afecten a otros usuarios del entorno compartido.

## Concepto clave

La instancia EC2 puede acceder a S3 sin credenciales hardcodeadas porque tiene asignado un **IAM Instance Profile**. AWS entrega credenciales temporales automáticamente via el **Instance Metadata Service (IMDS)**. Este es el patrón correcto de seguridad en producción — nunca se ponen access keys en el código o en la instancia.