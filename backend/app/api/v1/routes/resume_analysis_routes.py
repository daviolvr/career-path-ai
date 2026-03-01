from fastapi import APIRouter, UploadFile, File, Depends, Query

from app.models.user import User
from app.schemas.resume_analysis_schema import ResumeAnalysisResponse, ResumeAnalysisListResponse, ResumeAnalysisDeleteResponse
from app.api.v1.dependencies.security import verify_token
from app.api.v1.dependencies.services import ResumeAnalysisServiceDep


router = APIRouter()


@router.post("/", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume_analysis_service: ResumeAnalysisServiceDep,
    file: UploadFile = File(...),
    current_user: User = Depends(verify_token),
):
    """
    Faz análise do resumo enviado em .pdf e retorna para o usuário.
    """
    return await resume_analysis_service.analyze_resume_service(
        file, current_user
    )


@router.get("/", response_model=ResumeAnalysisListResponse)
async def get_my_resume_analyses(
    resume_analysis_service: ResumeAnalysisServiceDep,
    current_user: User = Depends(verify_token),
    skip: int = Query(0, ge=0, description="Número de itens para pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de itens por página")
):
    """
    Retorna todas as análises de currículo do usuário autenticado.
    """
    return await resume_analysis_service.get_resume_analysis_service(
        current_user, skip, limit
    )
    

@router.get("/{analysis_id}", response_model=ResumeAnalysisResponse)
async def get_resume_analysis(
    analysis_id: int,
    resume_analysis_service: ResumeAnalysisServiceDep,
    current_user: User = Depends(verify_token),
):
    """
    Retorna uma análise específica do usuário.
    """
    return await resume_analysis_service.get_resume_analysis_by_id_service(
        analysis_id, current_user
    )


@router.delete("/{analysis_id}", response_model=ResumeAnalysisDeleteResponse)
async def delete_resume_analysis(
    analysis_id: int,
    resume_analysis_service: ResumeAnalysisServiceDep,
    current_user: User = Depends(verify_token),
):
    """
    Deleta uma análise de currículo do usuário.
    """
    return await resume_analysis_service.delete_resume_analysis_service(
        analysis_id, current_user
    )
