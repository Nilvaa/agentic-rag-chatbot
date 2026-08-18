import os
import uuid
from fastapi import APIRouter,Depends,File,HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document

router=APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_document(
    file:UploadFile=File(...),
    db:Session=Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="only pdf allowed"   
        )
    unique_filename=f"{uuid.uuid4()}_{file.filename}"
    upload_dir="uploads/documents"
    os.makedirs(upload_dir,exist_ok=True)

    file_path=os.path.join(
        upload_dir,
        unique_filename
    )

    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())

    file_size=os.path.getsize(file_path)

    document=Document(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
        status="PENDING"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document