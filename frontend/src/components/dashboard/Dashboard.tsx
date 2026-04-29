import React, { useEffect, useState } from 'react';
import { Card, Col, Row, Statistic, Table, Typography } from 'antd';
import Plot from 'react-plotly.js';
import { DashboardStats, Technology } from '../../types';
import { dashboardApi } from '../../services';

const { Title } = Typography;

const UGT_DESCRIPTIONS: Record<number, string> = {
  1: 'Фундаментальные исследования',
  2: 'Прикладные исследования',
  3: 'Доказательство концепции',
  4: 'Валидация в лаборатории',
  5: 'Валидация в пром. среде',
  6: 'Демонстрация в пром. среде',
  7: 'Демонстрация в реальных условиях',
  8: 'Готово к применению',
  9: 'Серийное применение'
};

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await dashboardApi.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Ошибка загрузки статистики:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return <div>Загрузка...</div>;
  }

  // Данные для диаграммы распределения УГТ
  const ugtDistributionData = {
    x: Object.keys(stats.ugt_distribution),
    y: Object.values(stats.ugt_distribution),
    type: 'bar' as const,
    marker: { color: '#1890ff' },
    name: 'Количество технологий'
  };

  // Данные для графика динамики
  const trendData = {
    x: stats.ugt_trend.map(t => t.date),
    y: stats.ugt_trend.map(t => t.average_ugt),
    type: 'scatter' as const,
    mode: 'lines+markers',
    marker: { color: '#52c41a' },
    name: 'Средний УГТ'
  };

  // Колонки таблицы приоритетных технологий
  const columns = [
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'УГТ',
      dataIndex: 'current_ugt',
      key: 'current_ugt',
      render: (ugt: number) => (
        <span style={{ 
          fontWeight: 'bold',
          color: ugt >= 7 ? '#52c41a' : ugt >= 4 ? '#faad14' : '#ff4d4f'
        }}>
          {ugt} - {UGT_DESCRIPTIONS[ugt]}
        </span>
      ),
    },
    {
      title: 'Отрасль',
      dataIndex: ['industry', 'name'],
      key: 'industry',
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Дашборд системы УГТ</Title>
      
      {/* KPI карточки */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Всего технологий"
              value={stats.total_technologies}
              suffix="шт."
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Средний УГТ"
              value={stats.average_ugt}
              precision={2}
              suffix="/ 9"
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Готовы к внедрению"
              value={stats.ready_for_implementation}
              suffix="шт."
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Графики */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="Распределение технологий по уровням УГТ">
            <Plot
              data={[ugtDistributionData]}
              layout={{
                width: undefined,
                height: 300,
                title: '',
                xaxis: { title: 'Уровень УГТ' },
                yaxis: { title: 'Количество' },
                margin: { t: 20, b: 40, l: 40, r: 20 }
              }}
              config={{ responsive: true, displayModeBar: false }}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Динамика среднего УГТ">
            <Plot
              data={[trendData]}
              layout={{
                width: undefined,
                height: 300,
                title: '',
                xaxis: { title: 'Дата' },
                yaxis: { title: 'Средний УГТ', range: [0, 9] },
                margin: { t: 20, b: 40, l: 40, r: 20 }
              }}
              config={{ responsive: true, displayModeBar: false }}
            />
          </Card>
        </Col>
      </Row>

      {/* Приоритетные технологии */}
      <Card title="Приоритетные технологии">
        <Table
          columns={columns}
          dataSource={stats.priority_technologies}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
};
