
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
