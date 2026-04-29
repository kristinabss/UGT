from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.entities import Technology, UGTAssessment, Product, Industry, Enterprise
from ..schemas.schemas import (
    TechnologyCreate, TechnologyUpdate, TechnologyResponse,
    UGTAssessmentCreate, UGTAssessmentResponse, UGTAssessmentResult,
    UGTAssessmentRequest, DashboardStats
)
from ..services.ugt_service import UGTService
from ..ml.classifier import UGTClassifier

router = APIRouter(prefix="/technologies", tags=["Технологии"])


@router.get("", response_model=List[TechnologyResponse])
def get_technologies(
    skip: int = 0,
    limit: int = 100,
    industry_id: Optional[int] = None,
    enterprise_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получение списка технологий с фильтрацией."""
    query = db.query(Technology)
    
    if industry_id:
        query = query.filter(Technology.industry_id == industry_id)
    if enterprise_id:
        query = query.filter(Technology.enterprise_id == enterprise_id)
    
    technologies = query.offset(skip).limit(limit).all()
    return technologies


@router.get("/{technology_id}", response_model=TechnologyResponse)
def get_technology(technology_id: int, db: Session = Depends(get_db)):
    """Получение информации о технологии по ID."""
    technology = db.query(Technology).filter(Technology.id == technology_id).first()
    if not technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    return technology


@router.post("", response_model=TechnologyResponse, status_code=status.HTTP_201_CREATED)
def create_technology(
    technology: TechnologyCreate,
    db: Session = Depends(get_db)
):
    """Создание новой технологии."""
    db_technology = Technology(**technology.model_dump())
    db.add(db_technology)
    db.commit()
    db.refresh(db_technology)
    return db_technology


@router.put("/{technology_id}", response_model=TechnologyResponse)
def update_technology(
    technology_id: int,
    technology_update: TechnologyUpdate,
    db: Session = Depends(get_db)
):
    """Обновление информации о технологии."""
    db_technology = db.query(Technology).filter(Technology.id == technology_id).first()
    if not db_technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    
    update_data = technology_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_technology, field, value)
    
    db.commit()
    db.refresh(db_technology)
    return db_technology


@router.delete("/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technology(technology_id: int, db: Session = Depends(get_db)):
    """Удаление технологии."""
    db_technology = db.query(Technology).filter(Technology.id == technology_id).first()
    if not db_technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    
    db.delete(db_technology)
    db.commit()
    return None


@router.post("/{technology_id}/assess", response_model=UGTAssessmentResult)
def assess_technology(
    technology_id: int,
    assessment_request: UGTAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Оценка уровня готовности технологии (УГТ).
    Критическая функция системы - автоматическая классификация УГТ.
    """
    # Проверка существования технологии
    technology = db.query(Technology).filter(Technology.id == technology_id).first()
    if not technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    
    # Инициализация сервиса и классификатора
    ugt_service = UGTService(db)
    classifier = UGTClassifier()
    
    # Выполнение оценки
    result = ugt_service.perform_assessment(
        technology_id=technology_id,
        characteristics=assessment_request.characteristics,
        production_metrics=assessment_request.production_metrics,
        economic_metrics=assessment_request.economic_metrics,
        classifier=classifier
    )
    
    return result


@router.get("/{technology_id}/assessments", response_model=List[UGTAssessmentResponse])
def get_technology_assessments(
    technology_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Получение истории оценок УГТ для технологии."""
    assessments = db.query(UGTAssessment)\
        .filter(UGTAssessment.technology_id == technology_id)\
        .order_by(UGTAssessment.assessment_date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return assessments


@router.get("/{technology_id}/forecast")
def forecast_ugt(
    technology_id: int,
    target_ugt: int = 9,
    db: Session = Depends(get_db)
):
    """Прогнозирование времени достижения целевого уровня УГТ."""
    technology = db.query(Technology).filter(Technology.id == technology_id).first()
    if not technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    
    ugt_service = UGTService(db)
    forecast = ugt_service.forecast_ugt_timeline(technology_id, target_ugt)
    
    return forecast
