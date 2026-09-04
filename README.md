# NOZ-386 — поточне закриття Board / MetaTeam

Цей репозиторій містить відтворюваний **fail-closed** пакет перевірки для
NOZ-386. Пакет фіксує доступний у сесії зріз Linear, але навмисно не називає
його повним live snapshot або прийнятим операційним закриттям: у середовищі
немає Linear workspace API та доступу до workbook v5.1 у Google Drive.

## Перевірка

```bash
python3 scripts/validate_close.py
python3 -m unittest discover -s tests -v
```

Коли повний read-only export і workbook будуть доступні, `coverage.complete`
можна змінити лише після звірки всіх активних задач, а поля приймання — лише
після 86/86, Drive raw read-back і явного operating acceptance.
