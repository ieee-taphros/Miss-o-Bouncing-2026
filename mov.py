"""
teste_navegacao_manual_arm.py

Teste onde você arma manualmente no terminal do SITL.
"""

"Norte	latitude + delta"
"Sul	latitude - delta"
"Leste	longitude + delta"
"Oeste	longitude - delta"

from vehicle import Vehicle
from navigation import NavResult
import time

print("=" * 60)
print("TESTE DE NAVEGAÇÃO - ARM MANUAL")
print("=" * 60)
print()
print("⚠️  IMPORTANTE: No terminal do SITL, digite:")
print("    arm uncheck all")
print("    ou")
print("    arm throttle")
print()

drone = Vehicle("udp:127.0.0.1:14550")
planox = 0.00014
planoy = 0.00008

try:
    # Conectar
    print("1. Conectando...")
    drone.connect()
    drone.wait_ready(timeout=15)
    drone.print_status()
    
    # Modo GUIDED
    print("\n2. Mudando para GUIDED...")
    drone.set_mode("GUIDED")
    print(f"   Modo: {drone.state.flight_mode()}")
    
    # Aguardar armar manualmente
    print("\n3. Aguardando ARM manual...")
    print("   Vá no terminal do SITL e digite: arm uncheck all")
    
    while not drone.state.is_armed():
        time.sleep(1)
        print(".", end="", flush=True)
    
    print("\n   ✅ Armado!")
    
    # Decolar
    print("\n4. Decolando 7 metros...")
    result = drone.takeoff_guided(5.0, timeout=20.0)
    print(f"   Resultado: {result}")
    time.sleep(3)
    print(f"   Altitude: {drone.state.position.relative_altitude:.1f}m")
    
    # Passo 1 (drone vai até o norte, leste e oeste)

    # Norte
    pos = drone.state.position
    print(f"\n5. Indo para norte...")
    result = drone.goto(
        latitude=pos.latitude + (planox/2),
        longitude=pos.longitude,
        altitude=5.0,
        ground_speed=3.0,
        acceptance_radius=3.0,
        timeout=30.0
    )
    print(f"   Resultado: {result}")
    time.sleep(2)
    
      # Ir para leste
    pos = drone.state.position
    print(f"\n5. Indo para leste...")
    result = drone.goto(
        latitude=pos.latitude,
        longitude=pos.longitude + (planoy/2),
        altitude=5.0,
        ground_speed=3.0,
        acceptance_radius=3.0,
        timeout=30.0
    )
    print(f"   Resultado: {result}")
    time.sleep(2)
    
    # Ir para Oeste
    pos = drone.state.position
    print(f"\n5. Indo para oeste...")
    result = drone.goto(
        latitude=pos.latitude,
        longitude=pos.longitude - planoy,
        altitude=5.0,
        ground_speed=3.0,
        acceptance_radius=3.0,
        timeout=30.0
     )
    print(f"   Resultado: {result}")
    time.sleep(2)
    
    # Passo 2 - Aqui vai ter um for pra repetir o ngc

    for i in range(2):
    #desce pro sul 
      pos = drone.state.position
      print(f"\n5. Indo para sul...")
      result = drone.goto(
          latitude=pos.latitude - (planox/6),
          longitude=pos.longitude,
          altitude=5.0,
          ground_speed=3.0,
          acceptance_radius=3.0,
          timeout=30.0
      )
      print(f"   Resultado: {result}")
      time.sleep(2)
    
    # Ir para leste
      pos = drone.state.position
      print(f"\n5. Indo para leste...")
      result = drone.goto(
          latitude=pos.latitude,
          longitude=pos.longitude + planoy,
          altitude=5.0,
          ground_speed=3.0,
          acceptance_radius=3.0,
          timeout=30.0
      )
      print(f"   Resultado: {result}")
      time.sleep(2)

    #desce pro sul 
      pos = drone.state.position
      print(f"\n5. Indo para sul (+1m)...")
      result = drone.goto(
          latitude=pos.latitude - (planox/6),
          longitude=pos.longitude,
          altitude=5.0,
          ground_speed=3.0,
          acceptance_radius=3.0,
          timeout=30.0
      )
      print(f"   Resultado: {result}")
      time.sleep(2)
    
    # Ir para oeste
      pos = drone.state.position
      print(f"\n5. Indo para oeste...")
      result = drone.goto(
          latitude=pos.latitude,
          longitude=pos.longitude - planoy,
          altitude=5.0,
          ground_speed=3.0,
          acceptance_radius=3.0,
          timeout=30.0
      )
      print(f"   Resultado: {result}")
      time.sleep(2)
    
  
    
    # RTL
    print("\n6. RTL...")
    drone.set_mode("RTL")
    
    while drone.state.is_armed():
        alt = drone.state.position.relative_altitude or 0
        print(f"\r   Alt: {alt:.1f}m", end="")
        time.sleep(1)
    
    print("\n   ✅ Pouso concluído!")

except KeyboardInterrupt:
    print("\nInterrompido!")
    drone.set_mode("RTL")

finally:
    drone.disconnect()
    print("Desconectado!")
