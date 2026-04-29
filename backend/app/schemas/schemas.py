from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# Базовые схемы
class BaseSchema(BaseModel):
    """Базовая схема с общими полями."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Отрасли
class IndustryBase(BaseModel):
    name: str
    description: Optional[str] = None


class IndustryCreate(IndustryBase):
    pass


class IndustryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class IndustryResponse(IndustryBase, BaseSchema):
    pass


# Предприятия
class EnterpriseBase(BaseModel):
    name: str
    industry_id: int
    description: Optional[str] = None


class EnterpriseCreate(EnterpriseBase):
    pass


class EnterpriseUpdate(BaseModel):
    name: Optional[str] = None
    industry_id: Optional[int] = None
    description: Optional[str] = None


class EnterpriseResponse(EnterpriseBase, BaseSchema):
    industry: Optional[IndustryResponse] = None


# Технологии
class TechnologyBase(BaseModel):
    name: str
    description: Optional[str] = None
    industry_id: int
    enterprise_id: Optional[int] = None


class TechnologyCreate(TechnologyBase):
    pass


class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry_id: Optional[int] = None
    enterprise_id: Optional[int] = None
    current_ugt: Optional[int] = Field(None, ge=1, le=9)


class TechnologyResponse(TechnologyBase, BaseSchema):
    current_ugt: Optional[int] = None
    updated_at: Optional[datetime] = None
    industry: Optional[IndustryResponse] = None
    enterprise: Optional[EnterpriseResponse] = None


# Продукция
class ProductBase(BaseModel):
    name: str
    technology_id: int
    enterprise_id: int
    product_type: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    technology_id: Optional[int] = None
    enterprise_id: Optional[int] = None
    product_type: Optional[str] = None
    description: Optional[str] = None


class ProductResponse(ProductBase, BaseSchema):
    updated_at: Optional[datetime] = None
    technology: Optional[TechnologyResponse] = None
    enterprise: Optional[EnterpriseResponse] = None


# Характеристики продукта
class ProductCharacteristicBase(BaseModel):
    characteristic_name: str
    value: float
    unit: Optional[str] = None
    is_key: bool = False


class ProductCharacteristicCreate(ProductCharacteristicBase):
    product_id: int


class ProductCharacteristicUpdate(BaseModel):
    characteristic_name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    is_key: Optional[bool] = None


class ProductCharacteristicResponse(ProductCharacteristicBase, BaseSchema):
    product_id: int


# Производственные показатели
class ProductionMetricBase(BaseModel):
    metric_date: datetime
    production_volume: Optional[float] = None
    quality_rate: Optional[float] = Field(None, ge=0, le=100)
    defect_rate: Optional[float] = Field(None, ge=0, le=100)
    capacity_utilization: Optional[float] = Field(None, ge=0, le=100)


class ProductionMetricCreate(ProductionMetricBase):
    product_id: int


class ProductionMetricUpdate(BaseModel):
    production_volume: Optional[float] = None
    quality_rate: Optional[float] = None
    defect_rate: Optional[float] = None
    capacity_utilization: Optional[float] = None


class ProductionMetricResponse(ProductionMetricBase, BaseSchema):
    product_id: int


# Экономические показатели
class EconomicMetricBase(BaseModel):
    metric_date: datetime
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    profit_margin: Optional[float] = None
    roi: Optional[float] = None


class EconomicMetricCreate(EconomicMetricBase):
    product_id: int


class EconomicMetricUpdate(BaseModel):
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    profit_margin: Optional[float] = None
    roi: Optional[float] = None


class EconomicMetricResponse(EconomicMetricBase, BaseSchema):
    product_id: int


# Оценка УГТ
class UGTAssessmentBase(BaseModel):
    ugt_level: int = Field(ge=1, le=9)
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    technical_perfection: Optional[float] = None
    stability: Optional[float] = None
    production_scale: Optional[float] = None
    economic_efficiency: Optional[float] = None
    limiting_factors: Optional[str] = None
    recommendations: Optional[str] = None


class UGTAssessmentCreate(UGTAssessmentBase):
    technology_id: int


class UGTAssessmentUpdate(BaseModel):
    ugt_level: Optional[int] = Field(None, ge=1, le=9)
    confidence_score: Optional[float] = None
    technical_perfection: Optional[float] = None
    stability: Optional[float] = None
    production_scale: Optional[float] = None
    economic_efficiency: Optional[float] = None
    limiting_factors: Optional[str] = None
    recommendations: Optional[str] = None


class UGTAssessmentResponse(UGTAssessmentBase, BaseSchema):
    technology_id: int
    assessment_date: datetime
    technology: Optional[TechnologyResponse] = None


# Пользователи
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "user"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase, BaseSchema):
    is_active: bool
    enterprise_id: Optional[int] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Запрос оценки УГТ
class UGTAssessmentRequest(BaseModel):
    """Запрос на оценку УГТ с данными о продукции."""
    technology_id: int
    characteristics: List[ProductCharacteristicCreate] = []
    production_metrics: List[ProductionMetricCreate] = []
    economic_metrics: List[EconomicMetricCreate] = []


# Ответ с результатами оценки
class UGTAssessmentResult(BaseModel):
    """Результаты оценки УГТ."""
    ugt_level: int
    ugt_description: str
    confidence_score: float
    technical_perfection: float
    stability: float
    production_scale: float
    economic_efficiency: float
    limiting_factors: List[str]
    recommendations: List[str]
    factor_contributions: dict


# Дашборд
class DashboardStats(BaseModel):
    """Статистика для дашборда."""
    total_technologies: int
    average_ugt: float
    ready_for_implementation: int
    ugt_distribution: dict
    ugt_trend: List[dict]
    priority_technologies: List[TechnologyResponse]
