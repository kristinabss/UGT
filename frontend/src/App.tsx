import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, theme } from 'antd';
import { Dashboard } from './components/dashboard';

const { Header, Content, Sider } = Layout;

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider breakpoint="lg" collapsedWidth="80">
          <div style={{ 
            height: 32, 
            margin: 16, 
            background: 'rgba(255, 255, 255, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold'
          }}>
            УГТ Система
          </div>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1">
              <Link to="/">Дашборд</Link>
            </Menu.Item>
            <Menu.Item key="2">
              <Link to="/technologies">Технологии</Link>
            </Menu.Item>
            <Menu.Item key="3">
              <Link to="/products">Продукция</Link>
            </Menu.Item>
            <Menu.Item key="4">
              <Link to="/assessment">Оценка УГТ</Link>
            </Menu.Item>
            <Menu.Item key="5">
              <Link to="/reports">Отчеты</Link>
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout>
          <Header style={{ padding: '0 16px', background: colorBgContainer }}>
            <h2 style={{ margin: 0, lineHeight: '64px' }}>Система определения УГТ</h2>
          </Header>
          <Content style={{ margin: '16px' }}>
            <div
              style={{
                padding: 24,
                minHeight: 360,
                background: colorBgContainer,
                borderRadius: borderRadiusLG,
              }}
            >
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/technologies" element={<div>Раздел Технологии</div>} />
                <Route path="/products" element={<div>Раздел Продукция</div>} />
                <Route path="/assessment" element={<div>Раздел Оценка УГТ</div>} />
                <Route path="/reports" element={<div>Раздел Отчеты</div>} />
              </Routes>
            </div>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App;
