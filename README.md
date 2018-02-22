
# RIP homework 
#### Набойченко Георгий. КН-201. Вариант 11.
### Задание

Запустить протокол динамической маршрутизации RIP в сети из трех маршрутизаторов.

### Решение
1. Расположил все устройства из условия. 
2. В роутеры добавил плату NM-1FE-TX, чтобы было три порта. 
3. Соединил и настроил интерфейсы на роутерах, настроил сервера и компьютеры.
4. На каждом роутере настроил протокол RIP
    
```sh
        Router1
        Router(config)#router rip 
        Router(config-router)#network 192.168.1.0
        Router(config-router)#network 192.168.10.0
        Router(config-router)#network 10.11.1.0
        Router(config-router)#no auto-summary
        Router(config-router)#exit
  ```
  ```sh
        Router2
        Router(config)#router rip 
        Router(config-router)#network 192.168.2.0
        Router(config-router)#network 192.168.10.0
        Router(config-router)#network 192.168.10.4
        Router(config-router)#no auto-summary
        Router(config-router)#exit
  ```
  ```sh
        Router3
        Router(config)#router rip 
        Router(config-router)#network 192.168.3.0
        Router(config-router)#network 192.168.10.4
        Router(config-router)#network 10.11.1.0
        Router(config-router)#no auto-summary
        Router(config-router)#exit
  ```
 ### Результат
 Получилась сеть с протоколом RIP. Убедиться в этом можно с помощью команд: ```show ip route ``` и ```show ip interface brief```
 #### Router 1
 ```sh
        Router#show ip interface brief 
        Interface              IP-Address      OK? Method Status                Protocol 
        FastEthernet0/0        192.168.10.1    YES manual up                    up 
        FastEthernet0/1        10.11.1.1       YES manual up                    up 
        FastEthernet1/0        192.168.1.1     YES manual up                    up 
        Vlan1                  unassigned      YES unset  administratively down down
   
    Router#show ip route
    Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
           D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
           N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
           E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
           i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
           * - candidate default, U - per-user static route, o - ODR
           P - periodic downloaded static route

    Gateway of last resort is not set

         10.0.0.0/24 is subnetted, 1 subnets
    C       10.11.1.0 is directly connected, FastEthernet0/1
    C    192.168.1.0/24 is directly connected, FastEthernet1/0
    R    192.168.2.0/24 [120/1] via 192.168.10.2, 00:00:04, FastEthernet0/0
    R    192.168.3.0/24 [120/1] via 10.11.1.2, 00:00:19, FastEthernet0/1
         192.168.10.0/30 is subnetted, 2 subnets
    C       192.168.10.0 is directly connected, FastEthernet0/0
    R       192.168.10.4 [120/1] via 192.168.10.2, 00:00:04, FastEthernet0/0

    
 ```
  #### Router 2
 ```sh
        Router#show ip route
        Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
               i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
               * - candidate default, U - per-user static route, o - ODR
               P - periodic downloaded static route

        Gateway of last resort is not set

        R    10.0.0.0/8 [120/1] via 192.168.10.1, 00:00:13, FastEthernet0/0
                        [120/1] via 192.168.10.5, 00:00:17, FastEthernet0/1
        R    192.168.1.0/24 [120/1] via 192.168.10.1, 00:00:13, FastEthernet0/0
        C    192.168.2.0/24 is directly connected, FastEthernet1/0
        R    192.168.3.0/24 [120/1] via 192.168.10.5, 00:00:17, FastEthernet0/1
             192.168.10.0/30 is subnetted, 2 subnets
        C       192.168.10.0 is directly connected, FastEthernet0/0
        C       192.168.10.4 is directly connected, FastEthernet0/1

   
    Router#show ip interface brief 
    Interface              IP-Address      OK? Method Status                Protocol 
    FastEthernet0/0        192.168.10.2    YES manual up                    up 
    FastEthernet0/1        192.168.10.6    YES manual up                    up 
    FastEthernet1/0        192.168.2.1     YES manual up                    up 
    Vlan1                  unassigned      YES unset  administratively down down
 ```
 #### Router 3
 ```sh
        Router#show ip interface brief
        Interface              IP-Address      OK? Method Status                Protocol 
        FastEthernet0/0        10.11.1.2       YES manual up                    up 
        FastEthernet0/1        192.168.10.5    YES manual up                    up 
        FastEthernet1/0        192.168.3.1     YES manual up                    up 
        Vlan1                  unassigned      YES unset  administratively down down
   
    Router#show ip route
    Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
           D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
           N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
           E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
           i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
           * - candidate default, U - per-user static route, o - ODR
           P - periodic downloaded static route

    Gateway of last resort is not set

         10.0.0.0/24 is subnetted, 1 subnets
    C       10.11.1.0 is directly connected, FastEthernet0/0
    R    192.168.1.0/24 [120/1] via 10.11.1.1, 00:00:13, FastEthernet0/0
    R    192.168.2.0/24 [120/1] via 192.168.10.6, 00:00:00, FastEthernet0/1
    C    192.168.3.0/24 is directly connected, FastEthernet1/0
         192.168.10.0/30 is subnetted, 2 subnets
    R       192.168.10.0 [120/1] via 192.168.10.6, 00:00:00, FastEthernet0/1
    C       192.168.10.4 is directly connected, FastEthernet0/1
 ```
