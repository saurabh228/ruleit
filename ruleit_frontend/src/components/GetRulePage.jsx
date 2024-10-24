import React, { useState } from 'react';
import axios from 'axios';
import Grid from '@mui/material/Grid2'; // Ensure you have the correct import
import { Box, Button, Typography, TextField } from '@mui/material';
import { getRule } from '../services/ruleService'; 
import { useNavigate } from 'react-router-dom';


const GetRulePage = () => {
  const navigate = useNavigate();
  const [ruleId, setRuleId] = useState('');
  const [error, setError] = useState(null);


  const handleFetchRule = async () => {
    try {
      const response = await getRule(ruleId);
      setError(null);
      console.log(response);
      navigate('/rule', {
        state: {
          rule_id: response.data.id,
          rule_name: response.data.rule_name,
          rule_root_id: response.data.rule_root,
          rule_tokens: response.data.rule_tokens,
        },
    });
    } catch (err) {
      setError('Rule not found or an error occurred');
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Fetch Rule by ID
      </Typography>
      
      <Grid container spacing={2} alignItems="center">
        <Grid xs={8}>
          <TextField
            label="Enter Rule ID"
            variant="outlined"
            fullWidth
            value={ruleId}
            onChange={(e) => setRuleId(e.target.value)}
          />
        </Grid>
        <Grid xs={4}>
          <Button variant="contained" color="primary" onClick={handleFetchRule} disabled ={ruleId.trim()===''}>
            Get Rule
          </Button>
        </Grid>
      </Grid>

      {error && <Typography color="error" mt={2}>{error}</Typography>}
      
    </Box>
  );
};

export default GetRulePage;
