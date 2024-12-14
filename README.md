# Задание 8 RPC. gRPC. Protobuf

В ходе работы были созданы два сервера, один из серверов предоставляет пользователю REST API, второй сервер построен на основе grpc и формирует запросы к базе данных. В качестве хранилища терминов использется sqlite , Для валидации входных данных используется pydantic. Для удобства тестирования был использован Swagger. 

Для разворачивания сервера необходимо склонировать репозиторий командой 

```
git clone https://github.com/murzin66/pyweb-task8.git
```

Находясь в директории проекта для сборки образов и запуска контейнеров необходимо выполнить команду
```
docker compose up
```

После выполнения команд на порту 8000 доступен сервер, который принимает REST запросы от пользователя и переадресовывает запросы на grpc сервер. 
Для просмотра доступных API необходимо перейти по маршруту /docs

![image](https://github.com/user-attachments/assets/14b8873d-08d1-4690-a8cc-beef9d610d9a)

 Протестируем доступные API. 
 ## Получим полный список терминов, для этого можно обратиться к маршруту /terms

![image](https://github.com/user-attachments/assets/f11c27e3-4c88-4264-86a2-fd1428c56b80)

## При обращении по адресу /term/{term_name} получаем описание конкретного термина

![image](https://github.com/user-attachments/assets/2993f6a1-c2c4-4d07-83a2-1529e6a9345d)


 ## Протестируем добавление нового термина к списку, воспользуемся возможностями Swagger

![image](https://github.com/user-attachments/assets/ae91cbd3-788a-429a-8d88-b5449ebf54b0)

![image](https://github.com/user-attachments/assets/0b4ab7ef-cccb-49fa-bbbc-4587832810da)

При запросе описания добавленного термина получаем ожидаемый результат

![image](https://github.com/user-attachments/assets/ae3ea299-59b4-4fa1-9ab3-28914e781ba0)

## Протестируем удаление термина 

![image](https://github.com/user-attachments/assets/9cc81363-d1d2-42d7-aba6-240af5f7ff3f)

![image](https://github.com/user-attachments/assets/a0c33018-75ee-4039-9ac4-b17d0e081f33)

## Протестируем изменение термина

![image](https://github.com/user-attachments/assets/2a0241a1-9068-48ae-b284-17cb505c47e2)
![image](https://github.com/user-attachments/assets/f31474dc-37b0-4ba0-a377-54347e4ef8ca)

![image](https://github.com/user-attachments/assets/02a58740-a31d-40cc-8042-dc8e27194c29)

Таким образом, было развернуто веб-приложение, предоставляющее пользователю API для взаимодействия с глоссарием терминов, внешний сервер предоставляет REST и делает запросы со второго сервера, используя grpc. Требуемая функциональность API была успешно протестирована

