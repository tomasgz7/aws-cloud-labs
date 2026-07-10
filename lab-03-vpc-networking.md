# Lab 03 - VPC desde cero: Subnets, IGW, NAT Gateway, Route Tables

## Qué construí

VPC personalizada completa con subnets públicas y privadas en múltiples AZs, Internet Gateway para salida pública, NAT Gateway para salida privada, y verificación de conectividad con instancias reales.

## Arquitectura

```
Internet
    |
Internet Gateway (lab-igw)
    |
    +──── rt-public ────+──── pub-a (10.0.1.0/24, us-east-1a) ── bastion EC2
    |                   └──── pub-b (10.0.2.0/24, us-east-1b)
    |
NAT Gateway (nat-a, EIP en pub-a)
    |
    +──── rt-private ───+──── priv-a (10.0.11.0/24) ── app-server EC2
                        └──── priv-b (10.0.12.0/24)
```

## Servicios usados

`VPC` `Subnets` `Internet Gateway` `NAT Gateway` `Elastic IP` `Route Tables` `EC2` `Security Groups`

## Lo que hice

- Creé VPC `lab-vpc` con CIDR 10.0.0.0/16 y DNS hostnames habilitado
- Configuré 4 subnets: 2 públicas (pub-a, pub-b) y 2 privadas (priv-a, priv-b) distribuidas en 2 AZs
- Creé y adjunté Internet Gateway `lab-igw` a la VPC
- Creé NAT Gateway `nat-a` en pub-a con Elastic IP para permitir salida a Internet desde subnets privadas
- Configuré Route Tables independientes: `rt-public` (0.0.0.0/0 → IGW) y `rt-private` (0.0.0.0/0 → NAT)
- Verifiqué conectividad con instancias reales en subnets pública y privada

## Resultados reales

| Verificación | Resultado |
|---|---|
| `curl checkip.amazonaws.com` desde bastion (pública) | `3.236.115.35` (IP del IGW) |
| `curl checkip.amazonaws.com` desde app-server (privada) | EIP del NAT Gateway (confirmado) |
| ARN del rol en app-server | `arn:aws:sts::563267999368:assumed-role/LabRole/i-001f321919a54db59` |

## Conceptos clave

- **IGW vs NAT Gateway**: IGW es bidireccional (entrada + salida), NAT es solo salida. Las instancias privadas salen a Internet por NAT pero no son accesibles desde afuera
- **Route Tables**: cada subnet se asocia a una Route Table. Sin la ruta 0.0.0.0/0 correcta, la instancia no tiene salida a Internet
- **Security Group stateful vs NACL stateless**: los SG recuerdan la conexión y permiten la respuesta automáticamente; las NACL requieren reglas explícitas en ambas direcciones
- **IPs disponibles en una /24**: 256 - 5 reservadas por AWS = 251 usables

## Tabla de subnets

| Nombre | CIDR | AZ | Tipo | Auto-assign IP |
|---|---|---|---|---|
| pub-a | 10.0.1.0/24 | us-east-1a | Pública | ON |
| pub-b | 10.0.2.0/24 | us-east-1b | Pública | ON |
| priv-a | 10.0.11.0/24 | us-east-1a | Privada | OFF |
| priv-b | 10.0.12.0/24 | us-east-1b | Privada | OFF |

## Nota

La VPC `lab-vpc` y sus componentes (subnets, IGW, Route Tables) se mantuvieron intactos y se reutilizaron como infraestructura base en los Labs 04, 05, 06 y 07.