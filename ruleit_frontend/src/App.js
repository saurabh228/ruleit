import React from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import CreateRulePage from './components/CreateRulePage';
import RulePage from './components/RulePage';
import RuleList from './components/RuleList';
import GetRulePage from './components/GetRulePage';
import theme from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create-rule" element={<CreateRulePage />} />
          <Route path="/rule" element={<RulePage />} />
          <Route path="/rules" element={<RuleList />} />
          <Route path="/get-rule" element={<GetRulePage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
