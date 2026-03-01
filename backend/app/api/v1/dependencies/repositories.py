from typing import Annotated
from fastapi import Depends

from app.api.v1.dependencies.database import SessionDep
from app.repository.user_repository import UserRepository
from app.repository.resume_analysis_repository import ResumeAnalysisRepository
from app.repository.interview_guide_repository import InterviewGuideRepository
from app.repository.development_trail_repository import DevelopmentTrailRepository


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


async def get_resume_analysis_repository(session: SessionDep) -> ResumeAnalysisRepository:
    return ResumeAnalysisRepository(session)


async def get_interview_guide_repository(session: SessionDep) -> InterviewGuideRepository:
    return InterviewGuideRepository(session)


async def get_development_trail_repository(session: SessionDep) -> DevelopmentTrailRepository:
    return DevelopmentTrailRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
ResumeAnalysisRepositoryDep = Annotated[ResumeAnalysisRepository, Depends(get_resume_analysis_repository)]
InterviewGuideRepositoryDep = Annotated[InterviewGuideRepository, Depends(get_interview_guide_repository)]
DevelopmentTrailRepositoryDep = Annotated[DevelopmentTrailRepository, Depends(get_development_trail_repository)]