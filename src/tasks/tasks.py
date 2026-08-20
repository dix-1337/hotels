import asyncio
from time import sleep
from pathlib import Path
from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
# worker
# celery -A src.tasks.celery_app:celery_instance worker --pool=solo --loglevel=info
# beat
# celery -A src.tasks.celery_app:celery_instance beat --loglevel=info

@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")

async def send_email_to_users_with_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")

@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(send_email_to_users_with_today_checkin_helper())


#@celery_instance.task
def resize_image_to_widths(
    source_path: str | Path,
    output_dir: str | Path = "src/static/images",
    widths: tuple[int, ...] = (1000, 500, 200),
) -> list[Path]:
    source_path = Path(source_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths: list[Path] = []

    with Image.open(source_path) as image:
        image = image.convert("RGB")

        original_width, original_height = image.size

        for width in widths:
            ratio = width / original_width
            new_width = width
            new_height = int(original_height * ratio)

            resized_image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS,
            )

            output_filename = f"{source_path.stem}_{new_width}px.jpg"
            output_path = output_dir / output_filename

            resized_image.save(
                output_path,
                format="JPEG",
                quality=85,
                optimize=True,
            )

            saved_paths.append(output_path)

    return saved_paths