# AWS Cloud Labs - Portfolio

Laboratorios prácticos de arquitectura en la nube realizados en AWS Academy (IFTS N°21 - Arquitectura de Sistemas en la Nube, 2026).

Cada lab fue ejecutado en un entorno real de AWS (Learner Lab con créditos reales) y documentado con resultados obtenidos, no con valores de ejemplo.

---

## Arquitectura progresiva

```
Lab 02  →  Lab 03  →  Lab 04  →  Lab 05  →  Lab 06  →  Lab 07
IAM+S3      VPC         VPC+EC2    Contenedores  ALB+ASG     Flask+
+EC2        desde       +S3+IAM    +Serverless              Carga+CF
            cero        integrado
```

Cada lab construye sobre el anterior. La VPC creada en el Lab 03 se reutiliza en todos los labs siguientes.

---

## Labs

| Lab | Tema | Servicios AWS |
|---|---|---|
| [Lab 02](./lab-02-iam-s3-ec2/) | IAM + S3 + EC2 | IAM, S3, EC2, Security Groups |
| [Lab 03](./lab-03-vpc-networking/) | VPC desde cero | VPC, Subnets, IGW, NAT Gateway, Route Tables |
| [Lab 04](./lab-04-vpc-ec2-s3-iam/) | Lab integrador | VPC, EC2, S3, IAM Instance Profile |
| [Lab 05](./lab-05-containers-serverless/) | Contenedores y Serverless | EC2, Docker, ECS/Fargate (diseño), Lambda (diseño), SQS, SES |
| [Lab 06](./lab-06-alb-asg/) | ALB + Auto Scaling | ALB, Target Groups, Launch Templates, ASG, CloudWatch |
| [Lab 07](./lab-07-flask-alb-asg-pytest/) | App Flask escalable | Flask, ALB, ASG, pytest, CloudFront |

---

## Stack tecnológico

`AWS EC2` `AWS S3` `AWS VPC` `AWS IAM` `AWS ALB` `AWS Auto Scaling` `AWS CloudWatch` `AWS CloudFront` `Python` `Flask` `pytest` `Docker`

---

## Sobre los labs

- Entorno: AWS Academy Learner Lab (us-east-1, créditos reales)
- Todos los resultados registrados son valores reales obtenidos durante la ejecución
- Cada lab incluye limpieza de recursos para gestión de costos
- La VPC personalizada (lab-vpc, 10.0.0.0/16) se mantiene entre labs como infraestructura base
