from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Industry(Base):
    """Отрасль промышленности."""
    __tablename__ = "industries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    enterprises = relationship("Enterprise", back_populates="industry")
    technologies = relationship("Technology", back_populates="industry")


class Enterprise(Base):
    """Предприятие."""
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    industry = relationship("Industry", back_populates="enterprises")
    products = relationship("Product", back_populates="enterprise")
    technologies = relationship("Technology", back_populates="enterprise")


class Technology(Base):
    """Технология."""
    __tablename__ = "technologies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=False)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=True)
    current_ugt = Column(Integer, nullable=True)  # Текущий уровень УГТ (1-9)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    industry = relationship("Industry", back_populates="technologies")
    enterprise = relationship("Enterprise", back_populates="technologies")
    products = relationship("Product", back_populates="technology")
    ugt_assessments = relationship("UGTAssessment", back_populates="technology")


class Product(Base):
    """Продукт/Изделие."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=False)
    product_type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    technology = relationship("Technology", back_populates="products")
    enterprise = relationship("Enterprise", back_populates="products")
    characteristics = relationship("ProductCharacteristic", back_populates="product", cascade="all, delete-orphan")
    production_metrics = relationship("ProductionMetric", back_populates="product", cascade="all, delete-orphan")
    economic_metrics = relationship("EconomicMetric", back_populates="product", cascade="all, delete-orphan")


class ProductCharacteristic(Base):
    """Характеристики продукта."""
    __tablename__ = "product_characteristics"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    characteristic_name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    is_key = Column(Boolean, default=False)  # Ключевая характеристика
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    product = relationship("Product", back_populates="characteristics")


class ProductionMetric(Base):
    """Производственные показатели."""
    __tablename__ = "production_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    metric_date = Column(DateTime, nullable=False)
    production_volume = Column(Float, nullable=True)  # Объем производства
    quality_rate = Column(Float, nullable=True)  # Показатель качества (%)
    defect_rate = Column(Float, nullable=True)  # Процент брака
    capacity_utilization = Column(Float, nullable=True)  # Загрузка мощностей (%)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    product = relationship("Product", back_populates="production_metrics")


class EconomicMetric(Base):
    """Экономические показатели."""
    __tablename__ = "economic_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    metric_date = Column(DateTime, nullable=False)
    cost_price = Column(Float, nullable=True)  # Себестоимость
    selling_price = Column(Float, nullable=True)  # Цена продажи
    profit_margin = Column(Float, nullable=True)  # Рентабельность (%)
    roi = Column(Float, nullable=True)  # ROI (%)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    product = relationship("Product", back_populates="economic_metrics")


class UGTAssessment(Base):
    """Оценка УГТ."""
    __tablename__ = "ugt_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    ugt_level = Column(Integer, nullable=False)  # Уровень УГТ (1-9)
    confidence_score = Column(Float, nullable=True)  # Достоверность оценки
    technical_perfection = Column(Float, nullable=True)  # Техническое совершенство
    stability = Column(Float, nullable=True)  # Стабильность характеристик
    production_scale = Column(Float, nullable=True)  # Масштаб производства
    economic_efficiency = Column(Float, nullable=True)  # Экономическая эффективность
    limiting_factors = Column(Text, nullable=True)  # Ограничивающие факторы (JSON)
    recommendations = Column(Text, nullable=True)  # Рекомендации
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    technology = relationship("Technology", back_populates="ugt_assessments")


class User(Base):
    """Пользователь системы."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user")  # user, analyst, admin
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    enterprise = relationship("Enterprise")
