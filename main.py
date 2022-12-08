import network,_thread,machine,ubinascii
from machine import Pin
from time import sleep
from umqttsimple import MQTTClient
from machine import Pin,PWM

def moverServo():
    while True:
        servo.duty(50)
        sleep(1)
        servo.duty(120)
        sleep(1)
#Maquina        
def mostrar(topico,mensaje):
    #Hall Sensor
    sensor=Pin(22,Pin.IN)
    contador=0
    metros=int(mensaje.decode())
    print('[INFO] ENROLLANDO {} m'.format(metros))
    _thread.start_new_thread(moverServo,())
    total = 0.2083*(metros-7)
    while(metros > 0):
        m1.value(0)
        m2.value(1)
        state = sensor.value()
        if(state == 0):
            contador+=1
            print("[INFO] Contador {} :".format(contador))
            print("[INFO] Total {} :".format(round(total)))
            sleep(0.1)
            if(contador == round(total)):
                contador = 0
                m1.value(0)
                m2.value(0)
                print("centimetros completos :")
                print('Ingrese otra medida [cm]:')
                metros=int(mensaje.decode())
                break


if __name__ == "__main__":
    #RED
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    print('[INFO] CONNETING')
    wlan.connect("Helen","43729280")#credenciales wifi SSID y contraseña
    while not wlan.isconnected():
        pass
    print('[INFO] WLAN CONNECTED!!')
    #MOTOR
    m1=Pin(12,Pin.OUT)
    m2=Pin(14,Pin.OUT)
    #Servo
    servo=PWM(Pin(23),freq=50)
    #MQTT
    print('ENVIE LA MEDIDA DESDE EL BROKER.....')
    cliente = MQTTClient(ubinascii.hexlify(machine.unique_id()),'test.mosquitto.org')#id y broker de mosquitto  
    cliente.set_callback(mostrar)
    cliente.connect()
    cliente.subscribe("esp32/hilo")#topico 

    while True:
        cliente.check_msg()
