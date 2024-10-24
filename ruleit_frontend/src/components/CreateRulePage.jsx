import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  TextField,
  Typography,
  IconButton,
  Select,
  MenuItem,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import Grid from '@mui/material/Grid2';
import { createRule, combineRules } from '../services/ruleService';
import { useNavigate } from 'react-router-dom';


const CreateRulePage = () => {
    const navigate = useNavigate();
    const [rules, setRules] = useState([{ rule: '', operator: '' }]);
    const operators = ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR'];
    const [ruleName, setRuleName] = useState('');
    

    const handleRuleChange = (index, value) => {
        const newRules = [...rules];
        newRules[index].rule = value;
        setRules(newRules);
    };

    const handleOperatorChange = (index, value) => {
        const newRules = [...rules];
        newRules[index].operator = value;
        setRules(newRules);
    };

    const addRule = () => {
        setRules([...rules, { rule: '', operator: 'AND' }]);
    };

    const deleteRule = (index) => {
        const newRules = rules.filter((_, i) => i !== index);
        setRules(newRules);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const ruleStrings = rules.map(r => r.rule);
        const operators = rules.slice(1).map(r => r.operator);

        try {
            let response;
            if (rules.length === 1) {
                response = await createRule({ rule_name: ruleName, rule_string: ruleStrings[0] });
                console.log('Rule created:', response.data);
            }else{
                response = await combineRules({ rule_name: ruleName, rule_strings: ruleStrings, operators: operators });
                console.log('Rule created:', response.data);
            }
            
            alert('Rule created successfully!');
            setRules([{ rule: '', operator: '' }]);
            setRuleName('');
            navigate('/rule', {
                state: {
                  rule_id: response.data.rule_id,
                  rule_name: response.data.rule_name,
                  rule_root_id: response.data.rule_root_id,
                  rule_tokens: response.data.rule_tokens,
                },
            });
        } catch (error) {
            console.error('Error creating rule:', error);
            alert('Failed to create rule.');
        }
    };

    return (
        <Box sx={{ p: 3, display: 'flex', justifyContent: 'center' }}>
          <Box sx={{ width: '100%', maxWidth: 600 }}>
            <Typography variant="h4" gutterBottom textAlign="center">Create Rule</Typography>
            <form onSubmit={handleSubmit} >
              <Grid container spacing={2} sx={{ mb: 3,  width:'100%' }} >
                <Grid item xs={12} sx={{ width:'100%'}}>
                  <TextField
                    label="Rule Name"
                    variant="outlined"
                    fullWidth
                    value={ruleName}
                    onChange={(e) => setRuleName(e.target.value)}
                    required
                  />
                </Grid>
              </Grid>
              {rules.map((rule, index) => (
                <Grid container spacing={2} alignItems="center" key={index} sx={{ mb: 2 }} justifyContent="space-between">
                  {index > 0 && (
                    <Grid item xs={12} sm={3}>
                      <Select
                        value={rule.operator}
                        onChange={(e) => handleOperatorChange(index, e.target.value)}
                        required
                        variant="outlined"
                        fullWidth
                      >
                        {operators.map((op) => (
                          <MenuItem key={op} value={op}>{op}</MenuItem>
                        ))}
                      </Select>
                    </Grid>
                  )}
                  <Grid item xs={14} sm={index > 0 ? 7 : 10} size="grow">
                    <TextField
                      label={`Rule ${index + 1}`}
                      variant="outlined"
                      fullWidth
                      value={rule.rule}
                      onChange={(e) => handleRuleChange(index, e.target.value)}
                      required
                    />
                  </Grid>
                  {index > 0 && (
                    <Grid item xs={12} sm={2}>
                      <IconButton onClick={() => deleteRule(index)} color="error">
                        <DeleteIcon />
                      </IconButton>
                    </Grid>
                  )}
                </Grid>
              ))}
              <Grid container spacing={2} justifyContent="center">
                <Grid item>
                  <Button variant="outlined" onClick={addRule}>
                    Combine Another Rule
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained" type="submit">
                    Submit Rule
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Box>
        </Box>
      );
};

export default CreateRulePage;