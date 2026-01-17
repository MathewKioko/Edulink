from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from Database.Users.db_mongo import groups_collection
from Services.group import groupCreate
from Auth.Services.authService import get_current_user

router = APIRouter(tags=["Groups"])


def safe_group_helper(group) -> dict:
    """Safely convert MongoDB document to dict, handling missing fields."""
    try:
        return {
            "id": str(group["_id"]),
            "groupName": group.get("groupName", "Unknown"),
            "subject": group.get("subject", "Unknown"),
            "description": group.get("description", ""),
            "maxMembers": group.get("maxMembers", 0),
            "skillLevel": group.get("skillLevel", "beginner"),
            "meetingFrequency": group.get("meetingFrequency", "Flexible"),
            "meetingTime": group.get("meetingTime"),
            "meetingDate": group.get("meetingDate"),
            "location": group.get("location"),
            "created_at": group.get("created_at"),
            "creatorId": group.get("creatorId")
        }
    except Exception:
        return None


@router.post("/create")
async def create_group(
    group: groupCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new study group.
    Requires authentication (valid JWT token).
    """
    try:
        group_data = group.dict()
        group_data['creatorId'] = str(current_user['_id'])
        
        result = groups_collection.insert_one(group_data)
        new_group = groups_collection.find_one({"_id": result.inserted_id})
        
        return {
            "message": "Group created successfully", 
            "group": safe_group_helper(new_group) if new_group else None,
            "id": str(result.inserted_id)
        }
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed. Please try again later."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create group: {str(e)}"
        )


@router.get("/")
async def get_all_groups():
    """
    Get all study groups.
    Returns empty array if MongoDB is unavailable or no groups exist.
    """
    try:
        groups = []
        for g in groups_collection.find():
            helper_result = safe_group_helper(g)
            if helper_result:
                groups.append(helper_result)
        return {"groups": groups}
    except ServerSelectionTimeoutError:
        return {"groups": [], "error": "Database temporarily unavailable"}
    except ConnectionFailure:
        return {"groups": [], "error": "Connection to database failed"}


@router.get("/my")
async def get_my_groups(current_user: dict = Depends(get_current_user)):
    """
    Get groups created by the current authenticated user.
    """
    try:
        groups = []
        for g in groups_collection.find({"creatorId": str(current_user["_id"])}):
            g["_id"] = str(g["_id"])
            groups.append(g)
        return groups
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed. Please try again later."
        )

