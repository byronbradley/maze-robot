# Parts

Selected parts for the planned maze robot build. The sensor packs contain one spare.

| Part | Quantity | Model / details |
|---|---:|---|
| Controller | 1 | Arduino Nano 33 BLE Sense Rev2 with headers, ABX00070 |
| Chassis | 1 | DIYables 2WD kit, B0H2941XDK; two motors, wheels, caster, four-AA holder and switch |
| Motor driver | 1 | Adafruit DRV8833 breakout, product 3297 |
| Wall sensors | 3 | HC-SR04P, 3-5.5 V version; powered at 3.3 V |
| Batteries | 4 | Energizer NiMH rechargeable AA; 4.8 V nominal pack |
| Charger | 1 | Energizer Recharge Pro, supplied with four AA cells |
| Regulator | 1 | Pololu S7V7F5 #2119; fixed 5 V buck-boost |
| USB power adapter | 1 | Jienk USB-A female screw-terminal adapter; use 5 V and GND only |
| USB cable | 1 | Micro-USB data cable |
| Run button | 1 | Normally open momentary switch |
| Driver resistors | 2 | 10k ohm; sleep pulldown and fault pull-up to 3.3 V |
| Bulk capacitor | 1 | 220 uF, at least 16 V, across driver VM/GND |
| Motor capacitors | 2 | 100 nF ceramic, across each motor |
| Prototyping | As needed | Breadboard, jumpers, hookup wire, headers |
| Mounting | As needed | Three sensor brackets, standoffs, screws, cable ties |
| Supply protection | 1 | Inline fuse and holder, sized for motors and wiring |

The chassis encoder discs are not used by the timed-motion firmware. The corridor simulation uses a 10 cm robot model; this is not the physical chassis width. Measure the assembled chassis when setting maze clearance and motion timing.

See [wiring](wiring.md). HC-SR04P modules use the Nano 3V3 rail and direct echo connections. Do not substitute 5 V-only HC-SR04 modules without changing voltage protection. Remove the AA cells for charging; the charger does not connect to the robot's holder.

## Sources

- [Arduino ABX00070](https://store-usa.arduino.cc/products/nano-33-ble-sense-rev2-with-headers)
- [DIYables chassis](https://diyables.io/products/diyables-2wd-smart-robot-car-chassis-kit-pre-assembled-dual-dc-motor-with-encoder)
- [Adafruit DRV8833](https://www.adafruit.com/product/3297)
- [Pololu S7V7F5](https://www.pololu.com/product/2119)
- [HC-SR04P pack](https://www.amazon.com/dp/B0GL8NJCVT)
