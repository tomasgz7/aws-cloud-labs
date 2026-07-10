# Lab 07 - App Flask del Clima: EC2 + ALB + ASG + pytest + CloudFront

## Qué construí

App web Python (Flask) que consulta temperatura en tiempo real via Open-Meteo API, desplegada con alta disponibilidad en AWS: 2 instancias EC2 detrás de un ALB, gestionadas por un ASG con escalado automático por CPU, con suite de tests automatizados que genera carga real.

## Arquitectura

```
Internet
    |
[CloudFront - no disponible en Learner Lab]
    |
ALB: alb-web-clase7 (pub-a + pub-b, HTTP:80)
sg-alb: HTTP:80 desde 0.0.0.0/0 | Outbound: All traffic
    |
Target Group: tg-flask-clase7 (puerto 5000)
    |
    +──── EC2: web-1 (pub-a) ── Flask app :5000
    └──── EC2: web-2 (pub-b) ── Flask app :5000
         sg-web: TCP:5000 desde sg-alb | SSH:22 desde AWS Instance Connect range

ASG: asg-web (Min:1 / Desired:2 / Max:4)
Launch Template: lt-web (Flask User Data)
Política: cpu-60 (Target Tracking CPU 60%)

CloudWatch: métrica CPUUtilization por ASG
```

## Servicios usados

`EC2` `ALB` `Target Groups` `Launch Templates` `Auto Scaling Groups` `CloudWatch` `CloudFront (diseño)` `Python` `Flask` `pytest`

## Lo que hice

**Flask en EC2 via User Data**

La app consulta la API Open-Meteo y devuelve temperatura actual para 4 ciudades argentinas. Se despliega automáticamente en cada instancia via User Data, sin intervención manual.

**Security Groups con mínimo privilegio**

- `sg-alb`: recibe HTTP:80 del exterior
- `sg-web`: solo acepta tráfico desde `sg-alb` en el puerto 5000 - las instancias no son accesibles directamente desde Internet

**Tests automatizados con pytest**

4 tests que verifican funcionalidad y generan carga real:

| Test | Qué verifica |
|---|---|
| `test_app_responde` | HTTP 200 y datos de clima en la respuesta |
| `test_todas_las_ciudades` | Buenos Aires, Córdoba, Mendoza y Rosario responden |
| `test_balanceo` | 20 requests detectan más de 1 servidor (balanceo funcionando) |
| `test_carga_sostenida` | 800 requests (200 iteraciones × 4 ciudades) para disparar el ASG |

## Resultados reales

| Verificación | Resultado |
|---|---|
| `test_app_responde` | PASSED |
| `test_todas_las_ciudades` | PASSED |
| `test_balanceo` | PASSED - servidores detectados: `ip-10-0-1-128`, `ip-10-0-2-136` |
| `test_carga_sostenida` | PASSED |
| CPU máxima en CloudWatch durante carga | 0.682% |
| ¿Alarma cpu-60 se disparó? | No (t2.micro usa burst credits - absorbe carga sin subir la métrica) |
| ¿ASG lanzó nuevas instancias? | No (CPU no superó el umbral) |
| CloudFront | No disponible - AWS Academy no otorga permisos `cloudfront:ListDistributions` al rol voclabs |

## Por qué la CPU no subió del 60%

Las instancias t2.micro acumulan créditos de CPU burst. Con créditos disponibles, absorben la carga sin que la métrica CPUUtilization suba. Para disparar el ASG en un lab de este tipo se necesita agotar los créditos con carga sostenida durante más tiempo, o bajar el Target Value de la política a 30%.

## CloudFront - análisis teórico

Aunque no fue posible configurarlo en el Learner Lab (permisos restringidos), se analizó el diseño:

- **Por qué CachingDisabled para esta app**: los datos del clima cambian constantemente - cacharlos mostraría temperaturas desactualizadas
- **Cuándo usar TTL alto**: contenido estático (imágenes, CSS, JS, HTML fijo) que no cambia entre requests
- **Origin**: el DNS del ALB sin `http://` - CloudFront se conecta al ALB como origen

## Código de tests

Ver [`test_carga.py`](./test_carga.py)