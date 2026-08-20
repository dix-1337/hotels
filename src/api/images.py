import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image_to_widths

router = APIRouter(prefix="/image", tags=["Изображения"])

@router.post("")
def upload_image(file: UploadFile, background_task: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(f"src/static/images/{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    #saved_images = resize_image_to_widths.delay(source_path=image_path)
    #print(saved_images)

    background_task.add_task(resize_image_to_widths, source_path=image_path)
