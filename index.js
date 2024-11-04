const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Route to handle POST requests to /generate
app.post('/generate', async (req, res) => {
    const { prompt } = req.headers;

    if (!prompt) {
        return res.status(400).json({ error: 'Prompt is required' });
    }

    const API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large";
    const api_token = process.env.HUGGINGFACE_API_TOKEN;

    if (!api_token) {
        return res.status(500).json({ error: 'HUGGINGFACE_API_TOKEN environment variable is not set' });
    }

    const headers = { "Authorization": `Bearer ${api_token}` };
    const payload = { "inputs": prompt };

    const ora = (await import('ora')).default;
    const spinner = ora('Generating image...').start();

    try {
        const response = await axios.post(API_URL, payload, { headers, responseType: 'arraybuffer' });
        const imageBytes = Buffer.from(response.data, 'binary');

        spinner.succeed('Image generated successfully');

        res.set('Content-Type', 'image/png');
        res.send(imageBytes);
    } catch (error) {
        spinner.fail('Failed to generate image');
        console.error(`An error occurred: ${error}`);
        res.status(500).json({ error: 'Failed to generate image' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});