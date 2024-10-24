import React, {useState, useEffect, useRef} from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { TextField, Box, Typography, Button } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { editRule, evaluateRule } from '../services/ruleService';

const RulePage = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const { rule_id, rule_name, rule_root_id, rule_tokens } = location.state || {};

    const [jsonData, setJsonData] = useState('{\n : \n}');
    const [evalationResult, setEvalationResult] = useState(false);
    const [showEvalationResult, setShowEvalationResult] = useState(false);

    const [tokens, setTokens] = useState([]);
    const [editingIndex, setEditingIndex] = useState(-1);
    const [inputValues, setInputValues] = useState([]);
    const spanRefs = useRef([]);
    const tokenRefs = useRef([]);

    const handleTokenClick = (index) => {
        setEditingIndex(index);
    };
    
    const handleTokenInputChange = (e, index) => {
        const updatedTokens = [...tokens];
        updatedTokens[index] = e.target.value;
        setTokens(updatedTokens);
    };
    
    const handleTokenInputBlur = (index) => {
        if (editingIndex >= 0) {
            if (tokens[index].trim() === '') {
                const updatedTokens = [...tokens];
                updatedTokens.splice(index, 1);
                setTokens(updatedTokens);
            } 
            setEditingIndex(-1);
        }
    };
    
    const handleTokenKeyDown = (e, index) => {
        if (e.key === 'Enter') {
            handleTokenInputBlur(index); // Save changes on Enter
        }
        if (e.key === 'Backspace' && tokens[index] === '') {
            // Remove token on backspace
            const updatedTokens = [...tokens];
            updatedTokens.splice(index, 1);
            setTokens(updatedTokens);
            setEditingIndex(-1);
        }
    };

    const handleInputChange = (e, index) => {
        const newValues = [...inputValues];
        newValues[index] = e.target.value;
        setInputValues(newValues);
    };
    
    const handleInputBlur = (index) => {
        const updatedTokens = [...tokens];
        if (inputValues[index].trim() !== '') {
            updatedTokens.splice(index, 0, inputValues[index].trim());
            setTokens(updatedTokens);
        }  
        setInputValues(Array(updatedTokens.length+1).fill(''));
    };
    
    const handleKeyDown = (e, index) => {
        if (e.key === 'Enter') {
            e.target.blur();
            handleInputBlur(index); // Save changes on Enter
        }
        if (e.key === 'Backspace' && inputValues[index] === '') {
            e.target.blur(); // Blur the input field
        }
    };
    
    const handleUpdateRule = async () => {

        const ruleString = tokens.join(' ');

        try {
            const response = await editRule({ rule_id: rule_id, rule_string: ruleString });
            console.log('Rule edited:', response.data);
            
            alert('Rule Edited successfully!');

            navigate('/rule', {
                state: {
                  rule_id:response.data.rule_id,
                  rule_name: response.data.rule_name,
                  rule_root_id: response.data.rule_root_id,
                  rule_tokens: response.data.rule_tokens,
                },
            });

        } catch (error) {
            console.error('Error editing rule:', error);
            alert('Failed to edit rule.');
        }
    };

    const handleJsonInputChange = (e) => {
        setJsonData(e.target.value);
      };
    
    const handleEvaluate = async () => {
        // setShowEvalationResult(false);
        try {
            const parsedData = JSON.parse(jsonData);
            const response = await evaluateRule({ rule_id: rule_id, data: parsedData });
            console.log('Rule evaluated:', response.data);
            const result = JSON.parse(response.data.result);
            setEvalationResult(result);
            setShowEvalationResult(true);
        } catch (error) {
            console.error('Error evaluating data', error);
            alert('Invalid JSON for the rule.');
        }
    };

    useEffect(() => {
        setTokens(rule_tokens);
        setInputValues(Array(rule_tokens.length+1).fill(''));
    }, [rule_tokens]);

    useEffect(() => {
        inputValues.forEach((value, index) => {
            if (spanRefs.current[index]) {
                const spanWidth = spanRefs.current[index].offsetWidth;
                const inputElem = document.querySelector(`#input-${index}`);
                if (inputElem) {
                    inputElem.style.width = `${spanWidth + 3}px`;
                }
            }else{
                const inputElem = document.querySelector(`#input-${index}`);
                if (inputElem) {
                    inputElem.style.width = `${3}px`;
                }
            }
        });
    }, [inputValues]);
    
    useEffect(() => {
        if (editingIndex>=0 && tokenRefs.current[editingIndex]) {
            const tokenWidth = tokenRefs.current[editingIndex].offsetWidth;
            const inputElem = document.querySelector(`#token-${editingIndex}`);
            if (inputElem) {
                inputElem.style.width = `${tokenWidth }px`;
            }
        }
    }, [tokens, editingIndex]);
    

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography variant="h4" gutterBottom marginTop={3}>
                Rule Details
            </Typography>
            
            <Grid container spacing={2} style={{ width: '700px'}}> 
                <Grid item xs={12} size={"grow"} >
                    <Box sx={{ p: 2, border: '1px solid #ccc', borderRadius: 2, boxShadow: 1, backgroundColor: '#f9f9f9', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'flex-start', }} >
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                            <Typography variant="body2" sx={{fontSize:'1rem'}} >
                                Rule Name: {rule_name}
                            </Typography>
                            <Typography variant="body2" sx={{fontSize:'1rem'}} >
                                Rule ID: {rule_id}
                            </Typography>
                            <Typography variant="body2" sx={{fontSize:'1rem'}} >
                                Root ID: {rule_root_id}
                            </Typography>
                        </Box>
                        <Box sx={{ width: '100%', borderBottom: '1px solid #ccc', my: 1 }} />
                            <Typography variant="body1" sx={{ mt: 1, textAlign: 'center', overflowWrap: 'break-word', whiteSpace: 'normal', width: '100%', }} >
                                <strong>{rule_tokens.join(' ')}</strong>
                            </Typography>
                    </Box>
                    
                    <Box sx={{border: '2px solid #00c1cff0', display:'flex', borderRadius:'3px', marginTop:'10px', padding: '5px', flexDirection:'column', width: '100%', alignItems: 'center' }} size='grow'>
                            <div style={{ display: 'flex', flexWrap: 'wrap',  justifyContent: 'center' }}>
                                {tokens.map((token, index) => (
                                    <div key={index} style={{ display: 'flex', alignItems: 'center', marginTop: '2px', marginBottom: '2px' }}  >
                                        <input 
                                        id={`input-${index}`}
                                        value={inputValues[index]}
                                        onChange={(e) => handleInputChange(e, index)}
                                        onKeyDown={(e) => handleKeyDown(e, index)}
                                        onBlur={() => handleInputBlur(index)}
                                        style={{ minWidth: '1px', backgroundColor: '#ffffff00', border: '0px', paddingInline: '2px', marginInline: '4px', fontSize: 'inherit', }}
                                        placeholder='+'
                                        />
                                        <span ref={(el) => (spanRefs.current[index] = el)} style={{ visibility: 'hidden', position: 'absolute', whiteSpace: 'pre', fontSize: 'inherit', }} >
                                            {inputValues[index] || '+' }
                                        </span>

                                        <span ref={(el) => (tokenRefs.current[index] = el)} style={{ visibility: 'hidden', position: 'absolute', paddingInline: '6px', border: '1px solid ', whiteSpace: 'pre', fontWeight: 'bold', }} >
                                            {token}
                                        </span>

                                        {editingIndex === index ? (
                                            <input
                                            id={`token-${index}`}
                                            value={token}
                                            onChange={(e) => handleTokenInputChange(e, index)}
                                            onBlur={() => handleTokenInputBlur(index)}
                                            onKeyDown={(e) => handleTokenKeyDown(e, index)}
                                            autoFocus
                                            style={{ minWidth:'1px', paddingInline: '4px', fontSize: 'inherit', fontWeight: 'bold' }}
                                            />
                                        ) : (
                                            <span style={{ paddingInline: '6px', border: '1px solid #007bffae', cursor: 'pointer', borderRadius: '4px', fontWeight: 'bold', backgroundColor: 'rgba(0, 123, 255, 0.1)' }} 
                                                onClick={() => handleTokenClick(index)}
                                            >
                                                {token}
                                            </span>
                                        )}
                                    </div>
                                ))}
                                <div style={{ display: 'flex', alignItems: 'center', marginTop: '2px', marginBottom: '2px' }}>
                                    <input
                                        id={`input-${tokens.length}`}
                                        value={inputValues[tokens.length]}
                                        onChange={(e) => handleInputChange(e, tokens.length)}
                                        onKeyDown={(e) => handleKeyDown(e, tokens.length)}
                                        onBlur={() => handleInputBlur(tokens.length)}
                                        style={{ minWidth: '1px',backgroundColor: '#ffffff00',border: '0px',paddingInline: '2px',marginInline: '4px',fontSize: 'inherit',}}
                                        placeholder='+'
                                    />
                                    <span ref={(el) => (spanRefs.current[tokens.length] = el)} style={{visibility: 'hidden',position: 'absolute',whiteSpace: 'pre',fontSize: 'inherit',}}>
                                        {inputValues[tokens.length] || '+' }
                                    </span>
                                </div>
                            </div>
                        <Button variant="contained" color="primary" style={{ maxWidth: 'fit-content', marginTop: '10px' }}
                            onClick={handleUpdateRule}>
                            Update Rule
                        </Button>
                    </Box>
                </Grid>
            </Grid>

            <Box sx={{ mt:2, display: 'flex', flexDirection: 'column', gap: 2, p: 2, border: '2px solid #fda585', borderRadius: 2, backgroundColor: '#f9f9f9', boxShadow: 1,width: '700px',}}>
                <Typography variant="h6" gutterBottom>
                    Enter Data for Rule Evaluation (JSON format):
                </Typography>
            
                <TextField label="JSON Input" multiline rows={6} color='secondary' variant="outlined" value={jsonData} onChange={handleJsonInputChange} fullWidth sx={{ backgroundColor: '#fff', borderRadius: 1 }} />

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2, }} >
                    <Button variant="contained" color="secondary" onClick={handleEvaluate}>
                        Submit
                    </Button>

                    {showEvalationResult && (
                        <Typography
                            variant="body1"
                            sx={{
                            color: 'white',
                            backgroundColor: evalationResult ? '#4CAF50' : '#F44336',
                            p: 1,
                            borderRadius: 2,
                            boxShadow: 2,
                        
                            }}
                        >
                            {evalationResult ? 'Rule Passed' : 'Rule Failed'}
                        </Typography>
                    )}
                </Box>
            </Box>
        </div>

    );
};

export default RulePage;
