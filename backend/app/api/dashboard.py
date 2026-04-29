from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.entities import Technology, UGTAssessment
from ..schemas.schemas import DashboardStats, TechnologyResponse
from ..services.ugt_service import UGTService

router = APIRouter(prefix="/dashboard", tags=["Дашборд"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Получение статистики для дашборда.
    - Общее количество технологий
    - Средний уровень УГТ
    - Количество технологий, готовых к внедрению (УГТ >= 7)
    - Распределение по уровням УГТ
    - Динамика изменения УГТ
    - Приоритетные технологии
    """
    ugt_service = UGTService(db)
    stats = ugt_service.get_dashboard_stats()
    return stats


@router.get("/ugt-trend")
def get_ugt_trend(
    days: int = 90,
    db: Session = Depends(get_db)
):
    """Получение динамики среднего УГТ за период."""
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    assessments = db.query(UGTAssessment)\
        .filter(UGTAssessment.assessment_date >= cutoff_date)\
        .order_by(UGTAssessment.assessment_date)\
        .all()
    
    # Группировка по датам
    trend_data = []
    if assessments:
        current_date = assessments[0].assessment_date.date()
        sum_ugt = 0
        count = 0
        
        for assessment in assessments:
            if assessment.assessment_date.date() != current_date:
                if count > 0:
                    trend_data.append({
                        'date': current_date.isoformat(),
                        'average_ugt': round(sum_ugt / count, 2)
                    })
                current_date = assessment.assessment_date.date()
                sum_ugt = 0
                count = 0
            
            sum_ugt += assessment.ugt_level
            count += 1
        
        # Последняя группа
        if count > 0:
            trend_data.append({
                'date': current_date.isoformat(),
                'average_ugt': round(sum_ugt / count, 2)
            })
    
    return {'trend': trend_data}
