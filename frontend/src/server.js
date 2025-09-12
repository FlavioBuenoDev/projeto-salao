const express = require('express');
const app = express();
const PORT = 3000;

app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'Frontend está funcionando!' });
});

app.listen(PORT, () => {
  console.log(`Frontend rodando na porta ${PORT}`);
});