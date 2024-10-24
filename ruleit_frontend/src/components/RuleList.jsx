import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid2';
import { Typography, Box, Pagination } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { getRules } from '../services/ruleService';

const RuleList = () => {
    const navigate = useNavigate();
    const [rules, setRules] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageCount, setPageCount] = useState(0);

    useEffect(() => {
        fetchRules(currentPage);
    }, [currentPage]);

    const fetchRules = async (page) => {
        try {
        const response = await getRules(page);
        setRules(response.data.results);
        setPageCount(Math.ceil(response.data.count / 10));
        } catch (error) {
        console.error('Error fetching rules:', error);
        }
    };

    const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
    };

    const handleRuleClick = (index) => {
        navigate('/rule', {
            state: {
              rule_id: rules[index].id,
              rule_name: rules[index].rule_name,
              rule_root_id: rules[index].rule_root,
              rule_tokens: rules[index].rule_tokens,
            },
        });
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography variant="h4" gutterBottom marginTop={3}>
                All Rules
            </Typography>
            
            <Grid container spacing={2} style={{ width: '700px'}}> 
                {rules.map((rule, index) => (
                    <Grid 
                        item xs={12} 
                        key={index} 
                        size={"grow"} 
                        onClick={() => handleRuleClick(index)}
                        sx={{cursor:'pointer'}}
                    >
                    <Box
                    sx={{
                        p: 2,
                        border: '1px solid #ccc',
                        borderRadius: 2,
                        boxShadow: 1,
                        backgroundColor: '#f9f9f9',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'space-between',
                        alignItems: 'flex-start',
                    }}
                    >
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                        <Typography variant="body2" sx={{fontSize:'1rem'}} >
                        Rule Name: {rule.rule_name}
                        </Typography>
                        <Typography variant="body2" sx={{fontSize:'1rem'}} >
                        Rule ID: {rule.id}
                        </Typography>
                        <Typography variant="body2" sx={{fontSize:'1rem'}} >
                        Root ID: {rule.rule_root}
                        </Typography>
                    </Box>
                    <Box sx={{ width: '100%', borderBottom: '1px solid #ccc', my: 1 }} />
                    <Typography
                        variant="body1"
                        sx={{
                        mt: 1,
                        textAlign: 'center',
                        overflowWrap: 'break-word',
                        whiteSpace: 'normal',
                        width: '100%',
                        }}
                    >
                        <strong>{rule.rule_tokens.join(' ')}</strong>
                    </Typography>
                    </Box>
                </Grid>
                
                ))}
            </Grid>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Pagination
                    count={pageCount}
                    page={currentPage}
                    onChange={(event, value) => handlePageChange(value)}
                    color="primary"
                />
            </Box>
        </div>
    );
};

export default RuleList;
