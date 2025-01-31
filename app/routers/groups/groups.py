from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.config.logger import logger
from app.database import get_db
from app.auth import VerifyOauth2Token
from .schemas import Group, GroupCreate
from .models import Group as GroupModel, Member as MemberModel, GroupUpdate  # Add GroupUpdate import

router = APIRouter()

# Initialize token verification
token_verification = VerifyOauth2Token()

@router.post("/api/groups", response_model=Group, tags=["Groups"])
def create_group(
    group: GroupCreate, 
    db: Session = Depends(get_db), 
    token: dict = Security(token_verification.verify)
):
    try:
        db_group = GroupModel(**group.dict())
        db.add(db_group)
        db.commit()
        db.refresh(db_group)

        # Get user info from token
        owner_email = token.get("preferred_username", "local@email.no")
        owner_name = token.get("name", "Local User")
        if not owner_email or not owner_name:
            raise HTTPException(status_code=400, detail="Token does not contain required user information.")

        db_member = MemberModel(
            member_id=uuid.uuid4(),
            group_id=db_group.group_id,
            email=owner_email,
            name=owner_name,
            role="owner"
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)

        # Add entry to group_updates table
        try:
            db_group_update = GroupUpdate(
                update_id=uuid.uuid4(),
                group_id=db_group.group_id,
                updated_by=db_member.member_id,
                update_details=f"Opprettet gruppe: {db_group.name}"
            )
            db.add(db_group_update)
            db.commit()
            db.refresh(db_group_update)
        except Exception as e:
            db.rollback()
            logger.error(f"Kunne ikke legge til oppdatering i group_updates: {e}")

        return db_group
    except Exception as e:
        db.rollback()
        logger.error(f"Kunne ikke legge til gruppe: {e}")
        raise HTTPException(status_code=500, detail="Kunne ikke legge til gruppe")

@router.get("/api/groups", response_model=List[Group], tags=["Groups"])
def get_groups(
    db: Session = Depends(get_db), 
    token: dict = Security(token_verification.verify)
):
    groups = db.query(GroupModel).all()
    
    # Add owners to each group
    for group in groups:
        owners = db.query(MemberModel).filter(
            MemberModel.group_id == group.group_id,
            MemberModel.role.in_(["owner", "coowner"])
        ).all()
        group.owners = [{"email": owner.email, "name": owner.name, "role": owner.role} for owner in owners]
    
    return groups

@router.get("/api/groups/{group_id}", response_model=Group, tags=["Groups"])
def get_group(
    group_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    token: dict = Security(token_verification.verify)
):
    group = db.query(GroupModel).filter(GroupModel.group_id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group
