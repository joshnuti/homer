from fastapi import APIRouter, File, UploadFile, Header, HTTPException
from ..helpers.file import config_path

router = APIRouter(
    prefix="/config/file",
    tags=['Config']
)

@router.post("")
async def upload(file: UploadFile = File(...), CONFIG_PATH: str | None = Header(None)):
    if CONFIG_PATH != None:
        path = CONFIG_PATH
    else:
        path = config_path

    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    return {"message": f"Successfully uploaded {file.filename} to {path}"}