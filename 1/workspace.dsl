workspace "Интернет-магазин" "Демонстрационный пример для домашнего задания 01 - Вариант 2" {
    
    !identifiers hierarchical
    
    model {
        // ===== ПОЛЬЗОВАТЕЛИ =====
        customer = person "Покупатель" "Заказчик услуги, осуществляющий покупку товаров" {
            tags "Customer"
        }
        
        seller = person "Продавец" "Сотрудник магазина, добавляющий товары" {
            tags "Customer"
        }
        
        // ===== ВНЕШНИЕ СИСТЕМЫ =====
        paymentSystem = softwareSystem "Внешняя платежная система" {
            description "Система регистрации платежей по банковским картам"
            tags "ExternalSystem"
        }
        
        emailService = softwareSystem "Email сервис" {
            description "Отправка уведомлений о заказах"
            tags "ExternalSystem"
        }
        
        smsService = softwareSystem "SMS сервис" {
            description "Отправка SMS с подтверждениями"
            tags "ExternalSystem"
        }
        
        // ===== НАША СИСТЕМА =====
        onlineStore = softwareSystem "Интернет-магазин" {
            description "Система для продажи товаров онлайн"
            url "https://www.ozon.ru/"
            tags "SoftwareSystem"
            
            // ----- КЛИЕНТСКИЕ ПРИЛОЖЕНИЯ -----
            mobileApp = container "Мобильное приложение покупателя" {
                description "Приложение для поиска товаров и оформления заказов"
                technology "Android/iOS app"
                tags "MobileApp"
            }
            
            webApp = container "Веб приложение покупателя" {
                description "Приложение для поиска товаров и оформления заказов через браузер"
                technology "Web Browser"
                tags "WebBrowser"
            }
            
            // Связи с внешними системами
            mobileApp -> paymentSystem "Оплата заказа"
            webApp -> paymentSystem "Оплата заказа"
            
            // ----- СЛОЙ BACKEND ДЛЯ КЛИЕНТСКИХ ПРИЛОЖЕНИЙ -----
            mobileBackend = container "Backend мобильного приложения" {
                description "Обработка запросов от мобильного приложения"
                technology "GoLang"
                tags "Container"
            }
            
            webBackend = container "Backend веб приложения" {
                description "Обработка запросов от веб приложения"
                technology "GoLang"
                tags "Container"
            }
            
            // Связи клиентских приложений с бэкендом
            mobileApp -> mobileBackend "Получение данных/выполнение запросов" "WebSocket"
            webApp -> webBackend "Получение данных/выполнение запросов" "WebSocket"
            
            // ----- ДОМЕННЫЕ СЕРВИСЫ -----
            // Сервис пользователей
            userService = container "CRM" {
                description "Учет пользователей и продавцов"
                technology "GoLang"
                tags "Container"
                
                userApi = component "API" {
                    description "Интерфейс для работы с пользователями"
                    technology "GoLang"
                }
                
                userDb = component "Client Database" {
                    description "Информация о пользователях"
                    technology "PostgreSQL"
                    tags "Database"
                }
                
                userApi -> userDb "запрос/изменение данных о пользователях" "TCP :5432"
            }
            
            // Сервис товаров
            productService = container "Inventory" {
                description "Учет товаров"
                technology "GoLang"
                tags "Container"
                
                productApi = component "API" {
                    description "API учета информации о товарах"
                    technology "Golang"
                }
                
                productDb = component "Product Database" {
                    description "Учет информации о товарах"
                    technology "PostgreSQL"
                    tags "Database"
                }
                
                productApi -> productDb "Запрос и обновление информации о товарах" "TCP :5432"
            }
            
            // Сервис корзины
            cartService = container "Cart" {
                description "Управление корзиной покупателя"
                technology "GoLang"
                tags "Container"
                
                cartApi = component "API" {
                    description "Интерфейс для работы с корзиной"
                    technology "Golang"
                }
                
                cartDb = component "Cart Database" {
                    description "Хранение содержимого корзин"
                    technology "PostgreSQL"
                    tags "Database"
                }
                
                cartApi -> cartDb "Сохранение и получение корзины" "TCP :5432"
            }
            
            // Сервис заказов
            orderService = container "Billing" {
                description "Оформление и оплата заказов"
                technology "GoLang"
                tags "Container"
                
                orderApi = component "API" {
                    description "Интерфейс для работы с заказами"
                    technology "GoLang"
                }
                
                orderDb = component "Order Database" {
                    description "Информация о заказах"
                    technology "PostgreSQL"
                    tags "Database"
                }
                
                orderQueue = component "Брокер" {
                    description "Брокер для событий заказов"
                    technology "RabbitMQ"
                    tags "Queue"
                }
                
                orderApi -> orderDb "запрос/изменение данных о заказах" "TCP :5432"
                orderApi -> orderQueue "публикация событий заказа" "AMQP"
            }
            
            // ----- СВЯЗИ МЕЖДУ СЕРВИСАМИ -----
            mobileBackend -> userService "Запрос данных пользователя" "REST/HTTP"
            webBackend -> userService "Запрос данных пользователя" "REST/HTTP"
            
            mobileBackend -> productService "Поиск товаров" "REST/HTTP"
            webBackend -> productService "Поиск товаров" "REST/HTTP"
            
            mobileBackend -> cartService "Работа с корзиной" "REST/HTTP"
            webBackend -> cartService "Работа с корзиной" "REST/HTTP"
            
            mobileBackend -> orderService "Оформление заказа" "REST/HTTP"
            webBackend -> orderService "Оформление заказа" "REST/HTTP"
            
            // Связи между сервисами
            cartService -> productService "Проверка наличия товаров" "REST/HTTP"
            orderService -> cartService "Получение содержимого корзины" "REST/HTTP"
            orderService -> userService "Получение данных покупателя" "REST/HTTP"
            orderService -> productService "Уменьшение остатков" "REST/HTTP"
            
            // Связи с внешними системами
            orderService -> paymentSystem "Запрос на оплату" "REST/HTTPS"
            orderService -> emailService "Отправка подтверждения" "SMTP"
            userService -> smsService "Отправка SMS с кодом" "REST/HTTPS"
            
            // Связи с пользователями
            customer -> mobileApp "Покупка товаров"
            customer -> webApp "Покупка товаров"
            seller -> webApp "Управление товарами"
        }
        
        // Связи пользователей с внешними системами
        customer -> paymentSystem "Ввод данных карты"
    }
    
    views {
        themes default
        
        // ===== SYSTEM CONTEXT DIAGRAM (C1) =====
        systemContext onlineStore "SystemContext" {
            include *
            autoLayout lr
            title "Контекст системы Интернет-магазин"
            description "Как интернет-магазин взаимодействует с пользователями и внешними системами"
        }
        
        // ===== CONTAINER DIAGRAM (C2) =====
        container onlineStore "Containers" {
            include *
            autoLayout lr
            title "Контейнеры системы Интернет-магазин"
            description "Внутреннее устройство системы: приложения, сервисы и базы данных"
        }
        
        // ===== DYNAMIC DIAGRAM =====
        dynamic onlineStore "UC01" {
            autoLayout lr
            title "Сценарий: Оформление заказа"
            description "Последовательность действий при оформлении заказа покупателем"
            
            customer -> onlineStore.mobileApp "1. Открывает мобильное приложение"
            onlineStore.mobileApp -> onlineStore.mobileBackend "2. Запрос на оформление заказа"
            onlineStore.mobileBackend -> onlineStore.userService "3. Получение данных пользователя"
            onlineStore.mobileBackend -> onlineStore.cartService "4. Получение содержимого корзины"
            onlineStore.cartService -> onlineStore.productService "5. Проверка наличия товаров"
            onlineStore.cartService -> onlineStore.orderService "6. Передача данных для заказа"
            onlineStore.orderService -> paymentSystem "7. Запрос на оплату"
            paymentSystem -> onlineStore.orderService "8. Подтверждение оплаты"
            onlineStore.orderService -> onlineStore.productService "9. Уменьшение остатков товаров"
            onlineStore.orderService -> emailService "10. Отправка подтверждения на email"
            onlineStore.orderService -> onlineStore.mobileBackend "11. Заказ оформлен"
            onlineStore.mobileBackend -> onlineStore.mobileApp "12. Отображение статуса заказа"
            onlineStore.mobileApp -> customer "13. Заказ успешно оформлен"
        }
        
        // ===== STYLES =====
        styles {
            element "Person" {
                color #ffffff
                fontSize 22
                shape Person
                background #08427b
            }
            
            element "Customer" {
                background #08427b
            }
            
            element "ExternalSystem" {
                background #c0c0c0
                color #ffffff
            }
            
            element "SoftwareSystem" {
                background #1168bd
                color #ffffff
            }
            
            element "Container" {
                background #438dd5
                color #ffffff
            }
            
            element "WebBrowser" {
                shape WebBrowser
                background #438dd5
                color #ffffff
            }
            
            element "MobileApp" {
                shape MobileDevicePortrait
                background #438dd5
                color #ffffff
            }
            
            element "Database" {
                shape Cylinder
                background #438dd5
                color #ffffff
            }
            
            element "Queue" {
                shape Pipe
                background #438dd5
                color #ffffff
            }
            
            element "Component" {
                background #85bbf0
                color #000000
                shape Component
            }
        }
    }
}