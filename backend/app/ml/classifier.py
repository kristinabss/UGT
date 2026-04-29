import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime
import joblib
import os
from pathlib import Path


class UGTClassifier:
    """
    Классификатор уровня готовности технологий (УГТ).
    Реализует автоматическую классификацию на основе данных о продукции.
    """
    
    # Описание уровней УГТ
    UGT_DESCRIPTIONS = {
        1: "Фундаментальные исследования. Доказаны базовые принципы технологии.",
        2: "Прикладные исследования. Сформулировано практическое применение.",
        3: "Доказательство концепции. Создан лабораторный прототип.",
        4: "Валидация в лабораторных условиях. Прототип прошел испытания.",
        5: "Валидация в промышленной среде. Пилотная установка.",
        6: "Демонстрация в промышленной среде. Рабочий прототип.",
        7: "Демонстрация в реальных условиях. Серийный образец.",
        8: "Технология готова к применению. Полномасштабное производство.",
        9: "Технология применяется серийно. Массовое внедрение."
    }
    
    def __init__(self, model_path: str = None):
        """
        Инициализация классификатора.
        
        Args:
            model_path: Путь к файлу обученной модели
        """
        self.model = None
        self.feature_names = [
            'technical_perfection',
            'stability',
            'production_scale',
            'economic_efficiency'
        ]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Инициализация модели по умолчанию (правила-based)."""
        from sklearn.ensemble import GradientBoostingClassifier
        
        # Создаем простую модель на основе правил
        self.is_trained = False
    
    def load_model(self, model_path: str):
        """Загрузка обученной модели."""
        try:
            self.model = joblib.load(model_path)
            self.is_trained = True
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            self._initialize_default_model()
    
    def save_model(self, model_path: str):
        """Сохранение модели."""
        if self.model:
            joblib.dump(self.model, model_path)
    
    def calculate_indicators(
        self,
        characteristics: List[Dict],
        production_metrics: List[Dict],
        economic_metrics: List[Dict]
    ) -> Dict[str, float]:
        """
        Расчет интегральных показателей.
        
        Args:
            characteristics: Характеристики продукции
            production_metrics: Производственные показатели
            economic_metrics: Экономические показатели
            
        Returns:
            Словарь с рассчитанными показателями
        """
        # Техническое совершенство (на основе характеристик)
        technical_perfection = self._calculate_technical_perfection(characteristics)
        
        # Стабильность характеристик
        stability = self._calculate_stability(production_metrics)
        
        # Масштаб производства
        production_scale = self._calculate_production_scale(production_metrics)
        
        # Экономическая эффективность
        economic_efficiency = self._calculate_economic_efficiency(economic_metrics)
        
        return {
            'technical_perfection': technical_perfection,
            'stability': stability,
            'production_scale': production_scale,
            'economic_efficiency': economic_efficiency
        }
    
    def _calculate_technical_perfection(self, characteristics: List[Dict]) -> float:
        """Расчет показателя технического совершенства (0-100)."""
        if not characteristics:
            return 50.0
        
        # Нормализация и агрегация характеристик
        values = [c.get('value', 0) for c in characteristics if c.get('is_key', False)]
        if not values:
            values = [c.get('value', 0) for c in characteristics]
        
        if not values:
            return 50.0
        
        # Простая нормализация (в реальности нужна отраслевая специфика)
        avg_value = np.mean(values)
        # Нормализуем к шкале 0-100
        return min(100, max(0, avg_value))
    
    def _calculate_stability(self, production_metrics: List[Dict]) -> float:
        """Расчет показателя стабильности (0-100)."""
        if not production_metrics:
            return 50.0
        
        quality_rates = [m.get('quality_rate', 50) for m in production_metrics if m.get('quality_rate')]
        if not quality_rates:
            return 50.0
        
        # Средняя стабильность качества
        avg_quality = np.mean(quality_rates)
        
        # Вариация (чем меньше, тем стабильнее)
        if len(quality_rates) > 1:
            variation = np.std(quality_rates)
            stability_factor = max(0, 1 - variation / 20)  # Нормализация вариации
        else:
            stability_factor = 1.0
        
        return min(100, max(0, avg_quality * stability_factor))
    
    def _calculate_production_scale(self, production_metrics: List[Dict]) -> float:
        """Расчет показателя масштаба производства (0-100)."""
        if not production_metrics:
            return 30.0
        
        volumes = [m.get('production_volume', 0) for m in production_metrics if m.get('production_volume')]
        if not volumes:
            return 30.0
        
        max_volume = max(volumes)
        # Логарифмическая шкала для масштаба
        scale = min(100, 20 * np.log10(max_volume + 1))
        
        return scale
    
    def _calculate_economic_efficiency(self, economic_metrics: List[Dict]) -> float:
        """Расчет показателя экономической эффективности (0-100)."""
        if not economic_metrics:
            return 50.0
        
        # Используем рентабельность или ROI
        efficiencies = []
        for m in economic_metrics:
            if m.get('profit_margin'):
                efficiencies.append(m['profit_margin'])
            elif m.get('roi'):
                efficiencies.append(m['roi'])
        
        if not efficiencies:
            return 50.0
        
        avg_efficiency = np.mean(efficiencies)
        # Нормализация к шкале 0-100
        return min(100, max(0, avg_efficiency))
    
    def predict(
        self,
        indicators: Dict[str, float]
    ) -> Tuple[int, float, Dict]:
        """
        Предсказание уровня УГТ.
        
        Args:
            indicators: Рассчитанные показатели
            
        Returns:
            Кортеж (уровень УГТ, достоверность, вклад факторов)
        """
        # Извлечение признаков
        features = np.array([
            indicators.get('technical_perfection', 50),
            indicators.get('stability', 50),
            indicators.get('production_scale', 30),
            indicators.get('economic_efficiency', 50)
        ]).reshape(1, -1)
        
        if self.model and self.is_trained:
            # Использование обученной модели
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            confidence = float(np.max(probabilities))
            
            # Расчет вклада факторов (упрощенно)
            factor_contributions = {
                'technical_perfection': float(features[0][0] / 100 * 0.3),
                'stability': float(features[0][1] / 100 * 0.25),
                'production_scale': float(features[0][2] / 100 * 0.25),
                'economic_efficiency': float(features[0][3] / 100 * 0.2)
            }
        else:
            # Правило-based классификация
            prediction = self._rule_based_classification(indicators)
            confidence = 0.7  # Достоверность по умолчанию
            
            factor_contributions = {
                'technical_perfection': float(indicators.get('technical_perfection', 50) / 100 * 0.3),
                'stability': float(indicators.get('stability', 50) / 100 * 0.25),
                'production_scale': float(indicators.get('production_scale', 30) / 100 * 0.25),
                'economic_efficiency': float(indicators.get('economic_efficiency', 50) / 100 * 0.2)
            }
        
        ugt_level = int(np.clip(prediction, 1, 9))
        
        return ugt_level, confidence, factor_contributions
    
    def _rule_based_classification(self, indicators: Dict[str, float]) -> int:
        """Классификация на основе правил."""
        tech = indicators.get('technical_perfection', 50)
        stab = indicators.get('stability', 50)
        scale = indicators.get('production_scale', 30)
        econ = indicators.get('economic_efficiency', 50)
        
        # Интегральный показатель
        integral = (tech * 0.3 + stab * 0.25 + scale * 0.25 + econ * 0.2)
        
        # Mapping к уровням УГТ
        if integral < 20:
            return 1
        elif integral < 30:
            return 2
        elif integral < 40:
            return 3
        elif integral < 50:
            return 4
        elif integral < 60:
            return 5
        elif integral < 70:
            return 6
        elif integral < 80:
            return 7
        elif integral < 90:
            return 8
        else:
            return 9
    
    def identify_limiting_factors(
        self,
        indicators: Dict[str, float],
        current_ugt: int
    ) -> List[str]:
        """
        Идентификация ограничивающих факторов.
        
        Args:
            indicators: Рассчитанные показатели
            current_ugt: Текущий уровень УГТ
            
        Returns:
            Список ограничивающих факторов
        """
        factors = []
        
        # Пороговые значения для следующего уровня
        thresholds = {
            'technical_perfection': 60 + current_ugt * 3,
            'stability': 60 + current_ugt * 3,
            'production_scale': 40 + current_ugt * 5,
            'economic_efficiency': 50 + current_ugt * 4
        }
        
        if indicators.get('technical_perfection', 0) < thresholds['technical_perfection']:
            factors.append("Недостаточное техническое совершенство продукции")
        
        if indicators.get('stability', 0) < thresholds['stability']:
            factors.append("Нестабильность характеристик продукции")
        
        if indicators.get('production_scale', 0) < thresholds['production_scale']:
            factors.append("Ограниченный масштаб производства")
        
        if indicators.get('economic_efficiency', 0) < thresholds['economic_efficiency']:
            factors.append("Недостаточная экономическая эффективность")
        
        return factors
    
    def generate_recommendations(
        self,
        limiting_factors: List[str],
        current_ugt: int
    ) -> List[str]:
        """
        Генерация рекомендаций по повышению УГТ.
        
        Args:
            limiting_factors: Ограничивающие факторы
            current_ugt: Текущий уровень УГТ
            
        Returns:
            Список рекомендаций
        """
        recommendations = []
        
        factor_recommendations = {
            "Недостаточное техническое совершенство продукции": [
                "Провести НИОКР по улучшению ключевых характеристик",
                "Внедрить новые материалы или компоненты",
                "Оптимизировать конструкцию изделия"
            ],
            "Нестабильность характеристик продукции": [
                "Внедрить систему статистического контроля качества",
                "Автоматизировать производственные процессы",
                "Провести анализ причин вариаций"
            ],
            "Ограниченный масштаб производства": [
                "Расширить производственные мощности",
                "Оптимизировать производственные процессы",
                "Наладить цепочки поставок"
            ],
            "Недостаточная экономическая эффективность": [
                "Снизить себестоимость производства",
                "Повысить производительность труда",
                "Оптимизировать использование ресурсов"
            ]
        }
        
        for factor in limiting_factors:
            if factor in factor_recommendations:
                recommendations.extend(factor_recommendations[factor][:2])
        
        # Общие рекомендации для уровня
        if current_ugt < 5:
            recommendations.append("Провести дополнительные лабораторные испытания")
        elif current_ugat < 7:
            recommendations.append("Организовать пилотное производство")
        elif current_ugt < 9:
            recommendations.append("Расширить рынок сбыта и увеличить объемы производства")
        
        return list(set(recommendations))[:5]  # Уникальные, максимум 5
    
    def get_ugt_description(self, ugt_level: int) -> str:
        """Получение вербального описания уровня УГТ."""
        return self.UGT_DESCRIPTIONS.get(ugt_level, "Неизвестный уровень")
    
    def forecast_ugt_timeline(
        self,
        current_ugt: int,
        target_ugt: int,
        historical_data: List[Dict]
    ) -> Dict:
        """
        Прогнозирование времени достижения целевого УГТ.
        
        Args:
            current_ugt: Текущий уровень
            target_ugt: Целевой уровень
            historical_data: Исторические данные об оценках
            
        Returns:
            Прогноз с датой достижения и вероятностью
        """
        if current_ugt >= target_ugt:
            return {
                'current_ugt': current_ugt,
                'target_ugt': target_ugt,
                'months_to_target': 0,
                'estimated_date': datetime.now().isoformat(),
                'probability': 1.0
            }
        
        # Анализ темпов роста из исторических данных
        if len(historical_data) >= 2:
            # Расчет среднего темпа роста
            ugt_values = [h['ugt_level'] for h in historical_data]
            time_diffs = [(h['date'] - historical_data[0]['date']).days 
                         for h in historical_data]
            
            if time_diffs[-1] > 0:
                growth_rate = (ugt_values[-1] - ugt_values[0]) / (time_diffs[-1] / 30)  # в месяц
            else:
                growth_rate = 0.5  # По умолчанию
        else:
            growth_rate = 0.5  # По умолчанию: пол-уровня в месяц
        
        # Прогноз
        levels_needed = target_ugt - current_ugt
        months_needed = int(levels_needed / max(0.1, growth_rate))
        
        from datetime import timedelta
        estimated_date = datetime.now() + timedelta(days=months_needed * 30)
        
        # Вероятность (уменьшается с расстоянием)
        probability = max(0.3, 1.0 - (levels_needed * 0.1))
        
        return {
            'current_ugt': current_ugt,
            'target_ugt': target_ugt,
            'months_to_target': months_needed,
            'estimated_date': estimated_date.isoformat(),
            'probability': round(probability, 2),
            'growth_rate_per_month': round(growth_rate, 2)
        }
