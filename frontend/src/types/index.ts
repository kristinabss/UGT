// Типы для системы УГТ

export interface Technology {
  id: number;
  name: string;
  description?: string;
  industry_id: number;
  enterprise_id?: number;
  current_ugt?: number;
  created_at: string;
  updated_at?: string;
  industry?: Industry;
  enterprise?: Enterprise;
}

export interface Industry {
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface Enterprise {
  id: number;
  name: string;
  industry_id: number;
  description?: string;
  created_at: string;
  industry?: Industry;
}

export interface Product {
  id: number;
  name: string;
  technology_id: number;
  enterprise_id: number;
  product_type?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
  technology?: Technology;
  enterprise?: Enterprise;
}

export interface ProductCharacteristic {
  id?: number;
  product_id: number;
  characteristic_name: string;
  value: number;
  unit?: string;
  is_key?: boolean;
  created_at?: string;
}

export interface ProductionMetric {
  id?: number;
  product_id: number;
  metric_date: string;
  production_volume?: number;
  quality_rate?: number;
  defect_rate?: number;
  capacity_utilization?: number;
  created_at?: string;
}

export interface EconomicMetric {
  id?: number;
  product_id: number;
  metric_date: string;
  cost_price?: number;
  selling_price?: number;
  profit_margin?: number;
  roi?: number;
  created_at?: string;
}

export interface UGTAssessment {
  id?: number;
  technology_id: number;
  assessment_date: string;
  ugt_level: number;
  confidence_score?: number;
  technical_perfection?: number;
  stability?: number;
  production_scale?: number;
  economic_efficiency?: number;
  limiting_factors?: string;
  recommendations?: string;
  created_at?: string;
  technology?: Technology;
}

export interface UGTAssessmentResult {
  ugt_level: number;
  ugt_description: string;
  confidence_score: number;
  technical_perfection: number;
  stability: number;
  production_scale: number;
  economic_efficiency: number;
  limiting_factors: string[];
  recommendations: string[];
  factor_contributions: Record<string, number>;
}

export interface DashboardStats {
  total_technologies: number;
  average_ugt: number;
  ready_for_implementation: number;
  ugt_distribution: Record<string, number>;
  ugt_trend: Array<{ date: string; average_ugt: number }>;
  priority_technologies: Technology[];
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  enterprise_id?: number;
  is_active: boolean;
  created_at: string;
}
