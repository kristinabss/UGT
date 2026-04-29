from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.entities import Product, ProductCharacteristic, ProductionMetric, EconomicMetric
from ..schemas.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductCharacteristicCreate, ProductCharacteristicUpdate, ProductCharacteristicResponse,
    ProductionMetricCreate, ProductionMetricUpdate, ProductionMetricResponse,
    EconomicMetricCreate, EconomicMetricUpdate, EconomicMetricResponse
)

router = APIRouter(prefix="/products", tags=["Продукция"])


@router.get("", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    technology_id: int = None,
    enterprise_id: int = None,
    db: Session = Depends(get_db)
):
    """Получение списка продукции с фильтрацией."""
    query = db.query(Product)
    
    if technology_id:
        query = query.filter(Product.technology_id == technology_id)
    if enterprise_id:
        query = query.filter(Product.enterprise_id == enterprise_id)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получение информации о продукции по ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукция не найдена")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Создание новой записи о продукции."""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Обновление информации о продукции."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукция не найдена")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Удаление записи о продукции."""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукция не найдена")
    
    db.delete(db_product)
    db.commit()
    return None


# Характеристики продукции
@router.get("/{product_id}/characteristics", response_model=List[ProductCharacteristicResponse])
def get_product_characteristics(product_id: int, db: Session = Depends(get_db)):
    """Получение характеристик продукции."""
    characteristics = db.query(ProductCharacteristic)\
        .filter(ProductCharacteristic.product_id == product_id)\
        .all()
    return characteristics


@router.post("/{product_id}/characteristics", response_model=ProductCharacteristicResponse)
def create_product_characteristic(
    product_id: int,
    characteristic: ProductCharacteristicCreate,
    db: Session = Depends(get_db)
):
    """Добавление характеристики продукции."""
    db_characteristic = ProductCharacteristic(
        **characteristic.model_dump(),
        product_id=product_id
    )
    db.add(db_characteristic)
    db.commit()
    db.refresh(db_characteristic)
    return db_characteristic


# Производственные показатели
@router.get("/{product_id}/production-metrics", response_model=List[ProductionMetricResponse])
def get_production_metrics(product_id: int, db: Session = Depends(get_db)):
    """Получение производственных показателей."""
    metrics = db.query(ProductionMetric)\
        .filter(ProductionMetric.product_id == product_id)\
        .order_by(ProductionMetric.metric_date.desc())\
        .all()
    return metrics


@router.post("/{product_id}/production-metrics", response_model=ProductionMetricResponse)
def create_production_metric(
    product_id: int,
    metric: ProductionMetricCreate,
    db: Session = Depends(get_db)
):
    """Добавление производственного показателя."""
    db_metric = ProductionMetric(
        **metric.model_dump(),
        product_id=product_id
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


# Экономические показатели
@router.get("/{product_id}/economic-metrics", response_model=List[EconomicMetricResponse])
def get_economic_metrics(product_id: int, db: Session = Depends(get_db)):
    """Получение экономических показателей."""
    metrics = db.query(EconomicMetric)\
        .filter(EconomicMetric.product_id == product_id)\
        .order_by(EconomicMetric.metric_date.desc())\
        .all()
    return metrics


@router.post("/{product_id}/economic-metrics", response_model=EconomicMetricResponse)
def create_economic_metric(
    product_id: int,
    metric: EconomicMetricCreate,
    db: Session = Depends(get_db)
):
    """Добавление экономического показателя."""
    db_metric = EconomicMetric(
        **metric.model_dump(),
        product_id=product_id
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric
