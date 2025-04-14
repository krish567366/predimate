# Updated simulator.py
import time
import random
import paho.mqtt.client as mqtt
import json
import docker

# MQTT Broker Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Simulation Parameters (based on 1.1 data)
SIMULATION_INTERVAL = 1  # Seconds
VIBRATION_RANGE = (0, 100)  # mm/s
TEMPERATURE_RANGE = (-40, 150)  # °C
CURRENT_RANGE = (0, 100)  # A
PRESSURE_RANGE = (0, 100)  # bar
FLOW_RANGE = (0, 500)  # L/min
GAS_RANGE = (0, 1000)  # ppm
EMISSIONS_RANGE = (0, 500) # ppm
CPU_RANGE = (0, 100) # percent
MEMORY_RANGE = (0, 256) # GB
DISK_IO_RANGE = (0, 500) # MB/s
NETWORK_LATENCY_RANGE = (0, 200) # ms
NETWORK_PACKET_LOSS_RANGE = (0, 5) # percent

def generate_vibration_data():
    return random.uniform(*VIBRATION_RANGE)

def generate_temperature_data():
    return random.uniform(*TEMPERATURE_RANGE)

def generate_current_data():
    return random.uniform(*CURRENT_RANGE)

def generate_pressure_data():
    return random.uniform(*PRESSURE_RANGE)

def generate_flow_data():
    return random.uniform(*FLOW_RANGE)

def generate_gas_data():
    return random.uniform(*GAS_RANGE)

def generate_emissions_data():
    return random.uniform(*EMISSIONS_RANGE)

def generate_cpu_data():
    return random.uniform(*CPU_RANGE)

def generate_memory_data():
    return random.uniform(*MEMORY_RANGE)

def generate_disk_io_data():
    return random.uniform(*DISK_IO_RANGE)

def generate_network_latency_data():
    return random.uniform(*NETWORK_LATENCY_RANGE)

def generate_network_packet_loss_data():
    return random.uniform(*NETWORK_PACKET_LOSS_RANGE)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        while True:
            vibration = generate_vibration_data()
            temperature = generate_temperature_data()
            current = generate_current_data()
            pressure = generate_pressure_data()
            flow = generate_flow_data()
            gas = generate_gas_data()
            emissions = generate_emissions_data()
            cpu = generate_cpu_data()
            memory = generate_memory_data()
            disk_io = generate_disk_io_data()
            network_latency = generate_network_latency_data()
            network_packet_loss = generate_network_packet_loss_data()

            client.publish("predimate/vibration", json.dumps({"value": vibration, "unit": "mm/s"}))
            client.publish("predimate/temperature", json.dumps({"value": temperature, "unit": "°C"}))
            client.publish("predimate/current", json.dumps({"value": current, "unit": "A"}))
            client.publish("predimate/pressure", json.dumps({"value": pressure, "unit": "bar"}))
            client.publish("predimate/flow", json.dumps({"value": flow, "unit": "L/min"}))
            client.publish("predimate/gas", json.dumps({"value": gas, "unit": "ppm"}))
            client.publish("predimate/emissions", json.dumps({"value": emissions, "unit": "ppm"}))
            client.publish("predimate/cpu", json.dumps({"value": cpu, "unit": "%"}))
            client.publish("predimate/memory", json.dumps({"value": memory, "unit": "GB"}))
            client.publish("predimate/disk_io", json.dumps({"value": disk_io, "unit": "MB/s"}))
            client.publish("predimate/network_latency", json.dumps({"value": network_latency, "unit": "ms"}))
            client.publish("predimate/network_packet_loss", json.dumps({"value": network_packet_loss, "unit": "%"}))

            time.sleep(SIMULATION_INTERVAL)

    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.loop_stop()
        client.disconnect()

def create_docker_mosquitto():
  client = docker.from_env()
  try:
    container = client.containers.run("eclipse-mosquitto:latest", detach=True, ports={'1883/tcp': 1883}, name="predimate-mosquitto")
    print("Mosquitto container started.")
  except docker.errors.APIError as e:
    print(f"Error starting Mosquitto: {e}")

def build_docker_image():
    client = docker.from_env()
    try:
        client.images.build(path=".", tag="predimate-simulator")
        print("Docker image built successfully.")
    except docker.errors.BuildError as e:
        print(f"Error building image: {e}")

if __name__ == "__main__":
    create_docker_mosquitto()
    build_docker_image()
    main()