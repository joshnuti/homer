from fastapi import APIRouter, File, UploadFile, Header, HTTPException
from fastapi.responses import FileResponse
from ..helpers.file import verify_config_path

router = APIRouter(
    prefix="/config/file",
    tags=['File'],
)

@router.get("", response_class=FileResponse, response_model_exclude_none=True)
async def download(CONFIG_PATH: str | None = Header(None)):
    path = verify_config_path(CONFIG_PATH)
    return FileResponse(path, media_type='application/yaml')

@router.post("", response_model_exclude_none=True)
async def upload(file: UploadFile = File(...), CONFIG_PATH: str | None = Header(None)):
    path = verify_config_path(CONFIG_PATH)

    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    return {"message": f"Successfully uploaded {file.filename} to {path}"}