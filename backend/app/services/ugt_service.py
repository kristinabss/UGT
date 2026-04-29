from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from ..models.entities import Technology, UGTAssessment, Product
from ..schemas.schemas import DashboardStats, TechnologyResponse
from ..ml.classifier import UGTClassifier


class UGTService:
    """Сервис для работы с оценками УГТ."""
    
    def __init__(self, db: Session):
        self.db = db
        self.classifier = UGTClassifier()
    
    def perform_assessment(
        self,
        technology_id: int,
        characteristics: List[Dict],
        production_metrics: List[Dict],
        economic_metrics: List[Dict],
        classifier: UGTClassifier = None
    ) -> Dict:
        """
        Выполнение оценки УГТ технологии.
        
        Args:
            technology_id: ID технологии
            characteristics: Характеристики продукции
            production_metrics: Производственные показатели
            economic_metrics: Экономические показатели
            classifier: Классификатор (опционально)
            
        Returns:
            Результаты оценки
        """
        if classifier is None:
            classifier = self.classifier
        
        # Расчет интегральных показателей
        indicators = classifier.calculate_indicators(
            characteristics=characteristics,
            production_metrics=production_metrics,
            economic_metrics=economic_metrics
        )
        
        # Предсказание уровня УГТ
        ugt_level, confidence, factor_contributions = classifier.predict(indicators)
        
        # Получение описания уровня
        ugt_description = classifier.get_ugt_description(ugt_level)
        
        # Идентификация ограничивающих факторов
        limiting_factors = classifier.identify_limiting_factors(indicators, ugt_level)
        
        # Генерация рекомендаций
        recommendations = classifier.generate_recommendations(limiting_factors, ugt_level)
        
        # Сохранение оценки в базу данных
        assessment = UGTAssessment(
            technology_id=technology_id,
            ugt_level=ugt_level,
            confidence_score=confidence,
            technical_perfection=indicators['technical_perfection'],
            stability=indicators['stability'],
            production_scale=indicators['production_scale'],
            economic_efficiency=indicators['economic_efficiency'],
            limiting_factors=str(limiting_factors),
            recommendations=str(recommendations)
        )
        
        self.db.add(assessment)
        
        # Обновление текущего УГТ технологии
        technology = self.db.query(Technology).filter(Technology.id == technology_id).first()
        if technology:
            technology.current_ugt = ugt_level
        
        self.db.commit()
        self.db.refresh(assessment)
        
        return {
            'ugt_level': ugt_level,
            'ugt_description': ugt_description,
            'confidence_score': confidence,
            'technical_perfection': indicators['technical_perfection'],
            'stability': indicators['stability'],
            'production_scale': indicators['production_scale'],
            'economic_efficiency': indicators['economic_efficiency'],
            'limiting_factors': limiting_factors,
            'recommendations': recommendations,
            'factor_contributions': factor_contributions
        }
    
    def get_dashboard_stats(self) -> DashboardStats:
        """Получение статистики для дашборда."""
        # Общее количество технологий
        total_technologies = self.db.query(Technology).count()
        
        # Средний УГТ
        avg_ugt_result = self.db.query(
            Technology.current_ugt
        ).filter(Technology.current_ugt.isnot(None)).all()
        
        if avg_ugt_result:
            average_ugt = sum([t[0] for t in avg_ugt_result]) / len(avg_ugt_result)
        else:
            average_ugt = 0.0
        
        # Количество технологий, готовых к внедрению (УГТ >= 7)
        ready_for_implementation = self.db.query(Technology)\
            .filter(Technology.current_ugt >= 7)\
            .count()
        
        # Распределение по уровням УГТ
        ugt_distribution = {}
        for level in range(1, 10):
            count = self.db.query(Technology)\
                .filter(Technology.current_ugt == level)\
                .count()
            ugt_distribution[str(level)] = count
        
        # Динамика УГТ (последние 5 оценок)
        recent_assessments = self.db.query(UGTAssessment)\
            .order_by(UGTAssessment.assessment_date.desc())\
            .limit(5)\
            .all()
        
        ugt_trend = [
            {
                'date': a.assessment_date.isoformat(),
                'average_ugt': a.ugt_level
            }
            for a in recent_assessments
        ]
        
        # Приоритетные технологии (с высоким УГТ или недавно обновленные)
        priority_technologies = self.db.query(Technology)\
            .filter(Technology.current_ugt.isnot(None))\
            .order_by(Technology.current_ugt.desc(), Technology.updated_at.desc())\
            .limit(5)\
            .all()
        
        return DashboardStats(
            total_technologies=total_technologies,
            average_ugt=round(average_ugt, 2),
            ready_for_implementation=ready_for_implementation,
            ugt_distribution=ugt_distribution,
            ugt_trend=ugt_trend,
            priority_technologies=priority_technologies
        )
    
    def forecast_ugt_timeline(
        self,
        technology_id: int,
        target_ugt: int = 9
    ) -> Dict:
        """
        Прогнозирование времени достижения целевого УГТ.
        
        Args:
            technology_id: ID технологии
            target_ugt: Целевой уровень УГТ
            
        Returns:
            Прогноз с датой достижения
        """
        # Получение технологии
        technology = self.db.query(Technology)\
            .filter(Technology.id == technology_id)\
            .first()
        
        if not technology:
            return {'error': 'Технология не найдена'}
        
        current_ugt = technology.current_ugt or 1
        
        # Получение исторических данных об оценках
        historical_assessments = self.db.query(UGTAssessment)\
            .filter(UGTAssessment.technology_id == technology_id)\
            .order_by(UGTAssessment.assessment_date)\
            .all()
        
        historical_data = [
            {
                'date': a.assessment_date,
                'ugt_level': a.ugt_level
            }
            for a in historical_assessments
        ]
        
        # Прогнозирование
        forecast = self.classifier.forecast_ugt_timeline(
            current_ugt=current_ugt,
            target_ugt=target_ugt,
            historical_data=historical_data
        )
        
        return forecast
