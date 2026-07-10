# Lab 06 - Application Load Balancer + Auto Scaling Group

## Qué construí

Arquitectura de alta disponibilidad con 2 instancias EC2 detrás de un Application Load Balancer, gestionadas por un Auto Scaling Group con política de escalado por CPU.

## Arquitectura

```
Internet
    |
ALB: alb-web-clase6 (pub-a + pub-b, HTTP:80)
sg-alb: HTTP:80 desde 0.0.0.0/0
    |
Target Group: tg-web-clase6 (HTTP:80, health check /)
    |
    +──── EC2: web-1 (pub-a, 10.0.1.48)
    └──── EC2: web-2 (pub-b, 10.0.2.22)
         sg-web: HTTP:80 desde 0.0.0.0/0

ASG: asg-web-clase6
Launch Template: lt-web-clase6
Min: 1 / Desired: 2 / Max: 4
Política: cpu-60 (Target Tracking, CPU 60%)
```

## Servicios usados

`EC2` `ALB` `Target Groups` `Launch Templates` `Auto Scaling Groups` `CloudWatch`

## Lo que hice

**EC2 con User Data**
- Lancé 2 instancias (web-1 en pub-a, web-2 en pub-b) con Apache y página que muestra la IP privada de cada servidor
- User Data usa IMDSv2 para obtener la IP interna de forma segura

**Target Group**
- Creé `tg-web-clase6` con health check en `/` - el ALB solo manda tráfico a instancias healthy

**Application Load Balancer**
- ALB Internet-facing cubriendo pub-a y pub-b (multi-AZ)
- Listener HTTP:80 → forwarding al Target Group
- Verifiqué balanceo round-robin recargando el navegador

**Launch Template**
- Configuración reutilizable para que el ASG pueda lanzar instancias idénticas automáticamente

**Auto Scaling Group**
- ASG adjunto al Target Group del ALB - las nuevas instancias quedan disponibles automáticamente
- Política Target Tracking `cpu-60`: si el CPU promedio sube del 60%, lanza instancias; si baja, las termina (respetando el mínimo de 1)

## Resultados reales

| Verificación | Resultado |
|---|---|
| DNS del ALB | `alb-web-clase6-1996009002.us-east-1.elb.amazonaws.com` |
| IP web-1 (pub-a) | `10.0.1.48` |
| IP web-2 (pub-b) | `10.0.2.22` |
| Balanceo confirmado | IPs alternando: 10.0.2.22 → 10.0.1.48 → 10.0.2.22 → 10.0.1.48 |
| Instancias lanzadas por el ASG | 2 (i-068f0c00218165be4, i-0df631bf3fac80948) |
| CPU observada en CloudWatch | 0.82% (idle, sin carga) |

## Conceptos clave

- **ALB vs ASG**: el ALB distribuye tráfico, el ASG escala instancias, CloudWatch monitorea. Son tres responsabilidades separadas
- **Target Tracking**: la política más simple - definís el objetivo (CPU 60%) y AWS ajusta el número de instancias automáticamente
- **Multi-AZ**: el ALB en pub-a y pub-b garantiza que si una AZ falla, el tráfico sigue fluyendo por la otra
- **Launch Template como receta**: el ASG usa el template para lanzar instancias idénticas sin configuración manual

## User Data usado

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/local-ipv4)
echo "<h1>Servidor: $IP - Clase 6</h1>" > /var/www/html/index.html
```

Usa **IMDSv2** (token-based) en lugar de IMDSv1 - práctica recomendada de seguridad.