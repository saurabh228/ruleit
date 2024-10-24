import React, { useState, useEffect, useRef } from 'react';
import { Container, Typography, Grid2, Card, CardContent, Button, Box } from '@mui/material';
import { Create, ListAlt, Visibility, Assessment } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';


const HomePage = () => {


  const navigate = useNavigate();

  const handleCreateRuleClick = () => {
    navigate('/create-rule');
  };
  const handleGetRuleClick = () => {
    navigate('/get-rule');
  };
  const handleViewAllRulesClick = () => {
    navigate('/rules');
  }

  return (
    <Container maxWidth="md" sx={{ textAlign: 'center', mt: 5 }}>
      {/* Page Title */}
      <Typography variant="h3" gutterBottom>
        RuleIt - Rule Engine
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
        Manage, evaluate, and explore rules with ease.
      </Typography>

      {/* Main Content */}
      <Grid2 container spacing={4} sx={{ mt: 3, justifyContent: 'center' }}>
        {/* Create Rule */}
        <Grid2 item xs={12} sm={6} md={6}>
          <Card sx={{ backgroundColor: '#f5f5f5', boxShadow: 3, width: '220px' }}>
            <CardContent>
              <Box mb={2}>
                <Create fontSize="large" color="primary" />
              </Box>
              <Typography variant="h5">Create New Rule</Typography>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
                onClick={handleCreateRuleClick}
              >
                Create Rule
              </Button>
            </CardContent>
          </Card>
        </Grid2>

        {/* View a Rule */}
        <Grid2 item xs={12} sm={6} md={6}>
          <Card sx={{ backgroundColor: '#f5f5f5', boxShadow: 3, width: '220px' }}>
            <CardContent>
              <Box mb={2}>
                <Visibility fontSize="large" color="primary" />
              </Box>
              <Typography variant="h5">View a Rule</Typography>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
                onClick={handleGetRuleClick}
              >
                View Rule
              </Button>
            </CardContent>
          </Card>
        </Grid2>

        {/* View All Rules */}
        <Grid2 item xs={12} sm={6} md={6}>
          <Card sx={{ backgroundColor: '#f5f5f5', boxShadow: 3, width: '220px' }}>
            <CardContent>
              <Box mb={2}>
                <ListAlt fontSize="large" color="primary" />
              </Box>
              <Typography variant="h5">View All Rules</Typography>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
                onClick={handleViewAllRulesClick}
              >
                All Rules
              </Button>
            </CardContent>
          </Card>
        </Grid2>

        {/* Evaluate Rule */}
        <Grid2 item xs={12} sm={6} md={6}>
          <Card sx={{ backgroundColor: '#f5f5f5', boxShadow: 3, width: '220px' }}>
            <CardContent>
              <Box mb={2}>
                <Assessment fontSize="large" color="secondary" />
              </Box>
              <Typography variant="h5">Evaluate Rule</Typography>
              <Button
                variant="contained"
                color="secondary"
                fullWidth
                sx={{ mt: 2 }}
                onClick={handleGetRuleClick}
              >
                Evaluate Rule
              </Button>
            </CardContent>
          </Card>
        </Grid2>
      </Grid2>

    
    </Container>
  );
};

export default HomePage;
