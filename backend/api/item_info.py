from typing import List
from datetime import datetime
from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db import models

from backend.schema.iteminfo_schema import (ItemInfoCreate, ItemInfo,
                                            ItemInfoUpdate)
from backend.crud import crud_itemInfo

router = APIRouter()


@router.get('/iteminfo/', response_model=ItemInfo)
def read_iteminfo(item_id: int, user_id: int, db: Session = Depends(get_db)):
    db_iteminfo = crud_itemInfo.item_info.get_iteminfos_with_user_and_item(
        db=db, user_id=user_id, item_id=item_id)
    return db_iteminfo


def convert_to_datetime(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d").date()


@router.post('/iteminfo/create', response_model=ItemInfo)
def create_iteminfo(*,
                    iteminfo: ItemInfoCreate,
                    item_id: int,
                    user_id: int,
                    db: Session = Depends(get_db)):

    new_iteminfo = crud_itemInfo.item_info.create_iteminfos_with_user_and_item(
        db=db, obj_in=iteminfo, item_id=item_id, user_id=user_id)
    return new_iteminfo


@router.put("iteminfo/update", response_model=ItemInfo)
def update_iteminfo(*,
                    iteminfo: ItemInfoUpdate,
                    item_id: int,
                    user_id: int,
                    db: Session = Depends(get_db)):
    db_obj = db.query(ItemInfo).filter((id == item_id)
                                       and (user_id == user_id)).first()
    if db_obj:
        updated_obj = crud_itemInfo.item_info.update(db=db,
                                                     db_obj=db_obj,
                                                     obj_in=iteminfo)
        return updated_obj
    else:
        raise HTTPException(status_code=404, detail="Item info not found.")


@router.delete("iteminfo/delete")
def delete_iteminfo(*, item_info_id: int, db: Session = Depends(get_db)):
    removed_obj = crud_itemInfo.item_info.remove(db=db, id=item_info_id)
    if removed_obj is None:
        raise HTTPException(status_code=500, detail="Remove item info failed.")
    return {"code": 204, "message": "object deleted"}