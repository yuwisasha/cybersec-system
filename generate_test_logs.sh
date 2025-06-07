#!/bin/bash

echo "📄 Генерация тестовых логов в journalctl..."

# 1. Критический: Аутентификация — Блокировка IP
echo "🛡️  [1] Аутентификация (authentication failure)"
for i in {1..20}; do
  logger "sshd[$((2000+i))]: authentication failure for root from 192.168.1.100"
  sleep 0.2
done

sleep 1

# 2. Высокий: Конфигурация — Аудит доступа
echo "⚙️  [2] Изменение конфигурации (visudo)"
for i in {1..20}; do
  logger "sudo[$((3000+i))]: visudo session opened by admin"
  sleep 0.2
done

sleep 1

# 3. Средний: Работа с файлами — Анализ логов
echo "📁 [3] Работа с файлами (deleted)"
for i in {1..20}; do
  logger "auditd[$((4000+i))]: user deleted /etc/passwd.backup"
  sleep 0.2
done

sleep 1

# 4. Критический: Повышение привилегий — Изоляция
echo "🔐 [4] Повышение привилегий (sudo → root)"
for i in {1..20}; do
  logger "sudo[$((5000+i))]: user gained root privileges"
  sleep 0.2
done

sleep 1

# 5. Высокий: Аномалия — Сброс пароля
echo "🤖 [5] Аномальное поведение (unexpected behavior)"
logger "kernel: unexpected behavior: system clock jumped 15 seconds"

echo "✅ Готово. Подожди 30–60 секунд, чтобы правила сработали."
