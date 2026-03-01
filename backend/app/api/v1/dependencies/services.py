from fastapi import Depends
from typing import Annotated

from app.services.user_services import UserService
from app.services.resume_analysis_services import ResumeAnalysisService
from app.services.interview_guide_services import InterviewGuideService
from app.services.development_trail_services import DevelopmentTrailService
from app.api.v1.dependencies.repositories import (
    UserRepositoryDep,
    ResumeAnalysisRepositoryDep,
    InterviewGuideRepositoryDep,
    DevelopmentTrailRepositoryDep
)


async def get_user_service(
    user_repository: UserRepositoryDep
) -> UserService:
    return UserService(user_repository)


async def get_resume_analysis_service(
    resume_analysis_repository: ResumeAnalysisRepositoryDep
) -> ResumeAnalysisService:
    return ResumeAnalysisService(resume_analysis_repository)


async def get_interview_guide_service(
    interview_guide_repository: InterviewGuideRepositoryDep
) -> InterviewGuideService:
    return InterviewGuideService(interview_guide_repository)


async def get_development_trail_service(
    development_trail_repository: DevelopmentTrailRepositoryDep
) -> DevelopmentTrailService:
    return DevelopmentTrailService(development_trail_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ResumeAnalysisServiceDep = Annotated[ResumeAnalysisService, Depends(get_resume_analysis_service)]
InterviewGuideServiceDep = Annotated[InterviewGuideService, Depends(get_interview_guide_service)]
DevelopmentTrailServiceDep = Annotated[DevelopmentTrailService, Depends(get_development_trail_service)]