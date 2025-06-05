from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import (
    EventCategory,
    SeverityLevel,
    Recommendation,
    ReactionRule,
    User,
)


def init_initial_data(db: Session):
    # Категории
    if db.query(EventCategory).count() == 0:
        categories = [
            (1, "Аутентификация", "Успешные и неудачные входы в систему"),
            (
                2,
                "Изменение конфигурации",
                "Настройки, политики, права доступа",
            ),
            (3, "Работа с файлами", "Удаление, загрузка, изменение"),
            (4, "Сетевая активность", "Подключения, сканирование портов"),
            (5, "Повышение привилегий", "sudo, su, root-доступ"),
            (6, "Аномальное поведение", "Нетипичная активность"),
        ]
        db.add_all(
            [
                EventCategory(id=id, name=name, description=desc)
                for id, name, desc in categories
            ]
        )

    # Уровни критичности
    if db.query(SeverityLevel).count() == 0:
        severities = [
            (1, "Низкий", "Не требует вмешательства"),
            (2, "Средний", "Потенциальная угроза"),
            (3, "Высокий", "Угроза безопасности"),
            (4, "Критический", "Требует немедленной реакции"),
        ]
        db.add_all(
            [
                SeverityLevel(id=id, name=name, explanation=desc)
                for id, name, desc in severities
            ]
        )

    # Рекомендации
    if db.query(Recommendation).count() == 0:
        recs = [
            (1, "Заблокировать IP-адрес"),
            (2, "Проанализировать логи пользователя"),
            (3, "Изменить пароль администратора"),
            (4, "Провести аудит доступа"),
            (5, "Изолировать рабочую станцию"),
            (6, "Обновить уязвимое ПО"),
        ]
        db.add_all(
            [
                Recommendation(id=id, content=text, created_at=None)
                for id, text in recs
            ]
        )

    # Правила реагирования
    if db.query(ReactionRule).count() == 0:
        rules = [
            (
                4,
                1,
                "внешний",
                1,
            ),  # Критический, Аутентификация, внешний → Блок IP
            (3, 2, "сервер", 4),  # Высокий, Конфигурация, сервер → Аудит
            (2, 3, "рабочая", 2),  # Средний, Файлы, рабочая → Анализ логов
            (4, 5, "сервер", 5),  # Критический, Привилегии, сервер → Изоляция
            (
                3,
                6,
                "локальный",
                3,
            ),  # Высокий, Аномалия, локальный → Сброс пароля
        ]
        db.add_all(
            [
                ReactionRule(
                    severity_id=sid,
                    category_id=cid,
                    source_type=stype,
                    recommendation_id=rid,
                )
                for sid, cid, stype, rid in rules
            ]
        )
        from app.core.auth import get_password_hash

        db.add(User(
            username="admin",
            hashed_password=get_password_hash("supersecret"),
            role="admin"
        ))

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_initial_data(db)
        print("✔ Предустановленные данные загружены.")
    finally:
        db.close()
