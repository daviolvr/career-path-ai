from fastapi import APIRouter, UploadFile, File, Form, Depends, Query

from app.models.user import User
from app.schemas.interview_guide_schema import InterviewGuideResponse, InterviewGuideListResponse, InterviewGuideDeleteResponse
from app.api.v1.dependencies.security import verify_token
from app.api.v1.dependencies.services import InterviewGuideServiceDep
router = APIRouter()


@router.post("/", response_model=InterviewGuideResponse)
async def generate_interview_guide(
    interview_guide_service: InterviewGuideServiceDep,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: User = Depends(verify_token),
):
    """
    Gera um roteiro detalhado para entrevista baseado no currículo e descrição da vaga
    """
    return await interview_guide_service.generate_interview_guide_service(
        file, job_description, current_user
    )


@router.get("/", response_model=InterviewGuideListResponse)
async def get_my_interview_guides(
    interview_guide_service: InterviewGuideServiceDep,
    current_user: User = Depends(verify_token),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de itens por página"),
):
    """
    Retorna todos os interview_guides do usuário autenticado.
    """
    return await interview_guide_service.get_interview_guide_service(
        current_user, skip, limit
    )


@router.get("/{interview_guide_id}", response_model=InterviewGuideResponse)
async def get_interview_guide(
    interview_guide_id: int,
    interview_guide_service: InterviewGuideServiceDep,
    current_user: User = Depends(verify_token),
):
    """
    Retorna um guia de entrevista específico do usuário.
    """
    return await interview_guide_service.get_interview_guide_by_id_service(
        interview_guide_id, current_user
    )


@router.delete("/{interview_guide_id}", response_model=InterviewGuideDeleteResponse)
async def delete_interview_guide(
    interview_guide_id: int,
    interview_guide_service: InterviewGuideServiceDep,
    current_user: User = Depends(verify_token),
):
    """
    Deleta um guia de entrevista do usuário.
    """
    return await interview_guide_service.delete_interview_guide_service(
        interview_guide_id, current_user
    )