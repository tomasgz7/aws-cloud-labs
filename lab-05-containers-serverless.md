# Lab 05 - Contenedores y Serverless: Docker, ECS/Fargate, Lambda

## Qué cubrí

Conceptos y diseño de arquitecturas con contenedores (Docker, ECS, Fargate) y serverless (Lambda, SQS, SES). El Learner Lab tiene restricciones de permisos para ECS/Fargate, por lo que este lab combina ejercicios prácticos de Docker con diseño de arquitecturas serverless.

## Servicios analizados

`Docker` `ECS` `Fargate` `Lambda` `SQS` `SES` `ECR` `CloudWatch`

## Lo que hice

### Docker - Conceptos prácticos

Analicé el flujo completo de containerización:

```
Dockerfile → docker build → imagen local
imagen local → docker run -p 3000:3000 → contenedor corriendo
imagen local → ECR (push) → ECS/Fargate (deploy)
```

Puntos clave entendidos:
- `EXPOSE` en el Dockerfile es solo documentación - el puerto real lo abre `-p` en `docker run` o las reglas del Security Group en AWS
- Las imágenes en AWS se almacenan en **Amazon ECR** (equivalente privado de Docker Hub dentro del ecosistema AWS)

### Lambda - Diseño de arquitectura para fintech

**Escenario**: sistema de notificaciones por email para transferencias > $10.000 ARS, con 50.000 transferencias/día y picos de 500/minuto.

| Decisión de diseño | Elección | Justificación |
|---|---|---|
| Trigger para Lambda | SQS | Desacopla el sistema, absorbe picos de 500/min sin perder eventos |
| Servicio de email | Amazon SES | Diseñado para envío masivo transaccional a bajo costo |
| ¿Cold start es problema? | No | Un email de notificación tolera 200-500ms de latencia adicional |
| Costo mensual estimado | ~$0.10/mes | 50.000 inv/día × 30 días, 256MB, 500ms promedio |
| EC2 vs Fargate vs Lambda | Lambda | Función puntual por evento, escala automático a picos, costo casi cero vs ~$30/mes de EC2 |

### Preguntas de análisis respondidas

- **Spot Instances**: para workloads tolerantes a interrupciones (ML, batch). No para producción crítica
- **Cold start**: latencia adicional al inicializar el entorno de ejecución por primera vez o post-inactividad - no es un error
- **Fargate vs ECS con EC2**: Fargate = contenedores sin gestionar infraestructura. ECS con EC2 requiere gestionar el cluster
- **Lambda duración máxima**: 15 minutos (hard limit). Para procesos más largos: Step Functions, ECS o EC2

## Arquitectura Lambda + SQS + SES

```
Sistema de transferencias
        |
        ↓ (si monto > $10.000 ARS)
      SQS Queue
        |
        ↓ (trigger)
   Lambda Function
        |
        ↓
   Amazon SES → Email al cliente
```

Esta arquitectura soporta los picos de 500/minuto sin pérdida de eventos gracias al buffer de SQS, y Lambda escala automáticamente sin gestión de infraestructura.

## Preguntas para el examen (Cloud Practitioner)

| Pregunta | Respuesta | Razón |
|---|---|---|
| Contenedores sin gestionar EC2 | Fargate | ECS con EC2 requiere gestionar el cluster |
| Duración máxima de Lambda | 15 minutos | Hard limit del servicio |
| Spot Instances: cuándo usarlas | Workloads tolerantes a interrupción (ML, batch) | Hasta 90% de descuento pero interrumpibles |
| Servidor 24/7 todo el año | Reserved Instance | 1 año de compromiso = hasta 72% de ahorro vs On-Demand |