import pytest
import requests
import time

ALB = 'http://alb-web-1786746584.us-east-1.elb.amazonaws.com'

CIUDADES = ['buenos_aires', 'cordoba', 'mendoza', 'rosario']

def hacer_request(ciudad='buenos_aires', timeout=10):
    r = requests.get(f'{ALB}/?ciudad={ciudad}', timeout=timeout)
    return r.status_code, r.text

def test_app_responde():
    """Verifica que la app devuelve HTTP 200 OK"""
    status, body = hacer_request()
    assert status == 200, f'Se esperaba 200, se obtuvo {status}'
    assert 'Temperatura' in body, 'La respuesta no contiene datos del clima'

def test_todas_las_ciudades():
    """Verifica que las 4 ciudades responden correctamente"""
    for ciudad in CIUDADES:
        status, body = hacer_request(ciudad)
        assert status == 200, f'Error en {ciudad}: status {status}'
        assert 'Temperatura' in body, f'Sin datos de clima para {ciudad}'
        print(f'  OK: {ciudad}')

def test_balanceo():
    """Verifica que el ALB distribuye tráfico entre múltiples instancias"""
    servidores = set()
    for _ in range(20):
        _, body = hacer_request()
        if 'Servidor:' in body:
            srv = body.split('Servidor:')[1][:30].split('<')[0].strip()
            servidores.add(srv)
    print(f'  Servidores detectados: {servidores}')
    assert len(servidores) > 1, (
        f'Solo un servidor respondio: {servidores}. '
        'Verificar que el Target Group tiene al menos 2 instancias healthy.'
    )

def test_carga_sostenida():
    """
    Genera carga sostenida para subir la CPU y disparar el ASG.
    200 iteraciones x 4 ciudades = 800 requests en ~80 segundos.
    """
    errores = 0
    total = 0
    print(f'  Generando carga a: {ALB}')
    for i in range(200):
        for ciudad in CIUDADES:
            status, _ = hacer_request(ciudad, timeout=15)
            total += 1
            if status != 200:
                errores += 1
        time.sleep(0.1)
        if (i + 1) % 50 == 0:
            print(f'  Progreso: {i+1}/200 ({total} requests, {errores} errores)')
    print(f'  Fin: {total} requests, {errores} errores')
    assert errores < 50, f'{errores}/{total} requests fallaron'