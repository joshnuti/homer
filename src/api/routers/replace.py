from fastapi import APIRouter, File, UploadFile
from ..helpers.file import config_path

router = APIRouter(
    prefix="/config/replace",
    tags=['Config']
)

@router.post("")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(config_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}