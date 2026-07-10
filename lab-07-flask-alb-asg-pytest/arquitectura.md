## Flask App con ALB + Auto Scaling en AWS

App web Python (Flask) que consulta temperatura en tiempo real
via Open-Meteo API, desplegada con alta disponibilidad en AWS.

### Arquitectura
- VPC con 2 subnets públicas en distintas AZs (us-east-1a / us-east-1b)
- Application Load Balancer distribuyendo tráfico entre instancias EC2
- Auto Scaling Group (min:1, desired:2, max:4) con política CPU 60%
- Security Groups con reglas de mínimo privilegio (ALB → EC2 en puerto 5000)

### Tests automatizados (pytest)
- test_app_responde: verifica HTTP 200 y datos de clima
- test_todas_las_ciudades: Buenos Aires, Córdoba, Mendoza, Rosario
- test_balanceo: confirma distribución entre múltiples instancias
- test_carga_sostenida: 800 requests para disparar el ASG

### Stack
AWS EC2 · ALB · Auto Scaling · VPC · Security Groups · Python · Flask · Pytest